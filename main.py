import pdftotext
import sys
import unicodedata
import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import xml
def prettify(elem):
	try:
		rough_string = ElementTree.tostring(elem, encoding='utf-8')
		reparsed = minidom.parseString(rough_string)
		return reparsed.toprettyxml(indent=" ")
	except xml.parsers.expat.ExpatError:
		return str(tostring(elem))
		


exportFormat = ""

if (len(sys.argv) > 2):
	if (sys.argv[2] == "-t"):
		print("export txt")
		exportFormat = "txt"
	elif (sys.argv[2] == "-x"):
		print("export xml")
		exportFormat = "xml"
	else:
		raise Exception("Erreur parametre non reconnus (" + str(sys.argv[2]) + ")")
		exit(1)
else:
	raise Exception("Pas assez de parametre fournis")
	exit(1)


# Dictionnaire data
data = {'fileName' : "",
		'abstract' : "",
		'title' : "",
		'author' : "",
		'biblio' : ""		
		}

# Convert pdf
os.system("pdftotext -nopgbrk "+sys.argv[1])
pdf = open(os.path.splitext(sys.argv[1])[0]+'.txt',"r",encoding='utf-8')
lines = pdf.readlines()

#genereration template xml
root = Element('opml')
root.set('version','1.0')
head = SubElement(root, 'article')
preamble = SubElement(head, 'preamble')
title = SubElement(head, 'title')
auteur = SubElement(head, 'auteur')
abstract = SubElement(head, 'abstract')
biblio = SubElement(head, 'biblio')
#print (prettify(root))
# recuperer le pdf source
if(exportFormat == "txt"):
	sortie = open(sys.argv[1]+"_parser.txt","w")  # delete le dernier fichier si il existe
else:
	sortie = open(sys.argv[1]+"_parser.xml","w")  # delete le dernier fichier si il existe
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
		data['title'] = doc.info[0]['Title'].decode("utf-16")
	except UnicodeDecodeError:
		#sortie.write(str(doc.info[0]['Title']))
		data['title'] = str(doc.info[0]['Title'])
else:
	#sortie.write(lines[0].strip()+'\n')
	data['title'] = lines[0].strip()+'\n'






# recuperer l'abstract
#sortie.write("<auteur>")

copy = False
cpt = 0
abstractStart = False
for line in lines:
	if str("Abstract\n") in line:
		copy = True
		abstractStart = True
	elif str("ABSTRACT\n") in line:
		copy = True
		abstractStart = True
	elif (cpt > 0 and abstractStart == False):
		data["author"] = data["author"]+line.strip()
	elif str("1\n") in line:
		copy = False
	elif str("I.\n") in line:
		copy = False
	elif str("1.\n") in line:
		copy = False
	elif copy:
		#sortie.write(line.strip())
		data['abstract'] = data['abstract']+str(line.strip())
	cpt += 1

copy = False
for line in lines:
	if str("References\n") in line:
		copy = True
	elif copy:
		data['biblio']=data['biblio']+line.strip()
if exportFormat == "txt":
	sortie.write("Preamble : ")
	sortie.write(data['fileName']+"\n")
	sortie.write("Title : ")
	sortie.write(data['title']+"\n")
	sortie.write("Auteur : ")
	sortie.write(data['author']+"\n")
	sortie.write("Abstract : ")
	sortie.write(data['abstract']+"\n")
	sortie.write("Biblio : ")
	sortie.write(data['biblio']+"\n")
else:
	preamble.text=data['fileName']
	title.text=data['title']
	auteur.text=data["author"]
	abstract.text=data['abstract']
	biblio.text=data["biblio"]
	sortie.write(prettify(root))
	
	


sortie.close()
pdf.close()


