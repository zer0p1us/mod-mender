#!/usr/bin/env python3
import requests
import json
from typing import Dict
import sys
import os

from .mod import mod

def get_page(url: str) -> str:
    """
    Retrieves the html content of a url
    @param url: URL to request
    @return: html content
    """
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error retrieving webpage. Status code: {response.status_code}")
        return ""

def modrinth_get(id: str, loader: str, mc_version: str) -> str:
    """
    Makes a GET to modrinth api to get the latest version of a mod
    @param id: mod identifier
    @param loader: minecraft mod loader
    @param mc_version: minecraft version
    @return: GET response
    """
    params = {'loaders': "[\""+loader+"\"]", 'game_versions': "[\""+mc_version+"\"]"}
    response = requests.get(url=f'https://api.modrinth.com/v2/project/{id}/version', params=params)
    
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
    file = open(path)
    return json.load(file)


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
            #print(mc_version, " != ", version["game_versions"])
            continue
        if loader not in version["loaders"]:
            #print(loader, " != ", version["loaders"])
            continue
        if version["version_number"] == current_mod.latest_version:
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
    if ((current_version.path_or_url_to_jar != "") & (os.path.exists(jar_destination+current_version.path_or_url_to_jar))): os.remove(jar_destination+current_version.path_or_url_to_jar)
    file = requests.get(url=latest_version.path_or_url_to_jar, stream=True)
    print("downloadind: "+jar_destination+latest_version.path_or_url_to_jar.split('/')[-1])
    open(jar_destination+latest_version.path_or_url_to_jar.split('/')[-1], "wb").write(file.content)

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

    # for each mod check latest version available and download if newer
    for i in mod_list_data.get("mods"):
        if i["platform"] == "curseforge":
           continue
        current_mod = mod(name=i.get('id'), latest_version=i.get('current_version'), path_or_url_to_jar=i.get('file'))
        latest_mod = modrinth_get_latest_mod(current_mod, str(mod_list_data.get('minecraft_version')), str(mod_list_data.get('loader')))
        if (latest_mod.latest_version == current_mod.latest_version):
            print(f"no new updates for {current_mod.name}")
            continue # no new update available

        # else new version available
        print(f"new available updates for {current_mod.latest_version} from {current_mod.latest_version} -> {latest_mod.latest_version}")
        update_jar(current_mod, latest_mod, argv[len(argv)-1].split('/')[0]+'/')
    pass

if __name__ == "__main__":
    main(sys.argv)