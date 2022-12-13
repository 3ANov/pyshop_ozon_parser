# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd


# useful for handling different item types with a single interface

class PyshopOzonParserPipeline:

    def open_spider(self, spider):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(item)
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.data)[['os_name', 'os_version']]
        grouped_df = df.groupby("os_name", as_index=False)["os_version"].value_counts(dropna=False)
        grouped_df = grouped_df.sort_values(by=["count"], ascending=False)
        grouped_df.insert(1, "space", "   ")
        grouped_df.insert(3, "-", "-")
        column_header = ['Система', '', 'Версия системы', '', '']
        df_text = grouped_df.to_string(header=column_header, index=False)
        with open('./output/os_version_distribution.txt', "w") as f:
            f.write(df_text)

