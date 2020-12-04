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
		

# Verification des arguments
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

copied = []


# Menu de selection
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
print("Chemin du document :", fileToParse)


# Convert pdf
os.system("pdftotext -nopgbrk -raw "+fileToParse)
#os.system("pdftotext -nopgbrk "+fileToParse)
pdf = open(os.path.splitext(fileToParse)[0]+'.txt',"r")
lines = pdf.readlines()

# genereration template xml
root = Element('opml')
root.set('version','1.0')
head = SubElement(root, 'article')
preamble = SubElement(head, 'preamble')
title = SubElement(head, 'title')
auteur = SubElement(head, 'auteur')
abstract = SubElement(head, 'abstract')
introduction = SubElement(head, 'introduction')
conclusion = SubElement(head, 'conclusion')
discusion = SubElement(head, 'discussion')
biblio = SubElement(head, 'biblio')
#print (prettify(root))
# recuperer le pdf source
if(exportFormat == "txt"):
	sortie = open(fileToParse+"_parser.txt","w")  # delete le dernier fichier si il existe
else:
	sortie = open(fileToParse+"_parser.xml","w")  # delete le dernier fichier si il existe



# recuperer les metadata (titre + auteur))
raw_pdf = open(fileToParse,'rb')#recuperer le pdf raw pour extract les metadata
parser = PDFParser(raw_pdf)
doc = PDFDocument(parser)#cast le PDF en doc dans notre code


if(doc.info[0] and doc.info[0]['Title']):
	try:
		data['title'] = doc.info[0]['Title'].decode("utf-16")
	except UnicodeDecodeError:
		data['title'] = str(doc.info[0]['Title'])
else:
	data['title'] = lines[0].strip()+'\n'


# authorinhtml = False  -> pas 'Author' dans copied
try:
	if(doc.info[0]['Author']):
		copied.append('auteur')  # authorinhtml = True
		try:
			data['author'] = doc.info[0]['Author'].decode("utf-16")
		except UnicodeDecodeError:
			data['author'] = str(doc.info[0]['Author'])
except:
	a = 0  # do nothing


# Récupération des données

copy = ''  # La section en cours de copie ('' : aucune)
# copied = [] (voir début du programme)
cpt = 0
for line in lines:
	# Abstract
	if reg.match(r'^.{0,5}abstract(s)?.{0,100}\n', line.lower()) and not 'abstract' in copied:
		print(line)
		copy = 'abstract'
		copied.append(copy)
	# Introduction
	elif reg.match(r'^.{0,5}introduction(s)?.{0,3}\n', line.lower()) and not 'introduction' in copied:
		print("tat")
		copy = 'introduction'
		copied.append(copy)
	# Fin Abstract
	#elif str("1.\n") in line or str("I.\n") in line or str("1.\n") in line:
	elif 'abstract' in copied and reg.match(r'^[1|I].{0,40}+\n', line) and not 'introduction' in copied :
		print(line)
		copy = ''
	# Fin Introduction
	elif reg.match(r'^2[\.|\ .+|\n]', line.lower()):
		copy = ''
	# Conclusion
	elif ( reg.match(r'^.{0,10}Conclusion(s)?.{0,40}\n', line) or reg.match(r'^.{0,10}CONCLUSION(S)?.{0,40}\n', line) ) and not 'conclusion' in copied:  # 'summary' pose problème
		copy = 'conclusion'
		copied.append(copy)
	# Fin FACULTATIVE
	#elif reg.match(r'^.{0,5}acknowledg(e)?ment(s)?', line.lower()):
		#copy = ''
	# Références bibliographiques (et = fin discussion)

	#elif reg.match(r'^.{0,5}Reference(s)?.{0,3}\n', line) or reg.match(r'^.{0,5}REFERENCE(S)?.{0,3}\n', line): # and not 'biblio' in copied (On prends le dernier match)  # !!! {1,..}
		#data['biblio'] = ""  # On garde seulement le dernier match ! (voir pdf Gonzalez)
		#copy = 'biblio'
		#copied.append(copy)
	# Références bibliographiques (et = fin discussion)
	elif ( reg.match(r'^.{0,5}Reference(s)?.{0,3}\n', line) or reg.match(r'^.{0,5}REFERENCE(S)?.{0,3}\n', line) ) and not 'biblio' in copied:
		copy = 'biblio'
		copied.append(copy)
	# Discussion
	elif ( reg.match(r'^.{0,3}Discussion(s)?.{0,40}\n', line) or reg.match(r'^.{0,3}DISCUSSION(S)?.{0,40}\n', line) ) and not 'discussion' in copied:  # !!! {..,3}
		copy = 'discussion'
		copied.append(copy)
	# Auteurs
	if cpt > 0 and cpt < 200 and copy == '' and not line.strip() in data['title'] and (copy == 'author' or not 'author' in copied):
		# not line.strip() data['title'] : si on est pas encore dans le titre
		if cpt == 1:
			print(line.strip())
		data['author'] = data['author']+line.strip()
		copy = 'author'
		copied.append('author')
	# Copie de bilio jusqu'à la fin du document (dernier element du doc : on en sort plus)
	if 'biblio' in copied:
		copy = 'biblio'
	if copy != '':
		data[copy] = data[copy]+str(line.strip())
	cpt += 1

# Export txt ou xml
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
	auteur.text=data['author']
	abstract.text=data['abstract']
	introduction.text=data['introduction']
	conclusion.text=data['conclusion']
	discusion.text=data['discussion']
	biblio.text=data['biblio']
	sortie.write(prettify(root))
	
	


sortie.close()
pdf.close()


