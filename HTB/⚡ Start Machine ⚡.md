
## Script Workflow  for  - Create Machine Note

*This is simple button that will automate the creation of starting notes that will improve your quality of pwn. Just click on it and select the name of the machine you would like to compromise.*

```mermaid
flowchart TB
        A["Button Action"] -- machine_name --> J["API Request"]
        J -- Not found --> N["Exit"]
	    J -- Found Machine --> B["Search folder name"]
        B -- Found --> E["Just update the machine info"]
        B -- Not Found --> C["Create folder structure"]
         C --> L["assets"]
        C --> F["00-index"]
        C --> G["01-recon"]
        C --> H["02-exploitation"]
        C --> I["03-post-exploitation"]
        C -- HTB API request --> K["Create Machine file info"]
  
```


```button
name Create Machine Note
type link
action obsidian://shell-commands/?vault=HTB&execute=m6e17y5rts
templater true
color blue
```


---------------------

## Script Workflow  for  - Update Machines info
*As you can see in the diagram below, you can update the machine info of all the machines that has its folder name under /Machines folder*

```mermaid
flowchart TB
        A["Button Action"] --> B["Search Markdown fileClass Machine"]
        B --> C["HTB API conn with file name as param"]
        C --> D["Create new file with updated attributes"]
		D --> C
        
	
```


```button
name Update Machines info
type link
action obsidian://shell-commands/?vault=HTB&execute=usnoddh2no
templater true
color blue
Custom Class custom-buttom
```





