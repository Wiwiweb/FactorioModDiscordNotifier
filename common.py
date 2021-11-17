from dataclasses import dataclass

@dataclass
class ChangelogDetails:
    mod_id: str
    mod_name: str
    last_version: str
    image_url: str
    changelog: str

@dataclass
class ModSavedInfo:
    last_known_version: str
    last_posted_changelog: str
