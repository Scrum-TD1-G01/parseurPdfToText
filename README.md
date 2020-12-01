# parseurPdfToText

## V1 : Capable de récupérer le titre, l'abstract et le nom du fichier d'origine

### Format Texte

Pour exporter en format Texte:  `python3 ./main.py pdf_file_path -t`

Avec _pdfFilePath_ le chemin vers un pdf.

**Exemple :** `python3 ./main.py ./testRessources/Boudin-Torres-2006.pdf -t`

### Format XML 

Pour exporter en format XML:  `python3 ./main.py pdf_file_path -x`

Avec _pdfFilePath_ le chemin vers un pdf.

**Exemple :** `python3 ./main.py ./testRessources/Boudin-Torres-2006.pdf -x`

### Resultat 

il se trouve dans le dossier du fichier d'origine et est nommé _pdfFilePath_parser.txt_

**Exemple :** `cat ./testRessources/Boudin-Torres-2006.pdf_parser.txt`

