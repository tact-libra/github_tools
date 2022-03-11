from os.path import expanduser

class Config:
	CONFIG_DIR = f"{expanduser('~')}/.config/github/"
	CONFIG_FILE = CONFIG_DIR + "userdata.json"

	HOST_DOMAIN = "https://api.github.com"
	USER = HOST_DOMAIN + "/user"
	REPOS = HOST_DOMAIN + "/repos"
	USER_REPOS = HOST_DOMAIN + "/user/repos"
	ORG_REPOS = HOST_DOMAIN + "/orgs/{}/repos"
