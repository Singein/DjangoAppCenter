from DjangoAppCenter.settings.loader import get_settings_dbcfg, load_settings

settings = load_settings()
# settings.get("DATABASES", {}).update(**get_settings_dbcfg())
for key, value in settings.items():
    if isinstance(value, str):
        exec(f"{key}='{value}'")
    elif isinstance(value, int):
        exec(f"{key}={value}")
    elif isinstance(value, (dict, list)):
        exec(f"{key}={str(value)}")
