import sys
import glob
import os

data = {}

dirPath = sys.argv[1]

fileList = glob.glob(dirPath+'**.pdf')
fileListKey = []
fileListDic = {}
for i in fileList:
	fileListKey.append(os.path.basename(i))
	fileListDic[fileListKey[-1]] = i

for i in range(len(fileListDic)):
	print(str(i)+" :", fileListKey[i])


resFileToParse = int(input("Saisir le numero du pdf à parser : "))
print("Parsing du document :", fileListKey[resFileToParse])
data['fileName'] = fileListDic[fileListKey[resFileToParse]]
print("Adresse du document :", data['fileName'])
