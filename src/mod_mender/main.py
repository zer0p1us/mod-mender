#!/usr/bin/env python3
import json
from typing import Dict
import sys
import os

import requests
import click

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

def modrinth_get(mod_id: str, loaders: [str], mc_version: str) -> str:
    """
    Makes a GET to modrinth api to get the latest version of a mod
    @param mod_id: mod identifier used by modrinth
    @param loaders: minecraft mod loaders
    @param mc_version: minecraft version
    @return: GET response
    """
    params = {'loaders': "[\""+"\", \"".join(loaders)+"\"]", 'game_versions': "[\""+mc_version+"\"]"}
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
        json.dump(mod_list_data, file, indent=4)

def modrinth_get_latest_mod(current_mod: mod, mc_version: str, loaders: [str]) -> mod:
    """
    Get the latest version of a mod for a specific minecraft version
    @param id: path to the list of mod versions
    @param current_mod_version: current version name of the mod
    @param mc_version: minecraft version needed
    @param loaders: list of mod loaders to target
    """
    modrinth_data = modrinth_get(current_mod.name, loaders, mc_version)
    for version in modrinth_data:
        if mc_version not in version["game_versions"]:
            continue
        if not any(x in loaders for x in version["loaders"]):
            continue
        if version["version_number"] == current_mod.version:
            return current_mod
        else:
            return mod(current_mod.name, version["version_number"], version["files"][0]["url"])

    return current_mod

def curseforge_get_latest_mod(current_mod: mod, mc_version: str, loaders: [str]) -> mod:
    """
    Get the latest version of a mod for a specific minecraft version
    @param id: path to the list of mod versions
    @param current_mod_version: current version name of the mod
    @param mc_version: minecraft version needed
    @param loaders: list of mod loaders to target
    """
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


def check_for_update(_mod: mod, mc_version: str, loaders: str, platform_check: callable) -> {bool, mod}:
    """
    Check if there are any updates for a given mod
    @param mod: mod object with mod details
    @param mc_version: minecraft version being targeted
    @param loaders: list of mod loaders being targeted
    @param platform_check: function for the mod platform to check for updates, will return a mod object of the lastest mod
    @return dictionary of a boolean indicating if there is an update and a mod object with latest details
    """
    latest_mod = platform_check(_mod, mc_version, loaders)
    if (latest_mod.version == _mod.version): return {False, _mod} # no new update available
    return {True, latest_mod}

def check_for_updates(mods: list[dict], mc_version: str, loaders: [str]) -> list[[mod, int]]:
    """
    Check for updates for a given list of mods
    @param mods: list of dictionaries containing mods details
    @param mc_version: minecraft version to check updates for
    @param loaders: list of mod loaders to for mods
    @return list of lists, each inner list has a mod object that has an update with the latest data and an index of the mod data in mods
    """
    updates = []
    for index, mod_json in enumerate(mods):
        match mod_json["platform"].lower():
            case "modrinth":
                get_latest_mod = modrinth_get_latest_mod
            case "curseforge":
                get_latest_mod = curseforge_get_latest_mod
            case _:
                print(f"Unsopported or misspelled mod platform {mod_json['platform']}")
                continue

        current_mod = mod(name=mod_json['id'], version=mod_json['current_version'], path=mod_json['file'])
        latest_mod = get_latest_mod(current_mod, mc_version, loaders)
        if (latest_mod.version == current_mod.version):
            print(f"no update possible for {current_mod.name} for {mc_version}")
            continue # no new update available

        # else new version available
        print(f"new available updates for {current_mod.name} from {current_mod.version} -> {latest_mod.version}")
        updates.append([latest_mod, index])
    return updates

def generate_mod_list(file:str):
    """
    Generate a new mod list json configuration
    @param file: path to json file to be generated
    """
    mc_version = input("Minecraft version you're targeting: ")
    loaders = input("Mod loaders you're targeting (seperate with a (,) if multiple): ").replace(' ', '').split(",")
    json_schema = {
        "minecraft_version": mc_version,
        "loaders": loaders,
        "mods": [{}]
    }
    with open(file, "w", encoding="utf8") as mod_list_file:
        json.dump(json_schema, mod_list_file, indent=4)

def strip_mod_details(mod_json: dict) -> dict:
    """
    Remove version and jar file details from a mod's json data
    @param mod_json: json data for a mod to be striped
    @return dict with striped json data
    """
    mod_json["current_version"] = ""
    mod_json["file"] = ""
    return mod_json

@click.command()
@click.argument("file", required=True, type=click.Path())
@click.option("-nf", "--new-file", flag_value=True, help="Generate a new modlist file")
@click.option("-u", "--update-to", type=str, help="Check if updating to a minecraft version is possible")
def main(file: str, update_to: str, new_file: bool = False):
    """Update mods in FILE"""
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

    if (new_file):
        generate_mod_list(file)
        sys.exit(0)
    
    mod_list_data = {}
    mod_list_file = file

    try:
        mod_list_data = load_mods_list(mod_list_file)
    except FileNotFoundError:
        print("Couldn't find {mod_list_file}")
        sys.exit(-1)
    except Exception:
        print("Couldn't open {mod_list_file}")
        sys.exit(-1)

    mods = mod_list_data["mods"] if mod_list_data["mods"] != [{}] else sys.exit(-1)

    minecraft_version = mod_list_data['minecraft_version']

    # if the -u option has been given change the minecraft version being checked for
    if (update_to is not None): minecraft_version = update_to

    available_updates = check_for_updates(mods, minecraft_version, mod_list_data['loaders'])

    if not available_updates:
        print(f"No available updates for any mod on {minecraft_version}")
        sys.exit(0)
    
    # ask if the of the mods should be updated
    if (input("Would you like to update the [Y/n]").lower() == 'n'): sys.exit(0)

    # if the mods have been updated to a newer version of minecraft update the `minecraft_version` on the mod list file
    if minecraft_version != mod_list_data["minecraft_version"]:
        mod_list_data["minecraft_version"] = minecraft_version
        supported_mods = [update_index[1] for update_index in available_updates]
        unsupported_mods = [update_index for update_index in range(len(mods)) if update_index not in supported_mods]
        # empty `verion` & `file` properties for mods that can't be updated to newer minecraft version
        for unsupported_mod in unsupported_mods:
            mods[unsupported_mod] = strip_mod_details(mods[unsupported_mod])

    for latest_mod, index in available_updates:
        current_mod_json = mods[index]
        current_mod = mod(name=latest_mod.name, version=current_mod_json["current_version"], path=current_mod_json['file'])
        update_jar(current_version=current_mod, latest_version=latest_mod, jar_destination=get_mods_dir(mod_list_file))
        mods[index] = update_json(latest_mod, current_mod_json)

    # save new mods_data
    # if old copy of modlist exist delete it cuz os.rename will fail otherwise
    path_to_backup_mod_list_file = os.path.join(os.path.dirname(mod_list_file), "old_"+os.path.basename(mod_list_file))
    if (os.path.exists(path_to_backup_mod_list_file)): os.remove(path_to_backup_mod_list_file)
    os.rename(mod_list_file, os.path.join(os.path.dirname(mod_list_file), "old_"+os.path.basename(mod_list_file)))
    mod_list_data["mods"] = mods
    save_mods_list(os.path.join(os.path.dirname(mod_list_file), os.path.basename(mod_list_file)), mod_list_data)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    # because main is populated by `click`
    # and pylint complains about the lack of parameters
    main()
