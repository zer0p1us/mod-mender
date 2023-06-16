# mod-mender 🔨

Tool to automatically update a set of mods to a given version of minecraft.

Supported platforms:
- Modrinth (Coming soon 🕝)
- Github (Coming soon 🕝)
- CurseForce (Coming soon 🕝)

## Building

Currently [Poetry](https://python-poetry.org/) will handle all the building and running as well as dependecies loading

### dependencies

To install all the dependencies in the virtual environment run the following from the root of the repository
```bash
poetry install
```

### Running

Once all the depencies have been install run the following to run the actual program, still from the root of the repository (or change the path to the main file)
```bash
poetry run python src/mod_mender/main.py
```

#### Installing

To create an installable build, run the following
```bash
poetry build
```

This will create a new dir called `dist` where a `tar.gz` and a `whl` files will be present, to install these packages call the following

```bash
pip install {path-to-build}
```
