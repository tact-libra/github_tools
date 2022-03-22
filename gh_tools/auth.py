import time, os, webbrowser
from requests import (
	get,
	post
)
from .config import Config
from .account import Account

def post_json_request(*args, **kwargs):
	headers = kwargs.pop("headers", {})
	headers.setdefault("Accept", "application/json")
	return post(*args, headers=headers, **kwargs)


def user_input(msg, _type):
	while True:
		try:
			return _type(input(msg))
		except TypeErorr as e:
			print("Incorrect input")


class Auth:
	def __init__(self):
		#login
		login = self.subparsers.add_parser("login", help=f"{self.cmd} login -h")
		login.add_argument("--token", action='store_true', help="login using token")
		login.set_defaults(subcommand_func=self.login)
	
	def _get_user_code(self):
		req = post_json_request(Config.CREATE_SESSION_URL,params={
			"client_id": Config.CLIENT_ID,
			"scope": " ".join([
				"repo",
				"public_repo",
				"repo_deployment",
				"delete_repo",
				"security_events",
				"gist",
				"user"
			])
		}).json()
		return (
			req["user_code"],
			req["device_code"]
		)

	def _check_verify_request(self, device_code):
		while True:
			res = post_json_request(Config.CHK_VERIFICATE_URL, params={
				"client_id": Config.CLIENT_ID,
				"device_code":device_code,
				"grant_type": Config.GRANT_TYPE
			}).json()

			error = res.get("error", None)
			if res.get("access_token", None) != None:
				return (0, res["access_token"])
			elif error == "authorization_pending":
				time.sleep(5)
			elif error == "slow_down":
				time.sleep(res["interval"])
			elif error == "access_denied":
				return (1, "access_denied")
			elif error in ["expired_token", "incorrect_device_code"]:
				return (2, error)
			else:
				raise Exception(f"[ERROR] {error}")

	def device_flow(self):
		user_code, device_code = self._get_user_code()
		print("\n  ".join([f"Open this link and enter code.", f"URL: {Config.VERIFICATION_URL}", f"code: {user_code}"]))
		webbrowser.open(Config.VERIFICATION_URL)
		error, token = self._check_verify_request(device_code)
		if not error:
			return token
		elif error == 1:
			print("Cancelled.")
		elif error == 2:
			print("Code expiration date has passed.")
		print("Please try again.")
		return None

	def login(self):
		if self.args.token:
			token = user_input("token: ", str)
		else:
			token = self.device_flow()
		res = self._request(
			get, Config.USER,
			headers={"Authorization": f"token {token}"},
			chklogin=False
		)
		if res.status_code == 200:
			data = res.json()
			self.set_token(data["login"], token, {
				"login": data["login"],
				"id": data["id"],
				"name": data["name"]
			})
		else:
			print("authentication failure")


