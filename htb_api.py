import os
import sys
import argparse
import Constants

from hackthebox import HTBClient
from templates_md import get_machine_template, get_machine_template, get_index_template, get_recon_template, get_exploitation_template, get_post_exploitation_template

# Params
parser = argparse.ArgumentParser(description='A test program.')
parser.add_argument("-m", "--machine_name", help="Input of the machine", default="",required=False)
parser.add_argument("-v", "--vault_path", help="Path of obsidian vault", default="",required=True)
args = parser.parse_args()


machine_name = args.machine_name 
VAULT_PATH = args.vault_path

client = HTBClient(app_token=Constants.API_TOKEN)
try:
    if machine_name == "":  #Recursively update of all machines
        folder = VAULT_PATH + "Machines"
        sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
        for sub_folder in sub_folders:
            os.system("/usr/bin/python3 " +  VAULT_PATH + "../htb_api.py -m " + sub_folder + ' -v "' + VAULT_PATH + '"')
            print("Finished execution of update " + sub_folder )    
        exit()
    else:
        machine_data = client.get_machine(machine_name)
except:
    if machine_name != "": #Checks only if machine_name does not exist 
        print(f"{machine_name} not found.")
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


author = matrix["maker"]
user_average = matrix["aggregate"]
MACHINE_FOLDER_PATH = VAULT_PATH + "Machines/" + machine_data.name 

#Call templates
machine_template = get_machine_template(VAULT_PATH,machine_data,user_average,author, user_rating, machine_tags)

#In case of first execution, create Machine Folder
if not os.path.exists(VAULT_PATH + "Machines/"):
    os.makedirs(VAULT_PATH + "Machines/")


# You can change me to define your folder structure
if not os.path.exists(MACHINE_FOLDER_PATH):
    os.makedirs(MACHINE_FOLDER_PATH)
    print("Created machine root folder")
    if not os.path.exists(MACHINE_FOLDER_PATH + "/assets"):
        os.makedirs(MACHINE_FOLDER_PATH + "/assets")
        print(("Created assets folder"))
    with open(os.path.join(MACHINE_FOLDER_PATH, "00-index.md"), 'w') as temp_file:
      temp_file.writelines(get_index_template())
      print("Created 00-index.md")
    with open(os.path.join(MACHINE_FOLDER_PATH, "01-recon.md"), 'w') as temp_file:
        temp_file.writelines(get_recon_template())
        print("Created 01-recon.md")
    with open(os.path.join(MACHINE_FOLDER_PATH, "02-exploitation.md"), 'w') as temp_file:
        temp_file.writelines(get_exploitation_template())
        print("Created 02-exploitation.md")
    with open(os.path.join(MACHINE_FOLDER_PATH, "03-post-exploitation.md"), 'w') as temp_file:
        temp_file.writelines(get_post_exploitation_template())
        print("Created 03-post-exploitation.md")


# Create the file info machine
with open(os.path.join(MACHINE_FOLDER_PATH, machine_data.name + ".md"), 'w') as temp_file:
    temp_file.writelines(machine_template)
    print("Created/Updated machine file ")


print("Exiting...")