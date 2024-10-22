def resolve_references(schema) -> dict:
    definitions = schema.get("$defs", {})

    def replace_refs(obj) -> dict:
        if isinstance(obj, dict):
            if "$ref" in obj:
                ref = obj["$ref"].split("/")[-1]
                return definitions[ref]

            return {k: replace_refs(v) for k, v in obj.items()}

        return obj

    return replace_refs(schema)
