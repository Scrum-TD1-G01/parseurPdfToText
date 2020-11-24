import pdftotext
import sys

# Load your PDF
with open("./testRessources/Boudin-Torres-2006.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)

# How many pages?
print(len(pdf))

#recuperer le pdf source
pdfsource = open(sys.argv[1],"r")
sortie = open(sys.argv[1]+"_parser.txt","w")#delete le dernier fichier si il existe
sortie.write("Fichier Original: \n"+"    "+sys.argv[1])
# Iterate over all the pages
for page in pdf:
    print(page)

# Read some individual pages
print(pdf[0])
print(pdf[1])

# Read all the text into one string
print("\n\n".join(pdf))
