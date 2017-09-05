class QueryBuilder:
	def __init__(self):
		self.values = []

	def build(self):
		if self.values:
			return "?" + "&".join(self.values)
		return ""

	def add_string(self, key, value):
		if value:
			self.values.append("{}={}".format(key, value))

	def add_int(self, key, value):
		if value:
			self.values.append("{}={}".format(key, value))

	def add_bool(self, key, value):
		if value is not None:
			self.values.append("{}={}".format(key, "true" if value else "false"))

	def add_set(self, key, value):
		if value:
			for v in value:
				self.values.append("{}={}".format(key, v))