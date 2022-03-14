from requests import (
	get,
	post
)

class User:
	def __init__(self):
		#profile
		profile = self.subparsers.add_parser("profile", help=f"{self.cmd} profile -h")
		profile.set_defaults(subcommand_func=self.profile)

	def profile(self):
		res = self._request(get, Config.USER)
		if res.status_code == 200:
			data = res.json()
			print(f"username\t{data['name']}")
			print(f"userid\t{data['login']}")
		#else:
			print(res.json())
		return (res.status_code, res)





