
Create python 3.12.3 + flask app 
CRUD app
dependency injection 
logging 
uv for dependecy management
Follow best practices
Separation of concerns
environment specific configuration
models User, Product
repositories, can have a baseRepo?
mapper classes
create class based routes
provide uv commands
use inmemory db, SQLAlchemy for ORM
separate file for db config
use mssql, connect to localhost mssql 1443
API does NOT return DB entity objects directly. Instead, return a separate response model (DTO / schema).

# ----- ----- ----- -----
# uv

pip install uv

> uv init
# creates pyproject.toml file 

# Add dependencies
> uv add flask flask_sqlalchemy python-dotenv marshmallow
> uv add flash sqlalchemy pyodbc pydantic python-dotenv

# Add dev dependencies
> uv add --dev pytest black ruff

> uv sync

> uv run python main.py
> uv run which python
# Runs .venv python

# ----- ----- ----- -----


# ----- ----- ----- -----


