#!/usr/bin/env python3
import json
from typing import Dict
import sys
import os

import requests

try:
    # relative import only works when installed as a module
    from .mod import mod
except ImportError:
    # absolute import only works when run directly with python main.py
    from mod import mod


def get_page(url: str) -> str:
    """
    Retrieves the html content of a url
    @param url: URL to request
    @return: html content
    """
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Error retrieving webpage. Status code: {response.status_code}")
        return ""

def modrinth_get(mod_id: str, loader: str, mc_version: str) -> str:
    """
    Makes a GET to modrinth api to get the latest version of a mod
    @param mod_id: mod identifier used by modrinth
    @param loader: minecraft mod loader
    @param mc_version: minecraft version
    @return: GET response
    """
    params = {'loaders': "[\""+loader+"\"]", 'game_versions': "[\""+mc_version+"\"]"}
    response = requests.get(url=f'https://api.modrinth.com/v2/project/{mod_id}/version', params=params, timeout=10)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error retrieving webpage. Status code: {response.status_code}")
        return ""


def load_mods_list(path: str) -> Dict:
    """
    Loads JSON data into dictionary
    @param path: file path to the mod_list.json file
    @return: dictionary with the json content of mod_list.json
    """
    with open(path, 'r', encoding='utf8') as file:
        return json.load(file)

def save_mods_list(path: str, mod_list_data: dict):
    """
    Updates json file in path with new mod_list_data data
    @param path: path to save json file to
    @param mod_list_data: json object with new mod list data
    """
    with open(path, "w", encoding='utf8') as file:
        json.dump(mod_list_data, file, indent=2)

def modrinth_get_latest_mod(current_mod: mod, mc_version: str, loader: str) -> mod:
    """
    Get the latest version of a mod for a specific minecraft version
    @param id: path to the list of mod versions
    @param current_mod_version: current version name of the mod
    @param mc_version: minecraft version needed
    @param loader: mod loader to target
    """
    modrinth_data = modrinth_get(current_mod.name, loader, mc_version)
    for version in modrinth_data:
        if mc_version not in version["game_versions"]:
            continue
        if loader not in version["loaders"]:
            continue
        if version["version_number"] == current_mod.version:
            return current_mod
        else:
            return mod(current_mod.name, version["version_number"], version["files"][0]["url"])

    return current_mod

def update_jar(current_version: mod, latest_version: mod, jar_destination: str):
    """
    Remove old jar file and download new one
    @param current_version: mod class of the current version
    @param latest_version: mod class of the latest data for mod
    @param jar_destination: path to where to download jar to
    """
    old_jar = os.path.join(jar_destination,current_version.path)
    if ((current_version.url is not None) & (os.path.isfile(old_jar))):
        os.remove(os.path.join(jar_destination, current_version.path))
    file = requests.get(url=latest_version.url, stream=True, timeout=10)
    print("downloadind: "+latest_version.get_url_filename())
    open(os.path.join(jar_destination, latest_version.get_url_filename()), "wb").write(file.content)

def get_path_dir(path: str) -> str:
    """
    Return parent directory of a file
    @pre: path must end in a file or be empty, it cannot be a dir itself otherwise it will return the parent directory of the directory
    @param path: path to extract dir from
    @return the dir of a path
    """
    # if there is '/' then split and return empty string is path is empty
    return path.rsplit('/', 1)[0] if path.__contains__('/') else ""

def update_json(updated_mod: mod, json_data: dict) -> dict:
    """
    Update json file with new mod data
    @param updated_mod: mod with latest data
    @param json_data: mod list data
    @return updated json data
    """
    json_data["current_version"] = updated_mod.version
    json_data["file"] = os.path.dirname(json_data["file"]) + updated_mod.get_url_filename()
    return json_data

def get_mods_dir(path_to_modlist: str) -> str:
    """
    Return the directly to download mods
    @param path_to_modlist: relative path to mod_list_file
    @return path to download mods
    """
    # absolute paths
    if (os.path.isabs(path_to_modlist)):
        return os.path.dirname(path_to_modlist)
    # relative paths
    return os.path.dirname(path_to_modlist)

def main(argv: list[str] = sys.argv):
    print(
    "====================================================================================\n\n"+
    "                                ▄▄                                           ▄▄                  \n" +
    "▀████▄     ▄███▀              ▀███ ▀████▄     ▄███▀                        ▀███                  \n" +
    "  ████    ████                  ██   ████    ████                            ██                  \n" +
    "  █ ██   ▄█ ██   ▄██▀██▄   ▄█▀▀███   █ ██   ▄█ ██   ▄▄█▀██▀████████▄    ▄█▀▀███   ▄▄█▀██▀███▄███ \n" +
    "  █  ██  █▀ ██  ██▀   ▀██▄██    ██   █  ██  █▀ ██  ▄█▀   ██ ██    ██  ▄██    ██  ▄█▀   ██ ██▀ ▀▀ \n" +
    "  █  ██▄█▀  ██  ██     █████    ██   █  ██▄█▀  ██  ██▀▀▀▀▀▀ ██    ██  ███    ██  ██▀▀▀▀▀▀ ██     \n" +
    "  █  ▀██▀   ██  ██▄   ▄██▀██    ██   █  ▀██▀   ██  ██▄    ▄ ██    ██  ▀██    ██  ██▄    ▄ ██     \n" +
    "▄███▄ ▀▀  ▄████▄ ▀█████▀  ▀████▀███▄███▄ ▀▀  ▄████▄ ▀█████▀████  ████▄ ▀████▀███▄ ▀█████▀████▄   \n" +
    "                                                                                                 \n" +
    "By zer0p1us\n"+
    "====================================================================================")
    
    mod_list_data = {}
    mod_list_file = ""

    if len(argv) <= 1: mod_list_file = input("Please enter path of the file: ")
    else: mod_list_file = argv[len(argv)-1]
    
    try:
        mod_list_data = load_mods_list(mod_list_file)
    except Exception:
        print("Couldn't open file")
        sys.exit(-1)

    mods = mod_list_data["mods"]
    updated_mods = False

    # for each mod check latest version available and download if newer
    for index, item in enumerate(mods):
        if item["platform"] == "curseforge":
            continue
        current_mod = mod(name=item['id'], version=item['current_version'], path=item['file'])
        latest_mod = modrinth_get_latest_mod(current_mod, str(mod_list_data.get('minecraft_version')), str(mod_list_data.get('loader')))
        if (latest_mod.version == current_mod.version):
            print(f"no new updates for {current_mod.name}")
            continue # no new update available

        # else new version available
        print(f"new available updates for {current_mod.name} from {current_mod.version} -> {latest_mod.version}")
        if (input("Would you like to update this mod [Y/n]?: ").lower() == 'n'): continue
        update_jar(current_mod, latest_mod, get_mods_dir(mod_list_file))
        mods[index] = update_json(latest_mod, item)
        updated_mods = True
    
    if not updated_mods: return

    # save new mods_data
    # if old copy of modlist exist delete it cuz os.rename will fail otherwise
    path_to_backup_mod_list_file = os.path.join(os.path.dirname(mod_list_file), "old_"+os.path.basename(mod_list_file))
    if (os.path.exists(path_to_backup_mod_list_file)): os.remove(path_to_backup_mod_list_file)
    os.rename(mod_list_file, os.path.join(os.path.dirname(mod_list_file), "old_"+os.path.basename(mod_list_file)))
    mod_list_data["mods"] = mods
    save_mods_list(os.path.join(os.path.dirname(mod_list_file), os.path.basename(mod_list_file)), mod_list_data)

if __name__ == "__main__":
    main(sys.argv)
