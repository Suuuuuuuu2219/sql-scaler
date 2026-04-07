from pydantic import BaseModel
from typing import List, Dict, Any

class Task(BaseModel):
    id: str
    difficulty: str
    query: str
    schema_info: Dict[str, Any]
    optimal: str

TASKS: List[Task] = [
    Task(
        id="easy_1",
        difficulty="easy",
        query="SELECT * FROM users;",
        schema_info={"users": ["id", "name", "age", "country"]},
        optimal="SELECT id, name, age, country FROM users;"
    ),
    Task(
        id="medium_1",
        difficulty="medium",
        query="SELECT users.name, orders.amount FROM users JOIN orders ON users.id = orders.user_id;",
        schema_info={
            "users": ["id", "name", "age", "country"],
            "orders": ["id", "user_id", "amount"]
        },
        optimal="SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id;"
    ),
    Task(
        id="hard_1",
        difficulty="hard",
        query="SELECT name FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 100);",
        schema_info={
            "users": ["id", "name", "age", "country"],
            "orders": ["id", "user_id", "amount"]
        },
        optimal="SELECT u.name FROM users u JOIN orders o ON u.id = o.user_id WHERE o.amount > 100;"
    )
]
