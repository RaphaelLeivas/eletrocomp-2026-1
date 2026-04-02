folder_name=${PWD##*/}

pdflatex $folder_name.tex
bibtex $folder_name.aux
pdflatex $folder_name.tex
pdflatex $folder_name.tex
rm *.aux *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz *.bbl *.blg