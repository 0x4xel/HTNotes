
def get_index_template():
    return '''This is the structure of the machine folder
```dataview
list
WHERE contains(file.folder, this.file.folder)
```
'''
    