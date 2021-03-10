import json

import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import CsobskItem
from itemloaders.processors import TakeFirst

base = 'https://www.csob.sk/delegate/getNewsDetail?ID={}'


class CsobskSpider(scrapy.Spider):
	name = 'csobsk'
	start_urls = ['https://www.csob.sk/o-nas/novinky']

	def parse(self, response):
		list_of_id = response.xpath('//div[contains(@id, "entryId")]/@id').getall()
		for _id in list_of_id:
			_id_num = _id.split('=')[1]
			url = base.format(_id_num)
			yield scrapy.Request(url, callback=self.parse_post)


	def parse_post(self, response):
		data = json.loads(response.text)
		title = data['title']
		description = remove_tags(data['newsDetailContent'])
		date = data['displayDate']


		item = ItemLoader(item=CsobskItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
