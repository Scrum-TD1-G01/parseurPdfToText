import pdftotext
import sys
import unicodedata
import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
def prettify(elem):
	rough_string = ElementTree.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent=" ")


exportFormat = ""

if (len(sys.argv) > 2):
	if (sys.argv[2] == "-t"):
		print("export txt")
		exportFormat = "txt"
	elif (sys.argv[2] == "-x"):
		print("export xml")
		exportFormat = "xml"

# Dictionnaire data
data = {'fileName' : "",
		'abstract' : "123",
		'title' : ""
		}

# Convert pdf
os.system("pdftotext -nopgbrk "+sys.argv[1])
pdf = open(os.path.splitext(sys.argv[1])[0]+'.txt',"r")
lines = pdf.readlines()

#genereration template xml
root = Element('opml')
root.set('version','1.0')
head = SubElement(root, 'article')
title = SubElement(head, 'title')
auteur = SubElement(head, 'auteur')
abstract = SubElement(head, 'abstract')
biblio = SubElement(head, 'biblio')
print (prettify(root))
# recuperer le pdf source
sortie = open(sys.argv[2]+"_parser.txt","w")  # delete le dernier fichier si il existe
#sortie.write("Fichier Original: \n"+"    "+sys.argv[1]+"\n")
data['fileName'] = sys.argv[1]



#recuperer les metadata et title
raw_pdf = open(sys.argv[1],'rb')#recuperer le pdf raw pour extract les metadata
parser = PDFParser(raw_pdf)
doc = PDFDocument(parser)#cast le PDF en doc dans notre code
sortie.write("Title: \n")

if(doc.info[0]['Title']):
	try:
		#sortie.write(doc.info[0]['Title'].decode("utf-16"))
		data['title'] = doc.info[0]['Title'].decode("utf-16")
	except UnicodeDecodeError:
		sortie.write(str(doc.info[0]['Title']))
		#data['title'] = str(doc.info[0]['Title'])
else:
	sortie.write(lines[0].strip()+'\n')
	#data['title'] = lines[0].strip()+'\n'

sortie.write("\n")




# recuperer l'abstract
sortie.write("<auteur>")

copy = False
cpt = 0
abstractStart = False
for line in lines:
	if str("Abstract\n") in line:
		copy = True
		abstractStart = True
		sortie.write("</auteur>\n<abstract>")
	elif str("ABSTRACT\n") in line:
		copy = True
		abstractStart = True
		sortie.write("</auteur>\n<abstract>")
	elif (cpt > 0 and abstractStart == False):
		sortie.write(line.strip())
	elif str("1\n") in line:
		copy = False
		sortie.write("</abstract>")
	elif str("I.\n") in line:
		copy = False
		sortie.write("</abstract>")
	elif str("1.\n") in line:
		copy = False
		sortie.write("</abstract>")
	elif copy:
		#sortie.write(line.strip())
		data['abstract'] = data['abstract']+str(line.strip())
	cpt += 1

if exportFormat == "txt":
	sortie.write("Preamble : ")
	sortie.write(data['fileName']+"\n")
	sortie.write("Title : ")
	sortie.write(data['title']+"\n")
	sortie.write("Abstract : ")
	sortie.write(data['abstract']+"\n")
'''
sortie.write('\n')
sortie.close()
pdf.close()
'''


