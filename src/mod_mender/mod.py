from dataclasses import dataclass
import urllib.parse

@dataclass
class mod:
    name: str
    latest_version: str
    url: str = ""
    path: str = ""
    
    def get_url_filename(self) -> str:
        return urllib.parse.unquote(self.url.rsplit('/', 1)[1])
