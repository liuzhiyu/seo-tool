with open("keyword.txt") as file:
	for keyword in file:
		keyword =  keyword.rstrip()
		keyword.decode('gbk')
		print keyword
		