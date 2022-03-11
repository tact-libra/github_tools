from os.path import expanduser

class Config:
	CERT_DIR = f"{expanduser('~')}/.config/github/"
	CERT_FILE = CERT_DIR + "certification"

	HOST_DOMAIN = "https://api.github.com"
	USER = HOST_DOMAIN + "/user"
	REPOS = HOST_DOMAIN + "/repos"
	USER_REPOS = HOST_DOMAIN + "/user/repos"
	ORG_REPOS = HOST_DOMAIN + "/orgs/{}/repos"
