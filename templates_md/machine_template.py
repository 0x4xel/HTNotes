from templates_md import get_template_char_user_rating, get_template_chart_radar
import datetime




def get_machine_template(VAULT_PATH,machine_data,user_average,author,user_rating,machine_tags):

    if machine_data.user_owned:
        user_owned = "✅"
    else:
        user_owned = "❌"
        machine_data.user_owned = False

    if machine_data.root_owned:
        root_owned = "✅"
    else:
        root_owned = "❌"
        machine_data.root_owned = False

    if machine_data.active:
        active = "✅"
    else:
        active = "❌"
    
    
    time_today = datetime.datetime.now()
    string_tags = ""
    for tag in machine_tags:
        tag_with_no_spaces = tag["name"].replace(" ", "_")
        string_tags = string_tags + "#" + tag_with_no_spaces + " "
    return f'''
---
fileClass: Machine
---

<p align="center"> <img src= "https://www.hackthebox.com/{machine_data.avatar}"> </p>

#machine

## Operation system - {machine_data.os}
<img style = "max-width:70px" src = "app://local/{VAULT_PATH}.res/{machine_data.os}.png">

## Metadata

|                       |   |
| ----------------      | - |
| ID                    |{machine_data.id} |
| Name                  |{machine_data.name} |
| Active                |{active}  |
| User Flag             |{user_owned} |
| Root Flag             |{root_owned}|
| Difficulty Text       |{machine_data.difficulty}  |
| Stars                 |⭐️ {machine_data.stars} |
| Created Note          |{time_today.strftime("%m/%d/%y")} |
| Published             |{machine_data.release_date.strftime("%m/%d/%y")} |
| tags                  |{string_tags} |

<p style = "display:none">
id:: {machine_data.id}
active:: {machine_data.active}
name:: {machine_data.name}
os::{machine_data.os}
user_flag:: {machine_data.user_owned}
root_flag:: {machine_data.root_owned}
difficulty_text:: {machine_data.difficulty}
stars:: {machine_data.stars}
created:: {time_today.strftime("%m/%d/%Y")}
published:: {machine_data.release_date.strftime("%m/%d/%y")}
avatar:: {machine_data.avatar}
tags:: {string_tags}
</p>

## Statistics

{get_template_chart_radar(user_average, author)}


### User rating

{get_template_char_user_rating(user_rating)}


```button
name Update this Machine info
type link
action obsidian://shell-commands/?vault=HTB&execute=g7sm2q030y
templater true
```

'''
