import scrapy

class ImdbSpiderSpider(scrapy.Spider):
    name = "imdb_spider"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc"]

    def start_requests(self):
        headers = {'Accept-Language': 'es-ES,es;q=0.9'}
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        #Mediante selector CSS
        for pelicula in response.css('div.lister-item.mode-advanced'): 
            titulo = pelicula.css('.lister-item-header a::text').get()
            año = pelicula.css(".lister-item-header span.lister-item-year::text").get()
            genero = pelicula.css("div span.genre::text").get()
            genero = genero.replace(", ", "-")
            print("-----")
            print(titulo,"\n")
            print(año[1:-1])
            print(genero,"\n")
        print('-------------------------------------------')

        #Mediante selector XPath
        for pelicula in response.xpath('//div[@class="lister-item mode-advanced"]'): 
            titulo = pelicula.xpath('.//h3[@class="lister-item-header"]/a/text()').get()
            año = pelicula.xpath('.//h3[@class="lister-item-header"]/span[@class="lister-item-year text-muted unbold"]/text()').get()
            genero = pelicula.xpath('.//span[@class="genre"]/text()').get()
            genero = genero.replace(", ", "-")
            print("-----")
            print(titulo,"\n")
            print(año[1:-1],"\n")
            print(genero,"\n")
    