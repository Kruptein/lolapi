import redis as re
import time

redis = re.StrictRedis()

def _string_to_dict(string:str):
    d = {}
    for pair in string.split(","):
        value, key = pair.split(":")
        d[int(key)] = int(value)
    return d

def redis_wrap(cls):
    class RedisRateLimitedEndpoint(cls):

        @classmethod
        def rget(clz, region:str, url:str):
            """
            Rate limited version of the Endpoint.rget method.
            Redis is used as a backend to keep track of rate limits for both app and method limits.
            """
            clz.wait(url)
            response = super().rget(region, url)
            clz.ratelimit(response)
            return response

        @classmethod
        def wait(clz, url:str):
            limits = redis.hgetall("app_limits")
            for limit in limits:
                key_str = "app_limits:{}".format(int(limit))
                if redis.zcard(key_str) >= int(limits[limit]):
                    redis.zremrangebyscore(key_str, '-inf', redis.time()[0] - int(limit) - 1)  # Subtract 1 second as a safety margin.
                    # If the count is still too large after removing scores, we have to sleep.
                    while redis.zcard(key_str) >= int(limits[limit]):
                        sleep_time = redis.zrange(key_str, 0, 0, withscores=True)[0][1] + int(limit) - int(redis.time()[0]) + 1  # Sleep an extra second as a safety margin
                        time.sleep(sleep_time)
                        redis.zremrangebyrank(key_str, 0, 0)

        @classmethod
        def ratelimit(clz, response):
            # Not every endpoint is ratelimited, use -1 to signify this.
            try:
                app_rate_limit = _string_to_dict(response.headers.get("X-App-Rate-Limit", ""))
                app_rate_limit_count = _string_to_dict(response.headers.get("X-App-Rate-Limit-Count", ""))
            except ValueError:
                return

            redis.hmset("app_limits", app_rate_limit)
            for limit in app_rate_limit:
                key_str = "app_limits:{}".format(limit)
                local_count = redis.zcard(key_str)
                actual_count = app_rate_limit_count[limit]
                # If our local count is less than the actual count, we add the missing values as if they were added now
                # This includes the current invocation and has the advantage that any missed count is also taken into account.
                if local_count < actual_count:
                    clock = int(redis.time()[0])
                    for i, _ in enumerate(range(actual_count-local_count)):
                        # We do not care about the key, but it has to be unique or we'll potentially update other keys still in the set!
                        redis.zadd(key_str, clock, "{}_{}_{}_{}".format(clock, i, actual_count, local_count))
                elif local_count == actual_count:
                    clock = int(redis.time()[0])
                    # We do not care about the key, but it has to be unique or we'll potentially update other keys still in the set!
                    redis.zadd(key_str, clock, "{}_{}_{}".format(clock, actual_count, local_count))
                # If our local count is larger than the actual count, we have some stale values which would be removed by the cleaner
                # But we can already do this now so go ahead.
                else:
                    redis.zremrangebyrank(key_str, 0, local_count-actual_count)


    return RedisRateLimitedEndpoint
