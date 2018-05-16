fp = open("nboutput.txt")
data1 = fp.readlines()
fp = open("dev-key.txt")
data2 = fp.readlines()
index = 0
count = 0
while index < len(data2):
	line1 = data1[index].split()
	line2 = data2[index].split()
	isError = False
	for i in range(1, len(line1)):
		word1 = line1[i]
		word2 = line2[i]
		if (word1 != word2):
			isError = True
	if(isError):
		count += 1
	index += 1
print len(data2)
print count
print (len(data2) - count)/float(len(data2))