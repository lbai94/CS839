import scrapy

class BarNobSpider(scrapy.Spider):
    name = 'BarNob'

    #fiction, history, fiction in german,health and diet,
    #start_urls = ['https://www.amazon.com/s/ref=lp_9_pg_2?rh=n%3A283155%2Cn%3A%211000%2Cn%3A9&page=2&ie=UTF8&qid=1521357971']
    #start_urls = ['https://www.amazon.com/s/ref=lp_17_pg_2?rh=n%3A283155%2Cn%3A%211000%2Cn%3A17&page=2&ie=UTF8&qid=1521349537']

    #start_urls = ['https://www.amazon.com/s/ref=lp_283155_nr_p_n_feature_nine_bro_1?fst=as%3Aoff&rh=n%3A283155%2Cp_n_feature_nine_browse-bin%3A3291436011&bbn=283155&ie=UTF8&qid=1521358536&rnid=3291435011']
    start_urls = ['https://www.barnesandnoble.com/s/mathematics?_requestid=27757']
    #start_urls = ['https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=books']

    def parse(self, response):
        # follow links to book pages
        book_pages = response.css('a[class="pImageLink "]::attr(href)').extract()
        for href in book_pages:
            #self.count = self.count + 1
            yield response.follow(href, self.parse_book)

        # follow pagination links
        next_pages = response.css('a[class="next-button"]::attr(href)').extract()
        for href in next_pages:

            yield response.follow(response.urljoin(href), self.parse)

    def parse_book(self, response):

        yield {
            'Title': response.css('meta[property="og:title"]::attr(content)').extract_first().strip(),
            'Author': response.css('span[itemprop="author"]::text').extract_first().strip(),
            'Publisher': response.css('a[href*="Ntk=Publisher"]::text').extract_first().strip(),
            'Time':  response.css('tbody tr:nth-of-type(3) td::text').extract_first().strip(),
            'ISBN-13':  response.css('tbody tr:nth-of-type(1) td::text').extract_first().strip(),
            #'Language': response.css('div.content ul li').re_first(r'<b>Language:</b>.*')[17:-5],
        }