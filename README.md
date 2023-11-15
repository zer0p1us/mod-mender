<h1 align="center">
    mod-mender 🔨
</h1>
<p align="center">
    Tool to automatically update a set of mods to a given version of minecraft.
</p>

Supported platforms:
- Modrinth ✅
- CurseForce (Maybe possible in the future 🕝)

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

Now you can call it from the terminal with
```bash
mod-mender {file name}
```

## Idiosyncrasies

The `src` is structured as follows

```
src
└── mod_mender
    ├──main.py
    ├──...
    ├──...
```

This is due to how poetry creates builds, the "top" folder determines what the package folder will be called when installed. This means if the src was to be left as the "top" folder the package would be installed under `../site-packages/src`, needless to say this is just asking for trouble. So the `mod_mender` was neccessary as a stopgap, on the other hand why even bother to keep the src folder? **because I want to** and because it feels wrong to not have a src folder. Another details is that it has to be `mod_mender` rather than `mod-mender`; so far as I understand it, it's a result of `-` not being a valid char in a python module name.
