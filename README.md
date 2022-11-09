# HTNotes


HTNotes is a powerfull automatic tool that integrates a Vault Workspace in `Obsidian`. It can automate the first steps of taking Notes in a HTB Machine by generating a folder structure  given a machine name. It has also an integration with the HTB API that makes requests and print the info into markdown files.

This can be performed with just a click on obsidian button. 

## Table of Contents

- Content
- Setup
- Usage

## Content


## Setup

### Install obsidian
You need Obsidian to integrate the tool.

Open your browser and go to [Download Obsidian](https://obsidian.md/download).
Install .deb and execute the folowing command under Dowloads

```
sudo dpkg -i <<Obsidian.deb>>
```

### Clone the repo
Now you need to clone this repository and install all the dependencies.  

```
git clone https://github.com/0x4xel/HTNotes
cd HTNotes
pip install -r requirements.txt
```

### Get App token in Hackthebox

1. You have to login in [HackTheBox](https://www.hackthebox.com/). 
2.  Explore under View Profile -> Profile Settings -> App Tokens -> Generate App token
3.  Create a token that will be needed to make requests on HTB API.

### Put token in Constants.py

Put you API key in Constants.py file and save.

### Open you Vault folder

1. Open obsidian and select  *open existing vault
2. Select the folder HTB under HTNotes


## Usage


