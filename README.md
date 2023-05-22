# mod-mender 🔨

Tool to automatically update a set of mods to a given version of minecraft.

Supported platforms:
- Modrinth (Coming soon 🕝)
- Github (Coming soon 🕝)
- CurseForce (Coming soon 🕝)

## Building

Currently [Poetry](https://python-poetry.org/) will handle all the building and running as well as dependecies loading

To install all the dependencies in the virtual environment run the following from the root of the repository
```bash
poetry install
```
Once all the depencies have been install run the following to run the actual program, still from the root of the repository (or change the path to the main file)
```bash
poetry run python src/main.py
```
