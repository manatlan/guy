# How to build a WHL package for pypi

You can create a pypi-package to distribute your app/tool !
It's really easy with [poetry](https://python-poetry.org/)

First of all : create your package, from a console :

    poetry new myapp
    
Edit your newly `myapp/pyproject.toml` to match :

```toml hl_lines="7 8 12"
[tool.poetry]
name = "myapp"
version = "0.1.0"
description = ""
authors = ["you <you@gmail.com>"]

[tool.poetry.scripts]            # <-- create a 'myapp' command
myapp = 'myapp:main'

[tool.poetry.dependencies]
python = "^3.7"
guy = "^0.4"                     # <-- add a dependency to guy

[tool.poetry.dev-dependencies]
pytest = "^3.0"

[build-system]
requires = ["poetry>=0.12"]
build-backend = "poetry.masonry.api"
```

I've setuped a console script in section `[tool.poetry.scripts]`. And I've added a dependency to `guy` in `[tool.poetry.dependencies]`.

Now, you just need to add the entry point `main()` (and the core app ;-) in your package ...

Edit the file `myapp/myapp/__init__.py` like that :

```python
__version__ = '0.1.0'

from guy import Guy

class App(Guy):
    """ hello """

def main():          # <-- the entry point for the script !!
    App().run()

if __name__=="__main__":
    main()
```

!!! info
    If you plan to declare your html in a static html file : just put your static datas in the `myapp/myapp/static` folder,
    and they will be be embbeded in the package (as `package_data`). Guy (>=0.4.0) will be able to resolve them in
    the installed package.


And you are ! Just build your package (place you in the folder where `pyproject.toml` sits)

    poetry build
    
And it's done ! 

You can distribute your package (`dist/myapp-0.1.0-py3-none-any.whl`), publish it to pypi.org ...

... or install it :

    python3.7 -m pip install --user --force dist/myapp-0.1.0-py3-none-any.whl 
