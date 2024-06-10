import scrapy
from pymongo import MongoClient
from pathlib import Path

class VnExpressSpider(scrapy.Spider):
    name = 'vnexpress'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net']

    def __init__(self, *args, **kwargs):
        super(VnExpressSpider, self).__init__(*args, **kwargs)
        # Kết nối đến MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['vnexpress']

    def parse(self, response):
        articles = response.xpath('//article[@class="list_news"]')
        for article in articles:
            item = {}
            item['base_url'] = response.url
            item['url'] = article.xpath('./h3/a/@href').extract_first()
            item['category'] = article.xpath('./h3/a/@title').extract_first()
            item['subcategory'] = article.xpath('./h4/a/@title').extract_first()
            item['title'] = article.xpath('./h3/a/text()').extract_first()
            item['image'] = article.xpath('./a/img/@src').extract_first()
            # Truy cập trang chi tiết của bài viết để lấy nội dung
            yield scrapy.Request(item['url'], callback=self.parse_content, meta={'item': item})

    def parse_content(self, response):
        item = response.meta['item']
        item['content'] = ''.join(response.xpath('//article//p/text()').extract())
        self.save_to_mongodb(item)

    def save_to_mongodb(self, item):
        # Lưu item vào MongoDB
        self.db.articles.insert_one(item)

    def closed(self, reason):
        # Đóng kết nối MongoDB khi Spider kết thúc
        self.client.close()