# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

class PyshopOzonParserPipeline:

    def open_spider(self, spider):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(item)
        return item

    def close_spider(self, spider):
        print(self.data)
        print(len(self.data))

