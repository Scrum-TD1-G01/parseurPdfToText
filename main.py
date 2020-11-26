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
sortie.write("Abstract : \n")
abstractDone = False

copy = False
for line in lines:

        if(abstractDone!=True):
                if str("Abstract\n") in line:
                        copy = True
                elif str("ABSTRACT\n") in line:
                        copy = True
                elif str("1\n") in line:
                        copy = False
                        abstractDone = True
                elif str("I.\n") in line:
                        copy = False
                        abstractDone = True
                elif str("1.\n") in line:
                        copy = False
                        abstractDone = True
                elif copy:
                        sortie.write(line.strip())
        elif (abstractDone):
                if str("References\n") in line:
                        copy = True
                        sortie.write("\n")
                        sortie.write("References : \n")
                elif copy:
                        sortie.write(line.strip())

sortie.write('\n')
sortie.close()
pdf.close()


