# eletrocomp-2026-1
Repositório para códigos da disciplina Eletromagnetismo Computacional 2026/1 PPGEE UFMG

# Procedimento para compilar os LaTeX localmente

## Configuração de ambiente

- Vá em https://www.latex-project.org/get/ 
- Clique em MikTex, na seção Windows, indo para https://miktex.org/download
- Faça download do MikTex para Windows 
- Salve em C:\Users\Usuario_01\AppData\Local\Programs\MiKTeX
- Instale a extensão LaTeX workshop no VS Code
- Instale o strawberry-perl-5.32.1.1-64bit.msi a partir de https://strawberryperl.com/
- Após a instalaçao, verifique o `perl` com
```
perl -v
```
Verifique o `PATH` do Windows caso não reconheça.
Talvez seja necessario fechar o VS Code e abrir de novo para o terminal integrado dele reconhecer o `perl`.
- Desative a extensão vscode-pdf para nao conflitar com a do latex.
- Rode o comando build com `ctrl + alt + B` (ou clica no icone verda da extensão no VS Code)
- Instale os packages que a extensão pedir que estão faltando.
- Nao deixe mostrar o dialog toda vez para cada instalação, deixe instalar todos packages de uma vez conforme a extensão precisar.
- Teste o PDF

- Usado a configuração `latex-workshop.latex.autoClean.run: OnBuilt` da extensão do VS Code que remove os arquivos auxiliares 
que são gerados após o build.


## Compilando localmente via CLI (sem o VS Code)

Compiling with BibTeX requires multiple steps (order matters):

    pdflatex main.tex

    bibtex main.aux

    pdflatex main.tex

    pdflatex main.tex

Ou cria um bash script para rodar isso automático.

Ou usa o VS que já faz tudo isso automático.