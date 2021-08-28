from dataclasses import dataclass

@dataclass
class ChangelogDetails:
    mod_id: str
    mod_name: str
    latest_version: str
    image_url: str
    changelog: str
