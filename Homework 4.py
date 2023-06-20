from pprint import pprint
from lxml import html
import requests
import time

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36'}


mail_url = 'https://news.mail.ru'
response = requests.get(mail_url, headers = header)
response

root = html.fromstring(response.text)
root
news = root.xpath('//div[@class="newsitem newsitem_height_fixed js-ago-wrapper"]')
news

for new in news:
    herf = new.xpath(".//span[@class='cell']/a/@href")
    title = new.xpath(".//span[@class='cell']/a/span/text()")
    source = new.xpath(".//div[@class='newsitem__params']/span[@class='newsitem__param']/text()")
    time_pub = new.xpath(".//div[@class='newsitem__params']/span[@class='newsitem__param js-ago']/@datetime")
    print(f'Новость - {title}\nИсточник - {source}\nСсылка - {herf}\nВремя публикации - {time_pub}')