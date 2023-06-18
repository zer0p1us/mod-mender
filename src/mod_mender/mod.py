from dataclasses import dataclass

@dataclass
class mod:
    name: str
    latest_version: str
    url: str = ""
    path: str = ""
    
    def get_url_filename(self) -> str:
        return self.url.rsplit('/', 1)[1]
