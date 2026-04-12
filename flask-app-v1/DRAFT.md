
Create python 3.12.3 + flask app 
CRUD app
dependency injection 
logging 
uv for dependecy management

# ----- ----- ----- -----
# uv

pip install uv

> uv init
# creates pyproject.toml file 

# Add dependencies
> uv add flask flask_sqlalchemy python-dotenv marshmallow

# Add dev dependencies
> uv add --dev pytest black ruff

> uv sync

> uv run python main.py
> uv run which python
# Runs .venv python

# ----- ----- ----- -----


# ----- ----- ----- -----

