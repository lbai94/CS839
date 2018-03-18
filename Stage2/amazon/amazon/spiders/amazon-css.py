import scrapy
from time import sleep


class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    #fiction, history, fiction in german,health and diet,
    #start_urls = ['https://www.amazon.com/s/ref=lp_9_pg_2?rh=n%3A283155%2Cn%3A%211000%2Cn%3A9&page=2&ie=UTF8&qid=1521357971']
    #start_urls = ['https://www.amazon.com/s/ref=lp_17_pg_2?rh=n%3A283155%2Cn%3A%211000%2Cn%3A17&page=2&ie=UTF8&qid=1521349537']

    #start_urls = ['https://www.amazon.com/s/ref=lp_283155_nr_p_n_feature_nine_bro_1?fst=as%3Aoff&rh=n%3A283155%2Cp_n_feature_nine_browse-bin%3A3291436011&bbn=283155&ie=UTF8&qid=1521358536&rnid=3291435011']
    #start_urls = ['https://www.amazon.com/s/ref=lp_10_pg_2?rh=n%3A283155%2Cn%3A%211000%2Cn%3A10&page=2&ie=UTF8&qid=1521359718']
    start_urls = ['https://www.amazon.com/s/ref=lp_3_pg_2?rh=n%3A283155%2Cn%3A%211000%2Cn%3A3&page=2&ie=UTF8&qid=1521360739']

    def parse(self, response):
        # follow links to book pages
        book_pages = response.css('a[class*="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]::attr(href)').extract()
        for href in book_pages:
            #self.count = self.count + 1
            yield response.follow(href, self.parse_book)

        # follow pagination links
        next_pages = response.css('a[title*="Next Page"]::attr(href)').extract()
        for href in next_pages:

            yield response.follow(response.urljoin(href), self.parse)

    def parse_book(self, response):


        yield {
            'Title': response.css('span[id*="productTitle"]::text').extract_first().strip(),
            'Author': response.css('td.a-size-base div.a-row span.a-size-medium::text').extract_first().strip(),
            'Publisher': response.css('div.content ul li').re_first(r'<b>Publisher:</b>.*\(')[18:-1].strip(),
            'Time':  response.css('span.a-text-normal::text').re_first(r'[A-Za-z]+\s[0-9]+,\s[0-9]+'),
            'Language': response.css('div.content ul li').re_first(r'<b>Language:</b>.*')[17:-5],
        }