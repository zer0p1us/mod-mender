# Mod list JSON Structure

This documents the structure of the `JSON` file that contains the mods list

```JSON
{
    "minecraft_version" : "1.19.4",
    "loader": "quilt",
    "mods" : [
        {
            "mod_name" : "name",
            "url" : "link",
            "current_version" : ""
        },
        {
            "mod_name" : "name",
            "url" : "link",
            "current_version" : ""
        }
    ]
}
```

## Properties

**minecraft_version** (String): Indicate the minecraft version of that is being targetted by the mod list
**loader** (String): Indicate the mod loader that the mod list is using
**mods** (List): List of mods that are part of the mod list, each list element has the following
- **mod_name** (String): Name of the mod
- **url** (String): Link to the mod page, yet to be decide on which platforms to support
- **current_version** (String): Version of the mod being using currently
