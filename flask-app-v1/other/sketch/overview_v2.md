Here’s a **production-style Flask app (Python 3.12.3)** with:

* ✅ CRUD (User, Product)
* ✅ Dependency Injection (simple container pattern)
* ✅ Logging
* ✅ Class-based routes
* ✅ Separation of concerns
* ✅ Environment-based config
* ✅ `uv` for dependency management

---

# 📁 Project Structure

```bash
flask-app/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── container.py
│   ├── extensions.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── product.py
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   └── product_repository.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   └── product_service.py
│   │
│   ├── routes/
│   │   ├── user_routes.py
│   │   └── product_routes.py
│   │
│   └── logging_config.py
│
├── run.py
├── pyproject.toml
└── .env
```

---

# ⚙️ `uv` Commands (Dependency Management)

```bash
# Install uv
pip install uv

# Create project
uv init flask-app
cd flask-app

# Create virtual env + install deps
uv add flask python-dotenv

# Optional (for dev)
uv add --dev pytest

# Run app
uv run python run.py
```

---

# ⚙️ `pyproject.toml` (auto-managed by uv)

```toml
[project]
name = "flask-app"
version = "0.1.0"
dependencies = [
    "flask",
    "python-dotenv"
]
```

---

# 🌱 Environment Config

## `.env`

```env
FLASK_ENV=development
```

---

## `app/config.py`

```python
import os

class BaseConfig:
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

def get_config():
    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
```

---

# 🧾 Logging

## `app/logging_config.py`

```python
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
```

---

# 🧱 Models

## `app/models/user.py`

```python
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
```

---

## `app/models/product.py`

```python
from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: float
```

---

# 🗄️ Repositories (In-Memory)

## `user_repository.py`

```python
from typing import List
from app.models.user import User

class UserRepository:
    def __init__(self):
        self.users: List[User] = []

    def add(self, user: User):
        self.users.append(user)

    def get_all(self):
        return self.users

    def delete(self, user_id: int):
        self.users = [u for u in self.users if u.id != user_id]
```

---

## `product_repository.py`

```python
from typing import List
from app.models.product import Product

class ProductRepository:
    def __init__(self):
        self.products: List[Product] = []

    def add(self, product: Product):
        self.products.append(product)

    def get_all(self):
        return self.products

    def delete(self, product_id: int):
        self.products = [p for p in self.products if p.id != product_id]
```

---

# 🧠 Services

## `user_service.py`

```python
import logging
from app.models.user import User

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, repo):
        self.repo = repo

    def create_user(self, user_id: int, name: str):
        user = User(user_id, name)
        self.repo.add(user)
        logger.info(f"User created: {user}")

    def list_users(self):
        return self.repo.get_all()

    def delete_user(self, user_id: int):
        self.repo.delete(user_id)
        logger.info(f"User deleted: {user_id}")
```

---

## `product_service.py`

```python
import logging
from app.models.product import Product

logger = logging.getLogger(__name__)

class ProductService:
    def __init__(self, repo):
        self.repo = repo

    def create_product(self, pid: int, name: str, price: float):
        product = Product(pid, name, price)
        self.repo.add(product)
        logger.info(f"Product created: {product}")

    def list_products(self):
        return self.repo.get_all()

    def delete_product(self, pid: int):
        self.repo.delete(pid)
        logger.info(f"Product deleted: {pid}")
```

---

# 🔌 Dependency Injection Container

## `app/container.py`

```python
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.services.user_service import UserService
from app.services.product_service import ProductService

class Container:
    def __init__(self):
        self.user_repo = UserRepository()
        self.product_repo = ProductRepository()

        self.user_service = UserService(self.user_repo)
        self.product_service = ProductService(self.product_repo)
```

---

# 🌐 Class-Based Routes

## `user_routes.py`

```python
from flask.views import MethodView
from flask import request, jsonify

class UserAPI(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        users = self.service.list_users()
        return jsonify([u.__dict__ for u in users])

    def post(self):
        data = request.json
        self.service.create_user(data["id"], data["name"])
        return {"message": "User created"}

    def delete(self):
        user_id = int(request.args.get("id"))
        self.service.delete_user(user_id)
        return {"message": "User deleted"}
```

---

## `product_routes.py`

```python
from flask.views import MethodView
from flask import request, jsonify

class ProductAPI(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        products = self.service.list_products()
        return jsonify([p.__dict__ for p in products])

    def post(self):
        data = request.json
        self.service.create_product(
            data["id"], data["name"], data["price"]
        )
        return {"message": "Product created"}

    def delete(self):
        pid = int(request.args.get("id"))
        self.service.delete_product(pid)
        return {"message": "Product deleted"}
```

---

# 🏗️ App Factory

## `app/__init__.py`

```python
from flask import Flask
from app.config import get_config
from app.container import Container
from app.routes.user_routes import UserAPI
from app.routes.product_routes import ProductAPI
from app.logging_config import setup_logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    setup_logging()

    container = Container()

    # Register routes
    user_view = UserAPI.as_view("user_api", service=container.user_service)
    product_view = ProductAPI.as_view("product_api", service=container.product_service)

    app.add_url_rule("/users", view_func=user_view, methods=["GET", "POST", "DELETE"])
    app.add_url_rule("/products", view_func=product_view, methods=["GET", "POST", "DELETE"])

    return app
```

---

# 🚀 Entry Point

## `run.py`

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
```

---

# 🧪 Example API Calls

```bash
# Create user
curl -X POST http://localhost:5000/users \
-H "Content-Type: application/json" \
-d '{"id":1,"name":"John"}'

# Get users
curl http://localhost:5000/users

# Delete user
curl -X DELETE "http://localhost:5000/users?id=1"
```

---

# 🧠 Why This Is Good (For Interviews)

* Clean architecture (Controller → Service → Repository)
* DI container (like Spring Boot mindset)
* Class-based views
* Logging separation
* Environment config
* Easily extendable (DB, auth, etc.)

---

# 🚀 If You Want Next Level

I can extend this to:

* ✅ SQLAlchemy (real DB)
* ✅ JWT authentication
* ✅ Middleware (Flask hooks)
* ✅ Unit tests with mocking DI
* ✅ Docker + CI/CD

Just tell me 👍
