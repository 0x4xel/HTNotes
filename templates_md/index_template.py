
def get_index_template():
    return '''---
tags:
  - tag1 
  - tag2
---

*This is the structure of the machine folder*
```dataview
list
WHERE contains(file.folder, this.file.folder)
```


## Workflow machine
```mermaid
flowchart TB
        A["10.10.10.X"] -- 80 --> B["Web"]
        A -- 22 --> C["FTP"]
		A -- 445,139 --> D["SMB"]
		D --> K["creds.txt"]
		B  --> E["Wordpress"]
		E --> J["Admin Pane"]
		K --> J
		J --> F["RCE CVE-X-X"]
		F --> G["www-data"]
		G --> H["gtfobins nmap"]
		H --> I["root"]

  
```
## Skills Acquired

- Text
- Text

## Tools used

- https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS
- https://github.com/carlospolop/PEASS-ng/tree/master/winPEAS
- https://sqlmap.org/
- ...

'''
    