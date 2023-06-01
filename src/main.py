import requests
import json
from typing import Dict
import sys


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

def load_mods_list(path: str) -> Dict:
    """
    Loads JSON data into dictionary
    @param path: file path to the mod_list.json file
    @return: dictionary with the json content of mod_list.json
    """
    file = open(path)
    return json.load(file)

def main(argv: list[str]):
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
    pass

if __name__ == "__main__":
    main(sys.argv)
