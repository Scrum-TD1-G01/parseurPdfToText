# parseurPdfToText

## V3 : Capable de récupérer : nom du fichier d'origine, titre, auteurs, abstract, biblio

### Format Texte

Pour exporter en format Texte:  `python3 ./main.py -t dirPath`

Avec _dirPath_ le chemin vers un dossier contenant des pdf.

**Exemple :** `python3 ./main.py -t ./testRessources`

### Format XML 

Pour exporter en format XML:  `python3 -x ./main.py dirPath`

Avec _dirPath_ le chemin vers un dossier contenant des pdf.

**Exemple :** `python3 ./main.py -x ./testRessources`

### Resultat 

il se trouve dans le dossier du fichier d'origine et est nommé _pdfFilePath_parser.txt_

**Exemple :** `cat ./testRessources/Boudin-Torres-2006.pdf_parser.txt`


### Pour tester tout les pdf de ./testRessources d'un coup (XML)

`./testAll.sh`
