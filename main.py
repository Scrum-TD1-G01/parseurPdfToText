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

# recuperer le pdf source
sortie = open(sys.argv[1]+"_parser.txt","w")  # delete le dernier fichier si il existe
sortie.write("Fichier Original: \n"+"    "+sys.argv[1]+"\n")


#recuperer les metadata et title
raw_pdf = open(sys.argv[1],'rb')#recuperer le pdf raw pour extract les metadata
parser = PDFParser(raw_pdf)
doc = PDFDocument(parser)#cast le PDF en doc dans notre code
sortie.write("Title: \n")

if(doc.info[0]['Title']):
	try:
		sortie.write(doc.info[0]['Title'].decode("utf-16"))
	except UnicodeDecodeError:
		sortie.write(str(doc.info[0]['Title']))
else:
	sortie.write(lines[0].strip()+'\n')

sortie.write("\n")




# recuperer l'abstract
sortie.write("Abstract: \n")

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
		sortie.write(line.strip())

sortie.write('\n')
sortie.close()
pdf.close()


