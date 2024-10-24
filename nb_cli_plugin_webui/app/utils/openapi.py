from typing import Any, Dict


def resolve_references(schema) -> Dict[str, Any]:
    definitions = schema.get("$defs", {})

    def replace_refs(obj) -> Dict[str, Any]:
        if isinstance(obj, dict):
            if "$ref" in obj:
                ref = obj["$ref"].split("/")[-1]
                return definitions[ref]

            return {k: replace_refs(v) for k, v in obj.items()}

        if isinstance(obj, list):
            return {str(i): replace_refs(item) for i, item in enumerate(obj)}

        return obj

    return replace_refs(schema)
