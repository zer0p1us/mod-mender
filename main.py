import requests
import json
from typing import Dict


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
    file = open('mod_list.json')
    return json.load(file)

def main():
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
    pass

if __name__ == "__main__":
    main()
