import pdftotext
import sys
import unicodedata
import os
import glob
import regex as reg
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
	if (sys.argv[1] == "-t"):
		print("export txt")
		exportFormat = "txt"
	elif (sys.argv[1] == "-x"):
		print("export xml")
		exportFormat = "xml"
	else:
		raise Exception("Erreur parametre non reconnus (" + str(sys.argv[1]) + ")")
		exit(1)
else:
	raise Exception("Pas assez de parametre fournis")
	exit(1)


# Dictionnaire data
data = {'fileName' : "",
		'abstract' : "",
		'title' : "",
		'author' : "",
		'biblio' : "",
		'discussion' : "",
		'conclusion' : "",
		'introduction': ""
	}


dirPath = sys.argv[2]
print(dirPath)
if os.path.isdir(dirPath):
	fileList = glob.glob(dirPath+'**.pdf')
	fileListKey = []
	fileListDic = {}
	for i in fileList:
		fileListKey.append(os.path.basename(i))
		fileListDic[fileListKey[-1]] = i
	
	for i in range(len(fileListDic)):
		print(str(i)+" :", fileListKey[i])
else:
	raise Exception("Le dossier (" + dirPath + ") n'existe pas")
resFileToParse = int(input("Saisir le numero du pdf a parser : "))
data['fileName'] = fileListKey[resFileToParse]
print("Parsing du document :", fileListKey[resFileToParse])
fileToParse = fileListDic[fileListKey[resFileToParse]]
print("Adresse du document :", fileToParse)


# Convert pdf
os.system("pdftotext -nopgbrk "+fileToParse)
pdf = open(os.path.splitext(fileToParse)[0]+'.txt',"r")
lines = pdf.readlines()

#genereration template xml
root = Element('opml')
root.set('version','1.0')
head = SubElement(root, 'article')
preamble = SubElement(head, 'preamble')
title = SubElement(head, 'title')
auteur = SubElement(head, 'auteur')
abstract = SubElement(head, 'abstract')
introduction = SubElement(head, 'introduction')
conclusion = SubElement(head, 'conclusion')
biblio = SubElement(head, 'biblio')
#print (prettify(root))
# recuperer le pdf source
if(exportFormat == "txt"):
	sortie = open(fileToParse+"_parser.txt","w")  # delete le dernier fichier si il existe
else:
	sortie = open(fileToParse+"_parser.xml","w")  # delete le dernier fichier si il existe



#recuperer les metadata et title
raw_pdf = open(fileToParse,'rb')#recuperer le pdf raw pour extract les metadata
parser = PDFParser(raw_pdf)
doc = PDFDocument(parser)#cast le PDF en doc dans notre code
#sortie.write("Title: \n")
authorinhtml = False
if(doc.info[0] and doc.info[0]['Title']):
	try:
		#sortie.write(doc.info[0]['Title'].decode("utf-16"))
		data['title'] = doc.info[0]['Title'].decode("utf-16")
	except UnicodeDecodeError:
		#sortie.write(str(doc.info[0]['Title']))
		data['title'] = str(doc.info[0]['Title'])
else:
	#sortie.write(lines[0].strip()+'\n')
	data['title'] = lines[0].strip()+'\n'

if(doc.info[0]['Author']):
	authorinhtml = False
	try:
		#sortie.write(doc.info[0]['Title'].decode("utf-16"))
		data['auteur'] = doc.info[0]['Author'].decode("utf-16")
	except UnicodeDecodeError:
		#sortie.write(str(doc.info[0]['Title']))
		data['auteur'] = str(doc.info[0]['Author'])
else:
	#sortie.write(lines[0].strip()+'\n')
	data['auteur'] = lines[0].strip()+'\n'







# recuperer l'abstract
#sortie.write("<auteur>")

copy = False
cpt = 0
abstractStart = False
introStart = False
conclusionStart = False
referenceStart =  False
for line in lines:
	'''
	if str("Abstract\n") in line:
		copy = True
		abstractStart = True
	elif str("ABSTRACT\n") in line:
		copy = True
		abstractStart = True
	'''
	if reg.match(r'^.{0,5}abstract[\.|\ |\n]', line.lower()):
		print(line)
		copy = True
		abstractStart = True
	elif str("1\n") in line:
		copy = False
	elif str("I.\n") in line:
		copy = False
	elif str("1.\n") in line:
		copy = False
	elif reg.match(r'^.{0,5}introduction[\.|\ |\n]', line.lower()):
		copy = False
		introStart = True
	elif str("2\n") in line:
		introStart = False
	elif reg.match(r'^.{0,5}conclusion[\.|\ |\n]', line.lower()):
		conclusionStart = True
	elif reg.match(r'^.{0,5}reference(s)[\.|\ |\n]', line.lower()):
		referenceStart = True
	elif (cpt > 0 and abstractStart == False and authorinhtml == False):
		data["author"] = data["author"]+line.strip()
	if copy:
		#sortie.write(line.strip())
		data['abstract'] = data['abstract']+str(line.strip())
	if introStart:
		data['introduction'] = data['introduction']+str(line.strip())
	if conclusionStart:
		data['conclusion']=data['conclusion']+line.strip()
	if referenceStart:
		data['biblio']=data['biblio']+line.strip()
	cpt += 1

copy = False
discussion = False
for line in lines:
	if str("Discussion\n" or "DISCUSSION\n") in line:
		discussion = True
	elif str("Conclusion\n" or "Conclusions\n" or "CONCLUSIONS\n" or "CONCLUSION\n") in line:
		copy = True
		discussion = False
	elif str("References\n") in line:
		copy = False
		discussion = False
	elif str("Appendix") in line :
		discussion = False
	elif discussion:
		data['discussion']=data['discussion']+line.strip()
	elif copy:
		data['conclusion']=data['conclusion']+line.strip()

if exportFormat == "txt":
	sortie.write("Preamble : ")
	sortie.write(data['fileName']+"\n")
	sortie.write("Title : ")
	sortie.write(data['title']+"\n")
	sortie.write("Auteur : ")
	sortie.write(data['author']+"\n")
	sortie.write("Abstract : ")
	sortie.write(data['abstract']+"\n")
	sortie.write("Introduction : ")
	sortie.write(data['introduction']+"\n")
	sortie.write("Conclusion : ")
	sortie.write(data['conclusion']+"\n")
	sortie.write("Discussion : ")
	sortie.write(data['discussion']+"\n")
	sortie.write("Biblio : ")
	sortie.write(data['biblio']+"\n")
else:
	preamble.text=data['fileName']
	title.text=data['title']
	auteur.text=data["author"]
	abstract.text=data['abstract']
	introduction.text=data['introduction']
	conclusion.text=data["conclusion"]
	biblio.text=data["biblio"]
	sortie.write(prettify(root))
	
	


sortie.close()
pdf.close()


