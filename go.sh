#!/bin/sh


input="2011-GI.pdf"
tempDir="temp"

echo "==>Input file: $input"
mkdir -p $tempDir

# echo "==>Exporting to image (low res)..."
# convert -density 50 $input $tempDir/lr.jpg

echo "==>Exporting to image (high res)..."
convert -density 200 $input $tempDir/hr.jpg
# pdftoppm -png -l 1 2011-GI.pdf > a.png

echo "==>Analyzing each page..."
nbPages=$(ls -1 $tempDir/hr-*.jpg | wc -l)
for page in $tempDir/hr-*.jpg
do
	python decol.py $page
	echo "==>Page $page /$nbPages"
done

echo "==>Creating epub"
#https://github.com/rupeshk/web2epub
python web2epub.py -t dada -a dudu -c aaa.gif -o dada.epub temp/*.html

echo "==>Done!"
