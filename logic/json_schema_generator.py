import json

def infer_type(value):
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "number"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, list):
        return "array"
    elif isinstance(value, dict):
        return "object"
    else:
        return "string"  # fallback

def merge_types(types):
    # Убираем дубликаты и сохраняем порядок
    seen = set()
    return [t for t in types if not (t in seen or seen.add(t))]

def merge_schemas(schemas):
    # Объединение нескольких схем в одну
    types = merge_types([s.get("type") for s in schemas if "type" in s])
    result = {"type": types[0] if len(types) == 1 else types}

    if "object" in types:
        properties = {}
        required = set()
        for s in schemas:
            if s.get("type") == "object":
                props = s.get("properties", {})
                for k, v in props.items():
                    if k in properties:
                        properties[k] = merge_schemas([properties[k], v])
                    else:
                        properties[k] = v
                required.update(s.get("required", []))
        result["properties"] = properties
        if required:
            result["required"] = list(required)

    elif "array" in types:
        items = [s.get("items", {}) for s in schemas if s.get("type") == "array"]
        result["items"] = merge_schemas(items) if items else {}

    return result

def generate_schema(data):
    if isinstance(data, dict):
        schema = {"type": "object", "properties": {}, "required": list(data.keys())}
        for key, value in data.items():
            schema["properties"][key] = generate_schema(value)
        return schema

    elif isinstance(data, list):
        if not data:
            return {"type": "array", "items": {}}
        item_schemas = [generate_schema(item) for item in data]
        merged_items = merge_schemas(item_schemas)
        return {"type": "array", "items": merged_items}

    else:
        t = infer_type(data)
        return {"type": t}

def json_to_json_schema(json_str):
    try:
        data = json.loads(json_str)
        schema_body = generate_schema(data)
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            **schema_body
        }
        return json.dumps(schema, indent=2, ensure_ascii=False)
    except json.JSONDecodeError as e:
        return f"Ошибка JSON: {e}"