import requests
from typing import Optional

from .kvusearch import Search
from .kvuconst import REQUA

__all__ = ['REQUA', 'Client', 'kvubook', 'kvucol', 'kvusearch']

class Client:

    def __init__(self, session:Optional[requests.Session]=None) -> None:
        
        self.session = session if session else requests.Session()
        self.session.headers.update({'User-Agent': REQUA})
    
    @classmethod
    def from_credentials(cls, login:str, password:str):

        session = requests.Session()
        session.headers.update({'User-Agent': REQUA})
        session.post(
            'https://knigavuhe.org/login/',
            data={
                'email': login,
                'password': password,
                'token': '0a8fb778ee0cb5bf7e56'
            }
        ).raise_for_status()

        if not 'auth' in session.cookies:
            raise ValueError('Check your username/email and password')

        return cls(session)
    
    @classmethod
    def from_cookies(cls, auth:str):

        session = requests.Session()
        session.headers.update({'User-Agent': REQUA})
        session.cookies.set('auth', auth)

        return cls(session)

    def search(self, query:str, limit:int=30, page:int=1):

        return Search(self.session, query, limit, page)
