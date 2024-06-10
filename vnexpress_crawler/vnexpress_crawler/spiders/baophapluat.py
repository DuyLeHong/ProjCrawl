import scrapy
import os
from scrapy.crawler import CrawlerProcess

class BaophapluatSpider(scrapy.Spider):
    name = "baophapluat"
    start_urls = [
        'https://baophapluat.vn/',
    ]

    def parse(self, response):
        base_url = response.url

        articles = response.css('article')

        for article in articles:
            yield {
                'base_url': base_url,
                'url': response.urljoin(article.css('a::attr(href)').get()),
                'category': article.css('span.cat-name a::text').get(),
                'subcategory': article.css('span.subcat-name a::text').get(),
                'title': article.css('h2.title-news a::text').get(),
                'abstract': article.css('p::text').get(),
                'content': '',  # Chưa lấy nội dung bài báo
                'publish': article.css('span.time::text').get(),
                'image': article.css('img::attr(src)').get()
            }

# Thiết lập thư mục lưu trữ dữ liệu
output_dir = 'news'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Chạy Spider và lưu kết quả vào file JSON
process = CrawlerProcess(settings={
    'FEEDS': {
        os.path.join(output_dir, 'baophapluat.json'): {'format': 'json'},
    },
})

process.crawl(BaophapluatSpider)
process.start()
