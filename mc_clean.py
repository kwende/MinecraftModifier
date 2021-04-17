import os
import zipfile
import sys
import shutil

zip_file = ""
if(len(sys.argv) == 2):
    zip_file = sys.argv[0]
else:
    zip_file = "C:\\Users\\ben\\Desktop\\forge-1.16.5-36.1.0-mdk.zip"

dir = os.path.join(os.path.dirname(zip_file), 'minecraft_forge_dir')

if os.path.exists(dir):
    shutil.rmtree(dir, ignore_errors=True)
else:
    os.makedirs(dir)

print(f"Unzipping {zip_file} to {dir}")

with zipfile.ZipFile(zip_file, 'r') as z:
    z.extractall(dir)

gradle_path = os.path.join(dir, 'build.gradle')
gradle_path_modified = os.path.join(dir, 'build.gradle2')
toml_file = os.path.join(dir, 'src\\main\\resources\\META-INF\\mods.toml')
toml_file_modified = os.path.join(dir, 'src\\main\\resources\\META-INF\\mods.toml2')

group_name_template = 'com.yourname.modid'
example_mod_template = 'examplemod'
vendor_template = 'examplemodsareus'
mod_id_template = 'modid'

group_name = input(f"group name ({group_name_template}): ")
mod_name = input(f"mod name ({example_mod_template}): ")
vendor_name = input(f"vendor ({vendor_template}):")
display_name = input(f"Display name: (Example Mod)")
mod_id = group_name[group_name.rfind('.')+1:]

if os.path.exists(gradle_path):
    with open(gradle_path_modified, 'w') as fout:
        with open(gradle_path) as fin:
            lines = fin.readlines()
            for line in lines:
                new_line = line.replace(group_name_template, group_name).replace(vendor_template, vendor_name).replace(example_mod_template, mod_name).replace(mod_id_template, mod_id)
                fout.write(new_line)

if os.path.exists(toml_file):
    with open(toml_file_modified, 'w') as fout:
        with open(toml_file) as fin:
            lines = fin.readlines()
            for line in lines:
                new_line = line
                if line.startswith("modId="):
                    new_line = f'modId="{mod_id}" #mandatory'
                elif line.startswith("displayName="):
                    new_line = f'displayName="{display_name}" #mandatory'
                if "examplemod" in line:
                    new_line = line.replace("examplemod", mod_name)
                fout.write(new_line)

os.remove(gradle_path)
os.rename(gradle_path_modified, gradle_path)

os.remove(toml_file)
os.rename(toml_file_modified, toml_file)