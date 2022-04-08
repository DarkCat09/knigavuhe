import re
import datetime
import requests
import lxml.html

from .kvucol import Collection
from .kvuconst import BASEURL

class Book:

    def __init__(
        self,
        session:requests.Session,
        url:str) -> None:
        
        if url.startswith('http'):
            # absolute link
            self.url = url
        else:
            # relative link
            self.url = BASEURL + url

        self.id = 0
        self.cover = ''
        self.title = ''
        self.author = None
        self.reader = None
        self.genre = None
        self.description = ''
        self.duration = 0
        self.added = ''
        self.likes = 0
        self.dislikes = 0
        self.favs = 0
        self.views = 0

        self.session = session
    
    def fetch(self) -> None:

        page = requests.get(self.url)
        tree = lxml.html.fromstring(page.content)

        info = tree.xpath('//div[@class="book_left_blocks"]')[0]
        acts = tree.xpath('//div[@class="book_right_blocks"]')[0]

        genreurl = info.xpath('//div[@class="book_genre_pretitle"]/a/@href')[0]
        self.genre = Collection(genreurl, self.session)

        pagetitle = info.xpath('//div[@class="page_title"]/h1')[0]
        self.title = pagetitle.xpath('./span[@itemprop="name"]')[0]\
            .text_content().strip()

        authorurl = pagetitle.xpath('.//span[@itemprop="author"]/a/@href')[0]
        self.author = Collection(authorurl, self.session)

        readerurl = pagetitle.xpath('.//a[starts-with(@href,"/reader")]/@href')[0]
        self.reader = Collection(readerurl, self.session)

        self.cover = info.xpath('//div[@class="book_cover"]/img/@src')[0]
        self.id = re.search(r'/covers/(\d+)/', self.cover).group(1)

        block = info.xpath('//div[@class="book_blue_block]')
        labels = block.xpath('./div[not(@class="-is_invis")]')

        # tags which should be removed
        tagdel = [
            '<span class="book_info_label -not_last">Время звучания:</span>',
            '<span class="book_info_label">Добавлена:</span>'
        ]
        time = labels[0].text_content()
        time = time.replace(tagdel[0], '')

        h, m, s = time.strip().split(':')
        self.duration = int(s) + int(m)*60 + int(h)*3600

        added = labels[1].text_content()
        added = added.replace(tagdel[1], '')
        self.added = self.convert_date(added)

        descr = info.xpath('//div[@itemprop="description"]')[0]
        self.description = descr.text_content().strip()

        likes = acts.xpath('//span[@id="book_likes_count"]')[0]
        self.likes = int(likes.text_content().strip())

        dlikes = acts.xpath('//span[@id="book_dislikes_count"]')[0]
        self.dislikes = int(dlikes.text_content().strip())

        favs = acts.xpath('//span[@id="book_fave_count"]')[0]
        self.favs = int(favs.text_content().strip())

        plays = acts.xpath('//div[@class="book_action_plays"]')[0]
        self.views = int(plays.text_content().strip())

    def download(self) -> None:
        requests.get(f'https://s10.knigavuhe.org/3/audio/{self.id}/PART.mp3')
    
    def convert_date(self, date:str) -> datetime.date:

        d, m, y = date.strip().lower().split(' ')
        if m.startswith('янв'): m = 1
        if m.startswith('фев'): m = 2
        if m.startswith('мар'): m = 3
        if m.startswith('апр'): m = 4
        if m.startswith('май'): m = 5
        if m.startswith('июн'): m = 6
        if m.startswith('июл'): m = 7
        if m.startswith('авг'): m = 8
        if m.startswith('сен'): m = 9
        if m.startswith('окт'): m = 10
        if m.startswith('ноя'): m = 11
        if m.startswith('дек'): m = 12
        return datetime.date(y, m, d)
