# f = open("temp.csv","r")
# fw = open("temp-final.csv","w")
# ls = f.readlines()
# for l in ls:
# 	fw.write(l[6:].replace("  ",",")[:-3] + "\n")


f = open("CA-animal.csv","r")
ls = f.readlines()
fw = open("animal-count.csv","w")
i = 67
count = 0

for l in ls:
	year = int(l.split(",")[-2].split("/")[-1])
	if i == year:
		count = count + 1
	else: 
		if (i <40):
			fw.write("20%d,%d\n"%(i, count))
		else:
			fw.write("19%d,%d\n"%(i, count))
		count = 1
		i = year


