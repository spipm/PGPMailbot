

def parse_config_file(filename="./config/pgpmailbot.conf"):
	'''
		Simple configuration parser
			Don't use the '=' sign in values
		'''
	config = {}
	with open(filename,'r') as data:
		for line in data.readlines():
			parts = line.strip("\n").split("=")
			config[parts[0]] = parts[1]

	return config

