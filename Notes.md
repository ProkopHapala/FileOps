
Zasadni je vyhledavani

- udelat .md prohlizec ktery uklada .md soubory ruzne na disku, ale drzi si jejich kopii (databazi) nekde jinde synchronizovanou (napr. v Dropboxu). Hlavni je v nich rychle vyhledavat.

- udelat univerzalni databazovaci program ve kterem si ulozi "profil" nebo "workplace" pro ruzne typy souboru / topicky / workplaces

- Solution of problem of multiple links - kategorize files according to different categoriess

# Browse Noter

## C++ code analysis
 - Search all Clas and Function names in file or in project
   - load file as long string or memview (ignore linebreaks `\n` )
   - go over chars, split to words ` \t\n` and track scope level `{}`
   - for each token in `level=0` check if it is keyword or some other name, take first non-keyword identifier
      - it is known that in `level=0` can be only 1) global variables 2) functions 3) classes
        - class can be distinguised easily (it it preceded by `class` keyword)
        - function is followed by `(`
            - function names can be split by `::` from classes
        - for methods and variables of a class we can do recursively the same

# Markdown

### References
 - Markdown in python (but needs python3) -  https://github.com/retext-project/retext (see recomandation https://softwarerecs.stackexchange.com/questions/17714/simple-markdown-viewer-for-ubuntu )


