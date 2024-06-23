import scrapy

class AtpSpiderSpider(scrapy.Spider):
    name = "atp_spider"
    allowed_domains = ["atptour.com"]
    start_urls = ["https://www.atptour.com/es/rankings/singles"]

    def start_requests(self):
        headers = {'Accept-Language': 'es-ES,es;q=0.9'}
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        #Mediante selector CSS
        for tenista in response.css('tr'): 
            ranking = tenista.css('.rank-cell border-left-4 border-right-dash-1::text').get()
            nombre = tenista.css(".player-cell border-left-dash-1 border-right-dash-1 span.player-cell-wrapper::text").get()
            mas_menos_ranking = tenista.css(".move-cell border-right-4 border-left-dash-1 span.move-none::text").get()
            mas_menos_puntos = tenista.css(".points-move-cell border-right-dash-1 span.move-down::text").get()
            print("-----")
            print(ranking,"\n")
            print(nombre,"\n")
            print(mas_menos_ranking,"\n")
            print(mas_menos_puntos,"\n")