import re

testBatteryData = "V[0]=128390/n/rBATMAN/n/rT[0]=123556/n/rV[99]=123456/n/rBC=12346"
testEngineData = "t7FF8AABBCCDDEEFFAABB/r/nt7FF8AABBCCDDEEFFAABB"

#A 'V' or a 'T' followed by a '[' with any number of 0-9s with a ']' after
#or 'BC=' followed by any number of 0-9s
batteryPattern = re.compile('([V|T]\\[[0-9]*\\]=[0-9]*|BC=[0-9]*)|BATMAN|ROBIN')
batmanRecognitionPattern = re.compile('BATMAN')
robinRecognitionPattern = re.compile('ROBIN')

enginePattern = re.compile('(t([0-9]|[A-F])*)')

m1 = batteryPattern.search(testBatteryData) #True
m2 = batteryPattern.match(testEngineData) #False
m3 = enginePattern.match(testEngineData) #True
m4 = enginePattern.match(testBatteryData) #False

while m1 != None:
	print(testBatteryData + " : " + m1.group())
	testBatteryData = testBatteryData[testBatteryData.index(m1.group())+len(m1.group())+4 : len(testBatteryData)]
	m1 = batteryPattern.search(testBatteryData)

code = "t40380000000000000000"
codeArray = list(code)

IDNum = int("0x" + codeArray[1] + codeArray[2] + codeArray [3], 16)     

#test
print ("ID =", IDNum)

#first number
hex1 = "0x" + codeArray[5] + codeArray[6]
hex2 = "0x" + codeArray[7] + codeArray[8]
hex3 = "0x" + codeArray[9] + codeArray[10]
hex4 = "0x" + codeArray[11] + codeArray[12]
first_number = int(hex1,16)+int(hex2,16)+int(hex3,16)+int(hex4,16)

#second number
hex5 = "0x" + codeArray[13] + codeArray[14]
hex6 = "0x" + codeArray[15] + codeArray[16]
hex7 = "0x" + codeArray[17] + codeArray[18]
hex8 = "0x" + codeArray[19] + codeArray[20]
second_number = int(hex5,16)+int(hex6,16)+int(hex7,16)+int(hex8,16)

print("First Numb:", first_number," Second Number:", second_number)