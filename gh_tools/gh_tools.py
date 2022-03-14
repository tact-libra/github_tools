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
from .user import User

class Tools(Account, Auth, Repo, User):
	cmd = os.path.splitext(os.path.basename(__file__))[0]

	def __init__(self):
		self.parser = argparse.ArgumentParser(
			description="",
			formatter_class=argparse.RawTextHelpFormatter
		)
		self.parser.add_argument('--version', action='version', version='%(prog)s 0.1')
		self.parser.add_argument("--user", help="")
		self.subparsers = self.parser.add_subparsers()

		Account.__init__(self)
		Auth.__init__(self)
		Repo.__init__(self)
		User.__init__(self)

	def run(self):
		self.args = self.parser.parse_args()
		if self.args.user:
			if self.args.user in self._get_user_list():
				self.select_user = self.args.user
			else:
				return print("Incorrect argument: user")

		if hasattr(self.args, 'subcommand_func'):
			self.args.subcommand_func()
		else:
			self.parser.print_help()

	def _request(self, func, url, headers={}, **kwargs):
		if kwargs.pop("chklogin", True) and not self.get_token():
			print("need to log in")
			return Response()
		headers.setdefault("Authorization", "token " + str(self.get_token()))
		result = func(url, headers=headers, **kwargs)
		if result.status_code == 401:
			print("need to log in")
		return result




def main():
	try:
		Tools().run()
	except KeyboardInterrupt:
		print("ERROR: Operation cancelled by user")

if __name__ == '__main__':
	main()
