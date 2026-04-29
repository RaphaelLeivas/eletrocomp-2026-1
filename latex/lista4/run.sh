folder_name=${PWD##*/}

pdflatex --interaction=nonstopmode $folder_name.tex | awk 'BEGIN{IGNORECASE = 1}/warning|!/,/^$/;'
bibtex $folder_name.aux
pdflatex --interaction=nonstopmode $folder_name.tex | awk 'BEGIN{IGNORECASE = 1}/warning|!/,/^$/;'
pdflatex --interaction=nonstopmode $folder_name.tex | awk 'BEGIN{IGNORECASE = 1}/warning|!/,/^$/;'
rm *.aux *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz *.bbl *.blg