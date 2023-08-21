# Mod list JSON Structure

This documents the structure of the `JSON` file that contains the mods list

```JSON
{
    "minecraft_version" : "1.19.4",
    "loader": ["quilt", "fabric"],
    "mods" : [
        {
            "mod_name" : "name",
            "id" : "link",
            "platform": "modrinth",
            "current_version" : "",
            "file": ""
        },
        {
            "mod_name" : "name",
            "url" : "link",
            "platform": "curseforge",
            "current_version" : "",
            "file": ""
        }
    ]
}
```

## Properties

**minecraft_version** (String): Indicate the minecraft version of that is being targetted by the mod list
**loader** (List of Strings): Indicate the mod loaders that the mod list is using, it needs to be a list because some mods only specify one the base loader and not the forks
**mods** (List): List of mods that are part of the mod list, each list element has the following
- **mod_name** (String): Name of the mod
- **platform** (String): the platform the mod is hosted on
- **id** (String): id of the mod to retrieve through modrinth, **Only for Modrinth**
- **url** (String): Link to the mod page, **Only for CurseForge**
- **current_version** (String): Version of the mod being using currently
- **file** (String): Relative path to the mod file compared to json file
