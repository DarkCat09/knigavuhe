import requests
from typing import Optional

from .kvuconst import BASEURL

class Collection:

    def __init__(
        self, url:str,
        session:Optional[requests.Session]=None) -> None:
        
        if url.startswith('http'):
            # absolute link
            self.url = url
        else:
            # relative link
            self.url = BASEURL + url
        
        self.books = []
        self.session = session
    
    def fetch(self) -> None:
        pass
