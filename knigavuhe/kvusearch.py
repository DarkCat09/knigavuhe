import re
import requests
import lxml.html
from typing import List, Dict, Any, Union

from .kvubook import Book
from .kvucol import Collection
from .kvuconst import BASEURL, REQUA

class Search:

    def __init__(
        self, session:requests.Session,
        query:str, limit:int=30, page:int=1) -> None:
        
        self.q = query
        self.len = len(query)
        self.lim = limit
        self.page = page

        self.session = session

    def makereq(self, stype:str) -> bytes:

        byletter = f'/{stype}/letter/{self.q}'
        bytext = f'/search/{stype}'
        req = None

        if (self.len < 1):
            raise ValueError('Empty search request!')

        elif (self.len == 1 and stype != ''):
            # if the search text is one letter
            req = self.session.get(
                BASEURL + byletter
            )
        
        else:
            req = self.session.get(
                BASEURL + bytext,
                params={
                    'q': self.q,
                    'page': self.page
                }
            )

        req.raise_for_status()
        return req.content
    
    def parse(self, cls, response:bytes, expr:str) -> Dict[str,Union[List[Any],int]]:

        tree = lxml.html.fromstring(response)
        res = tree.xpath(expr)
        lst = []

        for n, item in enumerate(res):
            if n > self.lim:
                break
            lst.append(cls(item, self.session))
        
        pages = tree.xpath('//div[@class="pn_page_buttons"]/a[contains(@class," -page")][last()]/@data-pages')

        count = 0
        countexp = [
            # on different pages the count label
            # is located in diff. places
            tree.xpath('//div[@class="page_title"]/b'),
            tree.xpath('//div[@class="page_title_ext_sublabel"]/b'),
            tree.xpath('//div[@class="page_title_count"]')
        ]
        for c in countexp:
            if not c:
                continue
            # extracting a number
            match = re.search(r'^([\d ]+)', c[0].text_content())
            if match:
                count = match[0].replace(' ', '')
        
        return {
            'results': lst,
            'pages': int(pages),
            'count': int(count)
        }
    
    def books(self) -> Dict[str,Union[List[Book],int]]:
        
        return self.parse(
            Book,
            self.makereq(''),
            '//div[@class="bookkitem"]/a/@href'
        )

    def authors(self) -> Dict[str,Union[List[Collection],int]]:

        return self.parse(
            Collection,
            self.makereq('authors'),
            '//div[contains(@class,"common_list_item ")]/a/@href'
        )

    def readers(self) -> Dict[str,Union[List[Collection],int]]:
        
        return self.parse(
            Collection,
            self.makereq('readers'),
            '//div[contains(@class,"common_list_item ")]/a/@href'
        )

    def series(self) -> Dict[str,Union[List[Collection],int]]:

        return self.parse(
            Collection,
            self.makereq('series'),
            '//div[contains(@class,"common_list_item ")]/a/@href'
        )
