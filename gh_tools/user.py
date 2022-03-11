import json, os
from .config import Config

class User:
	def __init__(self):
		if os.path.isfile(Config.CONFIG_FILE):
			with open(Config.CONFIG_FILE) as f:
				self.data = json.load(f)
		else:
			with open(Config.CONFIG_FILE, "w") as f:
				f.write("{}")
			self.data = {}
		self.select_user = self.get_default_user()
	
	def __save(self):
		with open(Config.CONFIG_FILE, "w") as f:
			json.dump(self.data, f, indent=4)

	def get_user_list(self):
		return list(self.data.keys())

	def get_default_user(self):
		for name, val in self.data.items():
			if val.get("x-gh-default", False):
				return name
		return None
	
	def set_default_user(self, name):
		if self.data.get(name, None) == None:
			return None
		defaulted_user = self.get_default_user()
		if defaulted_user:
			self.data[defaulted_user]["x-gh-default"] = False
		self.data[name]["x-gh-default"] = True
		return True

	def get_token(self, name=None):
		if not name:
			name = self.select_user
		return self.data.get(name, {}).get("x-gh-token", None)

	def set_token(self, name, token, val={}, default=None):
		if default == None and self.data == {}:
			default = True
		elif default == None:
			default = False
		self.data[name] = val
		self.data[name]["x-gh-token"] = token
		self.data[name]["x-gh-default"] = default
		self.__save()

