
*Your vault summary has the following instances*

## Machines in vault

```dataviewjs
const {fieldModifier: f} = this.app.plugins.plugins["metadata-menu"].api;
const vault_path = this.app.vault.adapter.basePath
dv.table(['Name', 'Avatar','Difficulty','Stars','OS'],
	dv.pages("#machine")
		.filter(p => p.file.path.includes("Machine"))
		.filter(p => !p.file.path.includes("fileClass"))
		.filter(p => !p.file.path.includes("templates"))
		.map(p => [
		p.file.link,
		'<img style="max-width:70px" src="https://www.hackthebox.com/'+p.avatar+'">',
		f(dv,p,"difficulty_text"),
		'<p> ⭐️ '+ p.stars+'</p>',
		'<img style = "max-width:30px" src = "app://local//'+vault_path+'/.res/'+ p.os +'.png">'
		
		]).sort(b => b.created )
		)
```

----------------------

## Machines in vault with USER but not ROOT


```dataviewjs
const {fieldModifier: f} = this.app.plugins.plugins["metadata-menu"].api;

dv.table(['Name', 'Avatar','Difficulty','Stars','OS'],
	dv.pages("#machine")
		.filter(p => p.file.path.includes("Machine"))
		.filter(p => !p.file.path.includes("fileClass"))
		.filter(p => !p.file.path.includes("templates"))
		.filter(p => !p.root_flag)
		.filter(p => p.user_flag)
		.map(p => [
		p.file.link,
		'<img style="max-width:70px" src="https://www.hackthebox.com/'+p.avatar+'">',
		f(dv,p,"difficulty_text"),
		'<p> ⭐️ '+ p.stars+'</p>',
		'<img style = "max-width:30px" src = "app://local//home/axel/Escritorio/HTNotes/HTB/.res/'+ p.os +'.png">'
		
		]).sort(b => b.created )
		)
```

-------------------

## Machines in vault without USER and ROOT

```dataviewjs
const {fieldModifier: f} = this.app.plugins.plugins["metadata-menu"].api;

dv.table(['Name', 'Avatar','Difficulty','Stars','OS'],
	dv.pages("#machine")
		.filter(p => p.file.path.includes("Machine"))
		.filter(p => !p.file.path.includes("fileClass"))
		.filter(p => !p.file.path.includes("templates"))
		.filter(p => !p.root_flag)
		.filter(p => !p.user_flag)
		.map(p => [
		p.file.link,
		'<img style="max-width:70px" src="https://www.hackthebox.com/'+p.avatar+'">',
		f(dv,p,"difficulty_text"),
		'<p> ⭐️ '+ p.stars+'</p>',
		'<img style = "max-width:30px" src = "app://local//home/axel/Escritorio/HTNotes/HTB/.res/'+ p.os +'.png">'
		
		]).sort(b => b.created )
		)
```
