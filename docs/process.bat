for %%f in (*.md) do c:\Apps\Python27\python.exe -m markdown -x markdown.extensions.fenced_code %%f -f %%~nf.html
