import json
from string import Template
import re

def extract_variables(template_str: str) -> list[str]:
    """
    Ищет переменные в шаблоне вида ${variableName}
    """
    return list(set(re.findall(r"\${(.*?)}", template_str)))

def render_template(template_str: str, variables: dict) -> dict:
    """
    Подставляет переменные в шаблон.
    """
    tpl = Template(template_str)
    rendered = tpl.safe_substitute(variables)
    return json.loads(rendered)

def json_to_template(data, parent_key=""):
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            new_key = f"{parent_key}_{key}" if parent_key else key
            if isinstance(value, (dict, list)):
                result[key] = json_to_template(value, new_key)
            else:
                result[key] = f"${{{new_key}}}"
        return result
    elif isinstance(data, list):
        result = []
        for index, item in enumerate(data):
            indexed_key = f"{parent_key}_{index}" if parent_key else str(index)
            result.append(json_to_template(item, indexed_key))
        return result
    else:
        return data

