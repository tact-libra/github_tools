from requests import (
	get,
	post,
	delete,
)
from .config import Config

class Repo:
	def __init__(self):
		repo = self.subparsers.add_parser(
			"repo",
			help=f"{self.cmd} repo -h"
		).add_subparsers()

		#create
		create = repo.add_parser("create", help=f"{self.cmd} create -h")
		create.add_argument("name", help="Name of repository to create.")
		create_private = create.add_mutually_exclusive_group()
		create_private.add_argument("--public", dest="private", action='store_false', help="Create in public repository. (default)")
		create_private.add_argument("--private", dest="private", action='store_true', help="Create in private repository.")
		create.add_argument("--description")
		create.add_argument("--licence", help="set repository licence")
		create.add_argument("--gitignore")
		create.add_argument("--org", help="set org name")
		create.set_defaults(private=False, subcommand_func=self.create_repo)

		#delete
		delete = repo.add_parser("delete", help=f"{self.cmd} delete -h")
		delete.add_argument("owner", help="owner of repository to delete.")
		delete.add_argument("name", help="name of repository to delete.")
		delete.set_defaults(subcommand_func=self.delete_repo)

		#list
		list_ = repo.add_parser("list", help=f"{self.cmd} list -h")
		list_.add_argument("--all", action="store_true")
		list_.add_argument("--org")
		list_.set_defaults(subcommand_func=self.list_repo)

	def create_repo(self):
		if self.args.org:
			url = Config.ORG_REPOS.format(self.args.org)
		else:
			url = Config.USER_REPOS
		res = self._request(post, url, json={
			"name": self.args.name,
			"description": self.args.description,
			"private": self.args.private,
			"license_template": self.args.licence,
			"gitignore_template": self.args.gitignore
		})
		if res.status_code == 201:
			print("success")
		else:
			print(res.__dict__)
		return (res.status_code, res)

	def delete_repo(self):
		res = self._request(delete, f"{Config.REPOS}/{self.args.owner}/{self.args.name}")
		if res.status_code == 204:
			print("success")
		else:
			print(res.__dict__)
		return (res.status_code, res)

	def list_repo(self):
		res = self._request(get, Config.USER_REPOS)
		if res.status_code == 200:
			if self.args.all:
				data = [i["full_name"] for i in res.json()]
			elif self.args.org:
				data = [i["name"] for i in res.json() if self.args.org == i["owner"]["login"]]
			else:
				data = [i["name"] for i in res.json() if self.get_user_id(self.select_user) == i["owner"]["id"]]
			print("\n".join(sorted(data)))
		return (res.status_code, res)








