# MHFU Kitchen Helper

A small Python GUI application that displays available buffs (and debuffs) for the Monster Hunter Freedom Unite (MHFU) kitchen system.

## Overview

MHFU Kitchen Helper helps hunters plan their pre-hunt meals by calculating and displaying the effects of different ingredient combinations based on the number of Felyne Chefs in their kitchen.

## Running the app

- **Python**: >= 3.13
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

## Setup

### Using uv (recommended)

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/MHFU_Kitechen_Helper.git
    cd MHFU_Kitechen_Helper
    ```
2.  Install dependencies:
    ```bash
    uv sync
    ```

## Run Commands

To start the application:

```bash
uv run app.py
```
Or if using standard Python:
```bash
python app.py
```

### Build

The project includes a `build.py` script to create a standalone executable using [PyInstaller](https://www.pyinstaller.org/).

Make sure you have PyInstaller installed:
```bash
uv sync --dev
```

> The app depends on Tkinter being installed, even though the build process will not being impacted,
> you will be unable to launch the app if the Tkinter modules are not installed.  
> Tkinter is not disitributed via PyPi, it has to be installed separately, see the [docs](https://tkdocs.com/tutorial/install.html).

To build the application:
```bash
uv run build.py
```
Or if using standard Python:
```bash
python app.py
```

This will create a `dist/MHFUKitchenHelper` executable. The build includes the `lang/` directory resources.

## Localisation

As 1.2.0 patch, only the english language is supported, but it's actually easy to add new languages to the app,
just add a new JSON file to the with the translated string into the ``lang`` directory, and the app will automaticly load it.
Feel free to contribute by adding your language to the app !