# Library Documentation
Simple API that provides "easy" access to INIM web services

## Development

### Environment preparation
```sh
python3 -m pip install pipenv
pipenv install --dev #this generate Pipfile.lock
```

### Running
```sh
pipenv run python src/inim.py
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

### Pipenv way
```sh
pipenv run pip install --upgrade build
pipenv run python -m build --wheel
```


### Classical way
```sh
pip install --upgrade build
python -m build --wheel
```

## Some useful resources

- [tutorial](https://community.home-assistant.io/t/tutorial-for-creating-a-custom-component/204793)
- [practical guide to setuptools and pyproject.toml](https://xebia.com/blog/a-practical-guide-to-setuptools-and-pyproject-toml/)
- [pipenv-pyenv](https://www.rootstrap.com/blog/how-to-manage-your-python-projects-with-pipenv-pyenv)
- [hass thread](https://community.home-assistant.io/t/inim-alarm/60354/56)
- [INIM_API_notes](https://www.dropbox.com/s/sf0hze5n33hjie3/HomeAssistant_INIM_API_notes_public-v5.pdf?dl=0)
<!-- https://github.com/gidgethub/gidgethub/tree/main/gidgethub -->
