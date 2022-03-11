import argparse, os
from requests import (
	get,
	post,
	delete,
	Response
)
from .config import Config
from .user import User


def user_input(msg, _type):
	while True:
		try:
			return _type(input(msg))
		except TypeErorr as e:
			print("Incorrect input")


class Tools:
	user = User()
	cmd = os.path.splitext(os.path.basename(__file__))[0]
	parser = argparse.ArgumentParser(
		description="",
		formatter_class=argparse.RawTextHelpFormatter
	)
	parser.add_argument("--user", help="")
	subparsers = parser.add_subparsers()

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
		self.args = self.parser.parse_args()
		if self.args.user:
			if self.args.user in self.user.get_user_list():
				self.user.select_user = self.args.user
			else:
				return print("Incorrect argument: user")
		if hasattr(self.args, 'subcommand_func'):
			self.args.subcommand_func()
		else:
			self.parser.print_help()

	def _request(self, func, url, headers={}, **kwargs):
		if kwargs.pop("chklogin", True) and not self.user.get_token():
			return Response()
		headers.setdefault("Authorization", "token " + str(self.user.get_token()))
		return func(url, headers=headers, **kwargs)

	def login(self):
		os.makedirs(f"{Config.CONFIG_DIR}", exist_ok=True)
		token = None
		if self.args.token:
			token = user_input("token: ", str)
			res = self._request(
				get, Config.USER,
				headers={"Authorization": f"token {token}"},
				chklogin=(token==None)
			)
			if res.status_code == 200:
				data = res.json()
				self.user.set_token(data["login"], token, data)
			else:
				print("authentication failure")
		else:
			print("Use '--token'.")
		if token:
			self.profile()

	def profile(self):
		res = self._request(get, Config.USER)
		if res.status_code == 200:
			data = res.json()
			print(f"username\t{data['name']}")
			print(f"userid\t{data['login']}")
		#else:
			print(res.json())
		return (res.status_code, res)

	def create(self):
		if self.args.org:
			url = Config.ORG_REPOS.format(self.args.org)
		else:
			url = Config.USER_REPOS
		res = self._request(post, url, json={
			"name": self.args.name,
			"private": self.args.private
		})
		if res.status_code == 201:
			print("success")
		else:
			print(res.__dict__)
		return (res.status_code, res)

	def delete(self):
		res = self._request(delete, f"{Config.REPOS}/{self.args.owner}/{self.args.name}")
		if res.status_code == 204:
			print("success")
		else:
			print(res.__dict__)
		return (res.status_code, res)

	def list_(self):
		res = self._request(get, Config.USER_REPOS)
		if res.status_code == 200:
			data = [str((i["full_name"], i["owner"]["type"])) for i in res.json()]
			print("\n".join(sorted(data)))
		return (res.status_code, res)



def main():
	Tools()

if __name__ == '__main__':
	main()
