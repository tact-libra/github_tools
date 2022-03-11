#!/usr/bin/python3
import argparse, os
import requests

def user_input(msg, _type):
	while True:
		try:
			return _type(input(msg))
		except TypeErorr as e:
			print("Incorrect input")

class Config:
	CERT_DIR = f"{os.path.expanduser('~')}/.config/github/"
	CERT_FILE = CERT_DIR + "certification"

	HOST_DOMAIN = "https://api.github.com"
	USER = HOST_DOMAIN + "/user"
	REPOS = HOST_DOMAIN + "/repos"
	USER_REPOS = HOST_DOMAIN + "/user/repos"
	ORG_REPOS = HOST_DOMAIN + "/orgs/{}/repos"

class TOOLS:
	cmd = os.path.basename(__file__)
	parser = argparse.ArgumentParser(
		description="",
		formatter_class=argparse.RawTextHelpFormatter
	)
	subparsers = parser.add_subparsers(required=True)

	def __init__(self):
		#login
		login = self.subparsers.add_parser("login", help=f"{self.cmd} login -h")
		login.add_argument("--token", action='store_true')
		login.set_defaults(subcommand_func=self.login)

		#profile
		profile = self.subparsers.add_parser("profile", help=f"{self.cmd} profile -h")
		profile.set_defaults(subcommand_func=self.profile)

		#create
		create = self.subparsers.add_parser("create", help=f"{self.cmd} create -h")
		create.add_argument("name", help="Name of repository to create.")
		create_private = create.add_mutually_exclusive_group()
		create_private.add_argument("--public", dest="private", action='store_false', help="Create in public repository. (default)")
		create_private.add_argument("--private", dest="private", action='store_true', help="Create in private repository.")
		create.add_argument("--org", help="set org name")
		create.set_defaults(private=False, subcommand_func=self.create)

		#delete
		delete = self.subparsers.add_parser("delete", help=f"{self.cmd} delete -h")
		delete.add_argument("owner", help="owner of repository to delete.")
		delete.add_argument("name", help="name of repository to delete.")
		delete.set_defaults(subcommand_func=self.delete)

		#list
		list_ = self.subparsers.add_parser("list", help=f"{self.cmd} list -h")
		list_.set_defaults(subcommand_func=self.list_)

		#run
		self.token = self._get_token()
		self.args = self.parser.parse_args()
		print(self.args)
		if hasattr(self.args, 'subcommand_func'):
			self.args.subcommand_func()
		else:
			self.parser.print_help()

	def _get_token(self):
		if os.path.isfile(Config.CERT_FILE):
			with open(Config.CERT_FILE) as f:
				token = f.read().splitlines()[0]
			return token
		else:
			return None

	def _post(self, func, url, headers={}, **kwargs):
		headers["Authorization"] = "token " + self._get_token()
		return func(url, headers=headers, **kwargs)

	def login(self):
		os.makedirs(f"{Config.CERT_DIR}", exist_ok=True)
		token = None
		if self.args.token:
			token = user_input("token: ", str)
			code, _ = self.profile(token)
			if code == 200:
				with open(f"{Config.CERT_FILE}", "w") as f:
					f.write(token)
			else:
				print("authentication failure")
		else:
			print("Use '--token'.")
		if token:
			self.profile()

	def profile(self, token=None):
		if (not token and not self._get_token()):
			return print("Please login")
		res = self._post(requests.get, Config.USER)
		if res.status_code == 200:
			data = res.json()
			print(f"username\t{data['name']}")
			print(f"userid\t{data['login']}")
		#else:
		print(res.json())
		return (res.status_code, res)

	def create(self):
		if not self._get_token():
			return print("Please login")
		if self.args.org:
			url = Config.ORG_REPOS.format(self.args.org)
		else:
			url = Config.USER_REPOS
		res = self._post(requests.post, url, json={
			"name": self.args.name,
			"private": self.args.private
		})
		if res.status_code == 201:
			print("success")
		else:
			print(res.__dict__)
		return (res.status_code, res)

	def delete(self):
		if not self._get_token():
			return print("Please login")
		res = self._post(requests.delete, f"{Config.REPOS}/{self.args.owner}/{self.args.name}")
		if res.status_code == 204:
			print("success")
		else:
			print(res.__dict__)
		return (res.status_code, res)

	def list_(self):
		if not self._get_token():
			return print("Please login")
		res = self._post(requests.get, Config.USER_REPOS)
		if res.status_code == 200:
			data = [i["full_name"] for i in res.json()]
			print("\n".join(sorted(data)))
		return (res.status_code, res)


TOOLS()
