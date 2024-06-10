from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            # "https://quotes.toscrape.com/page/1/",
            # "https://quotes.toscrape.com/page/2/",
            'https://www.anninhthudo.vn/',
            'https://baophapluat.vn/',
            'https://baotintuc.vn/',
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
            'https://vietnamnet.vn/',
            'https://vnexpress.net/',
            'https://vov.vn/',
            'https://vtc.vn/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")