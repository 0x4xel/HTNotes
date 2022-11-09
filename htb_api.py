import os
import sys
import argparse
import datetime
import Constants

from hackthebox import HTBClient
from templates_md import get_machine_template, get_machine_template, get_index_template


# Params
parser = argparse.ArgumentParser(description='A test program.')
parser.add_argument("-m", "--machine_name", help="Input of the machine", default="",required=False)
parser.add_argument("-v", "--vault_path", help="Path of obsidian vault", default="",required=True)
args = parser.parse_args()



#TODO Modify this
machine_name = args.machine_name 
VAULT_PATH = args.vault_path
MACHINES_PATH = VAULT_PATH + "Machines/" + machine_name
MACHINE_PATH = MACHINES_PATH + "/"

client = HTBClient(app_token=Constants.API_TOKEN)

try:
    if machine_name == "":  #Recursively update of all machines
      folder = VAULT_PATH +"/Machines"
      sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
      for folder2 in sub_folders:
        
        os.system("/usr/bin/python3 " +  VAULT_PATH + "/../htb_api.py -m " + folder2 + ' -v "' + VAULT_PATH + '/"')
        print("Finish execution of update " + folder2 )    
      exit()
    else:
      machine_data = client.get_machine(machine_name)
except:
    print("Machine not found.")
    exit() 

try:    
    machine_tags = client.get_tags_machine(int(machine_data.id))
except:
    machine_tags = []

try:    
    matrix = client.get_matrix(int(machine_data.id))
except:
    matrix = []


try:    
    user_rating = client.get_user_rating(int(machine_data.id))
except:
    user_rating = []


time_today = datetime.datetime.now()



# Convert
if not machine_data.user_owned:
    user_owned = False
    machine_data.user_owned = False

if not machine_data.root_owned:
    root_owned = False
    machine_data.root_owned = False

if machine_data.user_owned:
    user_owned = "✅"
else:
    user_owned = "❌"

if machine_data.root_owned:
    root_owned = "✅"
else:
    root_owned = "❌"

if machine_data.active:
    active = "✅"
else:
    active = "❌"



author = matrix["maker"]
user_average = matrix["aggregate"]


#Call templates
machine_template = get_machine_template(VAULT_PATH,machine_data,active,user_owned,root_owned, time_today,user_average,author, user_rating, machine_tags)

#In case of first execution
if not os.path.exists(VAULT_PATH + "Machines/"):
    os.makedirs(VAULT_PATH + "Machines/")


# You can change me to define your folder structure
if not os.path.exists(MACHINES_PATH):
    os.makedirs(MACHINES_PATH)
    with open(os.path.join(MACHINE_PATH, "00-index.md"), 'w') as temp_file:
      temp_file.writelines(get_index_template())
      print("Created 00-index.md")
    with open(os.path.join(MACHINE_PATH, "01-recon.md"), 'w') as temp_file:
      print("Created 01-recon.md")
    with open(os.path.join(MACHINE_PATH, "02-exploitation.md"), 'w') as temp_file:
      print("Created 02-exploitation.md")
    with open(os.path.join(MACHINE_PATH, "03-post-exploitation.md"), 'w') as temp_file:
      print("Created 03-post-exploitation.md")



# Create the file info machine
with open(os.path.join(MACHINE_PATH, machine_name + ".md"), 'w') as temp_file:
    temp_file.writelines(machine_template)
    print("Created/Updated machine file ")


print("Exiting...")