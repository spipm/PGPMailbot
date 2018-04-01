
def string_between_lt_gt(string):
	firstIndex = string.find('<')+1 if '<' in string else 0
	lastIndex = string.find('>') if '>' in string else strlen(string)
	return string[firstIndex:lastIndex]

def return_path_match_from(mailObject):
	returnPath = mailObject.get("Return-Path")
	fromAddress = mailObject.get("From")

	return string_between_lt_gt(returnPath) == string_between_lt_gt(fromAddress)
