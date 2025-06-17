import json
import random
from faker import Faker


faker = Faker()

def load_schema(schema_text: str) -> dict:
    return json.loads(schema_text)

def generate_fake_data(schema: dict):
    if "const" in schema:
        return schema["const"]

    elif "enum" in schema:
        return random.choice(schema["enum"])

    elif "default" in schema:
        return schema["default"]

    schema_type = schema.get("type")

    if schema_type == "object":
        properties = schema.get("properties", {})
        return {key: generate_fake_data(value) for key, value in properties.items()}

    elif schema_type == "array":
        item_schema = schema.get("items", {})
        return [generate_fake_data(item_schema) for _ in range(random.randint(1, 3))]

    elif schema_type == "string":
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

def process_schema(schema_text: str) -> str:
    schema = load_schema(schema_text)
    fake_data = generate_fake_data(schema)
    return json.dumps(fake_data, indent=2, ensure_ascii=False)