import pdftotext
import sys
import unicodedata
import os

# Convert pdf
os.system("pdftotext -nopgbrk "+sys.argv[1])
pdf = open(os.path.splitext(sys.argv[1])[0]+'.txt',"r")

#recuperer le pdf source
sortie = open(sys.argv[1]+"_parser.txt","w")#delete le dernier fichier si il existe
sortie.write("Fichier Original: \n"+"    "+sys.argv[1]+"\n")
sortie.write("Abstract: \n")
#recuperer l'abstract
lines = pdf.readlines()
copy = False
for line in lines:
	if str("Abstract") in line:
		copy = True
	elif str("ABSTRACT") in line:
		copy = True
	elif str("1\n") in line:
		copy = False
	elif str("I.") in line:
		copy = False
	elif str("1.\n") in line:
		copy = False
	elif copy:
		sortie.write(line.strip())
		
		
		
		
sortie.close()
pdf.close()


