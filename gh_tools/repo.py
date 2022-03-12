from requests import (
	get,
	post,
	delete,
)

class Repo:
	def __init__(self):
		repo = repo.add_parser(
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
		create.set_defaults(private=False, subcommand_func=self.repo_create)

		#delete
		delete = repo.add_parser("delete", help=f"{self.cmd} delete -h")
		delete.add_argument("owner", help="owner of repository to delete.")
		delete.add_argument("name", help="name of repository to delete.")
		delete.set_defaults(subcommand_func=self.repo_delete)

		#list
		list_ = repo.add_parser("list", help=f"{self.cmd} list -h")
		list_.set_defaults(subcommand_func=self.repo_list)

	def repo_create(self):
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

	def repo_delete(self):
		res = self._request(delete, f"{Config.REPOS}/{self.args.owner}/{self.args.name}")
		if res.status_code == 204:
			print("success")
		else:
			print(res.__dict__)
		return (res.status_code, res)

	def repo_list(self):
		res = self._request(get, Config.USER_REPOS)
		if res.status_code == 200:
			data = [str((i["full_name"], i["owner"]["type"])) for i in res.json()]
			print("\n".join(sorted(data)))
		return (res.status_code, res)








