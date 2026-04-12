# Smart Fan Project

Create a virtual environment before installing necessary dependencies

to create a python virtual environment, run

```sh
# in powershell

# makes the .venv file in your wd
python -m venv .venv

# activates the environment, uses relative path
.\.venv\Scripts\Activate.ps1

```

```bash
# in bash

# makes the .venv file in your wd
python3 -m venv .venv

# activates the environment, uses relative path
source .venv/bin/activate

# check to make sure if it's working
which python
# should return python from your .venv folder
# the same can be done for pip
```

to install dependencies, run

```sh
# in powershell
python -m pip install -r requirements.txt

```