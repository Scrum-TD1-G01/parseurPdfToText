import regex as reg
#import re as reg

# (\p{Lu}\p{L}+)(\-\p{L}+)?\ \p{Lu}\p{L}+(\-\p{L}+)?
# [A-Za-zÉé]+(\-?)[A-Za-zÉé]+\ [A-Za-zÉé]+(\-?)[A-Za-zÉé]+

def test1():
    with open("./CORPUS_TEST/Boudin-Torres-2006.txt", "r") as f:
        txt = f.read(400)
        print(txt)
        finding = reg.findall(r'[A-Za-z]+(\-?)[A-Za-z]+\ [A-Za-z]+(\-?)[A-Za-z]+', txt)
        for i in finding:
            print(i)

def test2():
    with open("./CORPUS_TEST/Boudin-Torres-2006.txt", "r") as f:
        txt = f.read(400)
        tokens = reg.findall(r'[A-Za-z\-]+', txt)

        for i in tokens:
            if (reg.fullmatch(r'[A-Za-z]+(\-?)[A-Za-z]+\ [A-Za-z]+(\-?)[A-Za-z]+', i)):
                print(i)


test2()
