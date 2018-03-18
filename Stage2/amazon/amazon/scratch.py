nextpage = response.css('a[title*="Next Page"]::attr(href)').extract_first()

response.urljoin(nextpage)


bookpage = response.css('a[class*="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]::attr(href)').extract()

booktitle = response.css('a[class*="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]::attr(title)').extract()

author = response.css('td.a-size-base div.a-row span.a-size-medium::text').extract_first().strip()
booktitle = response.css('span[id*="productTitle"]::text').extract_first()
publisher = response.css('div.content ul li').re_first(r'<b>Publisher:</b>.*\(')[18:-1].strip()
time = response.css('span.a-text-normal::text').re_first(r'[A-Za-z]+\s[0-9]+,\s[0-9]+')
Language = response.css('div.content ul li').re_first(r'<b>Language:</b>.*')[17:-5]

import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }
"""This spider will start from the main page, it will follow all the links to the authors pages calling the parse_author callback for each of them, and also the pagination links with the parse callback as we saw before.

Here we’re passing callbacks to response.follow as positional arguments to make the code shorter; it also works for scrapy.Request.

The parse_author callback defines a helper function to extract and cleanup the data from a CSS query and yields the Python dict with the author data.

Another interesting thing this spider demonstrates is that, even if there are many quotes from the same author, we don’t need to worry about visiting the same author page multiple times. By default, Scrapy filters out duplicated requests to URLs already visited, avoiding the problem of hitting servers too much because of a programming mistake. This can be configured by the setting DUPEFILTER_CLASS.

Hopefully by now you have a good understanding of how to use the mechanism of following links and callbacks with Scrapy.

As yet another example spider that leverages the mechanism of following links, check out the CrawlSpider class for a generic spider that implements a small rules engine that you can use to write your crawlers on top of it.

Also, a common pattern is to build an item with data from more than one page, using a trick to pass additional data to the callbacks."""