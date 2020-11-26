for i in `ls ./testRessources/*.pdf`
do
	python3 ./main.py $i
done
