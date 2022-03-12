import argparse, os, urllib.parse, time
from requests import (
	get,
	post,
	delete,
	Response
)
from .config import Config
from .account import Account
from .auth import Auth
from .repo import Repo
from .uesr import User

class Tools(Account, Auth, Repo, User):
	cmd = os.path.splitext(os.path.basename(__file__))[0]

	def __init__(self):
		Account.__init__()
		Auth.__init__()
		Repo.__init__()
		User.__init__()

		parser = argparse.ArgumentParser(
			description="",
			formatter_class=argparse.RawTextHelpFormatter
		)
		parser.add_argument('--version', action='version', version='%(prog)s 0.1')
		parser.add_argument("--user", help="")
		subparsers = parser.add_subparsers()
	
	def run(self):
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
			print("need to log in")
			return Response()
		headers.setdefault("Authorization", "token " + str(self.user.get_token()))
		result = func(url, headers=headers, **kwargs)
		if result.status_code == 401:
			print("need to log in")
		return result

	


def main():
	Tools().run()

if __name__ == '__main__':
	main()
