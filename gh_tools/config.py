from os.path import expanduser

class Config:
	CONFIG_DIR = f"{expanduser('~')}/.config/github/"
	CONFIG_FILE = CONFIG_DIR + "userdata.json"

	CREATE_SESSION_URL = "https://github.com/login/device/code"
	CHK_VERIFICATE_URL = "https://github.com/login/oauth/access_token"
	CLIENT_ID = "03b4aeb92e636572c285"

	HOST_DOMAIN = "https://api.github.com"
	USER = HOST_DOMAIN + "/user"
	REPOS = HOST_DOMAIN + "/repos"
	USER_REPOS = HOST_DOMAIN + "/user/repos"
	ORG_REPOS = HOST_DOMAIN + "/orgs/{}/repos"
