# Library Documentation
Simple API that provides "easy" access to INIM web services

## Usage

```sh
python3 -m venv venv
source venv/bin/activate.fish
python3 -m pip install aiohttp==3.9.5
# python3 -m pip install python-dotenv==1.0.1

# deprecated:
#python3 -m pip install --index-url https://test.pypi.org/simple/ pyinim-nidble==0.0.x
# python3 -m pip uninstall pyinim-nidble

python3 -m pip install pyinim==0.0.x
python3 -m pip uninstall pyinim
```

## Development

### Environment preparation
```sh
python3 -m pip install pipenv
pipenv install --dev #this generate Pipfile.lock
```

### Running
```sh
export PYTHONPATH="${PYTHONPATH}:$PWD" # or set --export PYTHONPATH ./src
pipenv run python src/pyinim/examples/poc.py
```

### Adding new lib
```sh
pipenv install python-dotenv
```

## Building the package

### Environment preparation
```sh
pip3 install --upgrade setuptools

# NO:
pip install --upgrade build
# Yes:
python3 -m pip install build # see https://stackoverflow.com/questions/73987135/python3-m-build-gives-modulenotfounderror-no-module-named-pathlib2
```

### Publishing Pipenv way
```sh
pipenv run pip install --upgrade build
pipenv run python -m build --wheel
```

### Publishing Classical way
```sh
pip install --upgrade build
python -m build --wheel # for only wheel (this not produce tarball)
python3 -m build # for wheel and tarball
```

### Publishing
[ref](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
###
```sh
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```

### Publishing & Publishing
```sh
rm -rf ./dist && python3 -m build && python3 -m twine upload --repository testpypi dist/*
```


## Some useful resources

- [tutorial](https://community.home-assistant.io/t/tutorial-for-creating-a-custom-component/204793)
- [practical guide to setuptools and pyproject.toml](https://xebia.com/blog/a-practical-guide-to-setuptools-and-pyproject-toml/)
- [pipenv-pyenv](https://www.rootstrap.com/blog/how-to-manage-your-python-projects-with-pipenv-pyenv)
- [hass thread](https://community.home-assistant.io/t/inim-alarm/60354/56)
- [INIM_API_notes](https://www.dropbox.com/s/sf0hze5n33hjie3/HomeAssistant_INIM_API_notes_public-v5.pdf?dl=0)
<!-- https://github.com/gidgethub/gidgethub/tree/main/gidgethub -->

# Disclaimer
Pyinim is an unofficial module for achieving interoperability with Inim RESTful API.

Author is in no way affiliated with Inim.

All the api requests used within the library are available and published on the internet (examples linked above) and this module is purely just a wrapper around those https requests.

Author does not guarantee functionality of this library and is not responsible for any damage.

All product names, trademarks and registered trademarks in this repository, are property of their respective owners.


# Inim CLI

You can use this small script to interact with your InimAlarm and list various components.


## Install the CLI
```sh
git clone https://github.com/nidble/pyinim
cd pyinim
python3 -m pip install pipenv
pipenv install --dev
export PYTHONPATH="${PYTHONPATH}:$PWD/src" # or set --export PYTHONPATH ./src
pipenv run python tools/inim_cli.py
```

## Read the Help for the usage:
```txt
❯ pipenv run python tools/inim_cli.py --help
usage: inim_cli.py [-h] [--username USERNAME] [--password PASSWORD] [--client_id CLIENT_ID] --list {deviceid,areas,scenarios} [--deviceid DEVICEID] [--dump filename]

options:
  -h, --help            show this help message and exit
  --username USERNAME   Inim User Name
  --password PASSWORD   Inim Password
  --client_id CLIENT_ID
                        Inim Client ID
  --list {deviceid,areas,scenarios}
                        Specify whether to list 'deviceid', 'areas', or 'scenarios'
  --deviceid DEVICEID   Optional device ID to filter results for 'areas' and 'scenarios'
  --dump filename       Dump the raw JSON response to the specified file
```

## Discover your devices ID
```sh
pipenv run python tools/inim_cli.py --username <YOUR_INIM_USERNAME> --password <YOUR_INIM_PASSWORD> --list deviceid
```

## Discover your Areas ID
```sh
pipenv run python tools/inim_cli.py --username <YOUR_INIM_USERNAME> --password <YOUR_INIM_PASSWORD> --list areas
```

## Discover your Scenarios ID
```sh
pipenv run python tools/inim_cli.py --username <YOUR_INIM_USERNAME> --password <YOUR_INIM_PASSWORD> --list scenarios
```

## TroubleShooting Info and Debug

To debug your Alarm you can dump the status via --dump
```sh
pipenv run python tools/inim_cli.py --username <YOUR_INIM_USERNAME> --password <YOUR_INIM_PASSWORD> --dump=debug.json
```
