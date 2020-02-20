



def GetChkSum(strData):
	chksum = 0
	chksum = chksum	^ (int(str(int("20", 16)), 10))
	chksum = chksum	^ (int(str(int("03", 16)), 10))
	print("Checksum - " + str(chksum))
	for char in strData:
		print(char + " - " + str(ord(char)))
		chksum = chksum ^ ord(char)
		print("Checksum - " + str(chksum))
	chksum = chksum	^ (int(str(int("04", 16)), 10))
	return chksum


def inicio():
    

if __name__ == "__main__":
    inicio()
    print("EXIT ROBOT")