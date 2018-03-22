import scrapy

class GoogleSpider(scrapy.Spider):
    name = 'google'

    #fiction, history, fiction in german,health and diet,
    start_urls = ['https://www.google.com/search?q=fiction&source=lnms&tbm=bks&sa=X&ved=0ahUKEwjn3or5w4DaAhVNVK0KHWVZCk0Q_AUICigB&biw=1332&bih=637']

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