import pdftotext
import sys
import unicodedata
import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

# Convert pdf
os.system("pdftotext -nopgbrk "+sys.argv[1])
pdf = open(os.path.splitext(sys.argv[1])[0]+'.txt',"r")
lines = pdf.readlines()

# Dictionnaire data
data = {'fileName' : "",
		'Abstract' : "123",
		'Title' : ""
		}

# recuperer le pdf source
sortie = open(sys.argv[1]+"_parser.txt","w")  # delete le dernier fichier si il existe

# recuperer le fileName original
#sortie.write("Fichier Original: \n"+"    "+sys.argv[1]+"\n")
data['fileName'] = sys.argv[1]


#recuperer les metadata et title
raw_pdf = open(sys.argv[1],'rb')#recuperer le pdf raw pour extract les metadata
parser = PDFParser(raw_pdf)
doc = PDFDocument(parser)#cast le PDF en doc dans notre code
#sortie.write("Title: \n")

if(doc.info[0]['Title']):
	try:
		#sortie.write(doc.info[0]['Title'].decode("utf-16"))
		data['Title'] = doc.info[0]['Title'].decode("utf-16")
	except UnicodeDecodeError:
		#sortie.write(str(doc.info[0]['Title']))
		data['Title'] = str(doc.info[0]['Title'])
else:
	#sortie.write(lines[0].strip()+'\n')
	data['Title'] = lines[0].strip()+'\n'

# sortie.write("\n")




# recuperer l'abstract
#sortie.write("Abstract: \n")

copy = False
for line in lines:
	if str("Abstract\n") in line:
		copy = True
	elif str("ABSTRACT\n") in line:
		copy = True
	elif str("1\n") in line:
		copy = False
	elif str("I.\n") in line:
		copy = False
	elif str("1.\n") in line:
		copy = False
	elif copy:
		#sortie.write(line.strip())
		print("IN abstract")
		data['Abstract'] = data['Abstract']+str(line.strip())

#sortie.write('\n')
#sortie.close()
print(data)
for i in data.keys():
	sortie.write(i+": "+data[i]+'\n')
pdf.close()


