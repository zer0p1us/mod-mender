from dataclasses import dataclass
import urllib.parse

@dataclass
class mod:
    name: str
    version: str
    url: str = ""
    path: str = ""
    
    def __str__(self) -> str:
        return self.name+self.version

    def __hash__(self) -> int:
        return hash(str(self))

    def get_url_filename(self) -> str:
        return urllib.parse.unquote(self.url.rsplit('/', 1)[1])
