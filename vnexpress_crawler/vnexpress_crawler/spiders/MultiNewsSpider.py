import scrapy
from scrapy.crawler import CrawlerProcess
import os

class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        'https://baochinhphu.vn/',
        'https://cand.com.vn/',
        'https://doanhnghiepvn.vn/',
        'https://kinhtedothi.vn/',
        'https://nld.com.vn/',
        'https://nhandan.vn/',
        'https://plo.vn/',
        'https://www.sggp.org.vn/',
        'https://tienphong.vn/',
        'https://kienthuc.net.vn/',
        'https://vietnamnet.vn/'
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

# Chạy Spider và lưu kết quả vào các file JSON
process = CrawlerProcess(settings={
    'FEEDS': {
        os.path.join(output_dir, 'baochinhphu.json'): {'format': 'json'},
        os.path.join(output_dir, 'cand.json'): {'format': 'json'},
        os.path.join(output_dir, 'doanhnghiepvn.json'): {'format': 'json'},
        os.path.join(output_dir, 'kinhtedothi.json'): {'format': 'json'},
        os.path.join(output_dir, 'nld.json'): {'format': 'json'},
        os.path.join(output_dir, 'nhandan.json'): {'format': 'json'},
        os.path.join(output_dir, 'plo.json'): {'format': 'json'},
        os.path.join(output_dir, 'sggp.json'): {'format': 'json'},
        os.path.join(output_dir, 'tienphong.json'): {'format': 'json'},
        os.path.join(output_dir, 'kienthuc.json'): {'format': 'json'},
        os.path.join(output_dir, 'vietnamnet.json'): {'format': 'json'},
    },
})

process.crawl(NewsSpider)
process.start()