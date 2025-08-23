import scrapy
        
class FashionSpider(scrapy.Spider):  
    name = "Fashion"  
    start_urls = ["https://fashionhistory.fitnyc.edu/1450-1459/"]  
  
    def parse(self, response):
        # Extract all text from within article tags  
        article_text = response.css("article *::text").getall()  
        
        # Clean and join the text  
        clean_text = " ".join(text.strip() for text in article_text if text.strip())  
        # scrap chunk wise (div based), and replace fig-x with the caption of those (fig-x) in that chunk
        # fetch all the images and their captions and store it as well
        yield {  
            "article_content": clean_text,  
            "source_url": response.url  
        }