import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    file = open("books.txt","a",encoding="UTF-8")
    page_count = 0
    book_count = 1
    start_urls = [
        'https://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=1&filter_in_stock=1&filter_in_stock=1&page=1'
    ]

    def parse(self, response):
        book_names = response.css("div.name.ellipsis a span::text ").extract()
        author_names = response.css("div.author span a span::text").extract()
        publisher_names = response.css("div.publisher span a span::text").extract()

        i = 0
        while(i  <len(book_names)):
            """yield {
                "book_names"      : book_names[i],
                "author_names"    : author_names[i],
                "publisher_names" : publisher_names[i]
            }"""
            self.file.write("*************************************************************\n")
            #self.file.write(str(self.book_count) + "." + "\n")
            self.file.write("Kitap ismi:" + book_names[i] + "\n")
            self.file.write("Yazar ismi:" + author_names[i] + "\n")
            self.file.write("Yayınevi ismi:" + publisher_names[i] + "\n")
            self.file.write("*************************************************************\n")
            #self.book_count += 1
            i += 1

        next_url = response.css("div.links a.next::attr(href)").extract_first()
        print(next_url)
        self.page_count += 1
        
        if next_url is not None and self.page_count != 5:
            yield scrapy.Request(url=next_url, callback=self.parse)
        else:
            self.file.close()

