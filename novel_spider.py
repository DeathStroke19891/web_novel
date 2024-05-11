from pathlib import Path
from pylatex import Document, Section, Subsection, Command, NoEscape
from pylatex.utils import italic

import scrapy
from scrapy.crawler import CrawlerProcess

doc = Document()
doc.documentclass = Command(
    'documentclass',
    options=['12pt', 'a4paper'],
    arguments=['article'],
)

doc.preamble.append(Command('title', 'Mother of Learning'))
doc.preamble.append(Command('author', 'nobody103'))
doc.preamble.append(Command('date', NoEscape(r'\today')))
doc.append(NoEscape(r'\maketitle'))
doc.preamble.append(Command('usepackage', 'bookmark'))
doc.append(NoEscape(r'\tableofcontents'))

i = 0

class NovelSpider(scrapy.Spider):
    name = "novel-spider"

    def start_requests(self):
        urls = [
            "https://freewebnovel.comenovel.com/mother-of-learning/chapter-1"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        text = ""
        plist = response.xpath("//p/text()").getall()
        for p in plist[:-2]:
            text += p
        global i
        i+=1
        with doc.create(Section("Chapter {}".format(i), numbering=True)):
            doc.append(text)
        next_url = response.css("a#next_url::attr(href)").get()
        if next_url == "https://freewebnovel.com/mother-of-learning.html":
            return
        else:
           next_page = response.urljoin(next_url)
           yield scrapy.Request(next_page, callback=self.parse)

process = CrawlerProcess(settings={
    'DOWNLOAD_DELAY': 0.5
})
process.crawl(NovelSpider)
process.start()

doc.generate_pdf("mother_of_learning", clean_tex=True)
