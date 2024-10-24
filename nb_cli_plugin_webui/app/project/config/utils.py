from .schemas import Item, ModuleConfigChild


def config_child_parser(name: str, data: dict) -> ModuleConfigChild:
    conf_type = data.get("type", "string")
    conf_configured = data.get("configured")
    conf_enum = data.get("enum")
    conf_default = data.get("default") if conf_type != "object" else conf_configured
    conf_items = Item(**item) if (item := data.get("items")) else None
    conf_title = data.get("title", "Unknown Config")
    conf_description = data.get("description")
    conf_unique_items = data.get("uniqueItems", False)
    conf_is_secret = data.get("writeOnly", False)
    conf_latest_change = data.get("latest_change", ".env")

    return ModuleConfigChild(
        title=conf_title,
        description=conf_description,
        name=name,
        default=conf_default,
        conf_type=conf_type,
        enum=conf_enum,
        configured=conf_configured,
        items=conf_items,
        unique_items=conf_unique_items,
        is_secret=conf_is_secret,
        latest_change=conf_latest_change,
    )
