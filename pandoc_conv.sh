# in ART125/md
cd md

# run pandoc on all files with a .md suffix, creating a file with a .md.txt suffix. 
find . -name \*.txt -type f -exec pandoc -f markdown -t html -o {}.html {} \;
find . -name \*.txt -type f -exec pandoc -f markdown -t docx -o {}.docx {} \;


# move new files to ART125/units and ART125/word
find . -name "*.txt.html" -exec mv {} ../units \;
find . -name "*.txt.docx" -exec mv {} ../word_files \;

# and remove .txt from the name
cd ../units
for file in *.txt.html ; do mv $file `echo $file | sed 's/\(.*\.\)txt.html/\1html/'` ; done


cd ../word_files
for file in *.txt.docx ; do mv $file `echo $file | sed 's/\(.*\.\)txt.docx/\1docx/'` ; done