import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class MySpider(scrapy.Spider):
    name = 'my_spider'

    def __init__(self, seed_url, max_pages=None, max_depth=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [seed_url]
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.visited_urls = set()

    def parse(self, response):
        depth = response.meta.get('depth', 0)
        if self.max_depth is not None and depth >= self.max_depth:
            return

        self.visited_urls.add(response.url)
        
        self.save_html(response)

        if self.max_pages is not None and len(self.visited_urls) >= self.max_pages:
            return

        for link in response.css('a::attr(href)').extract():
            yield response.follow(link, callback=self.parse, meta={'depth': depth + 1})

    def save_html(self, response):
        url = response.url.strip('/')
        filename = ''.join(c if c.isalnum() else '_' for c in url)
        filepath = os.path.join('htmlFiles', filename + '.html')
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(response.body)


def run_crawler(seed_url, max_pages=None, max_depth=None):
    process = CrawlerProcess(get_project_settings())
    process.crawl(MySpider, seed_url=seed_url, max_pages=max_pages, max_depth=max_depth)
    process.start()

if __name__ == "__main__":
    seed_url = "https://en.wikipedia.org/wiki/Roman_Empire"
    max_pages = 10
    max_depth = 3
    run_crawler(seed_url, max_pages, max_depth)
