import json
import random
from integrations.FakeApi.faker_user_repository import FakerUserRepository
from integrations.FakeApi.fake_user_service import FakeUserService
from faker import Faker
from typing import Optional, Any

faker_repo = FakerUserRepository()
service = FakeUserService(faker_repo)

faker = Faker()

def load_schema(schema_text: str) -> dict:
    return json.loads(schema_text)

def generate_fake_data(schema: dict, key: Optional[str] = None):
    if "const" in schema:
        return schema["const"]

    elif "enum" in schema:
        return random.choice(schema["enum"])

    elif "default" in schema:
        return schema["default"]

    schema_type = schema.get("type")

    if schema_type == "object":
        properties = schema.get("properties", {})
        return {prop_key: generate_fake_data(prop_schema, key=prop_key)
                for prop_key, prop_schema in properties.items()}

    elif schema_type == "array":
        item_schema = schema.get("items", {})
        quantity = random.randint(1, 3)
        result = []
        for _ in range(quantity):
            item_key = item_schema.get("title")
            result.append(generate_fake_data(item_schema, key=item_key))
        return result

    elif schema_type == "string":
        if key and "lastName" in key:
            users = service.get_fake_users(quantity=1)
            if users:
                return users[0].lastname
            return "Unknown"
        elif key and "firstName" in key:
            users = service.get_fake_users(quantity=1)
            if users:
                return users[0].firstname
            return "Unknown"
        else:
            fmt = schema.get("format")
            if fmt == "email":
                return faker.email()
            elif fmt == "date":
                return faker.date()
            elif fmt == "uuid":
                return faker.uuid4()
            elif "enum" in schema:
                return random.choice(schema["enum"])
            return faker.word()

    elif schema_type == "integer":
        return faker.random_int(min=0, max=1000)

    elif schema_type == "number":
        return round(random.uniform(0, 1000), 1)

    elif schema_type == "boolean":
        return faker.boolean()

    return None

def process_schema(schema_text: str) -> Any:
    schema = load_schema(schema_text)
    fake_data = generate_fake_data(schema)
    return fake_data