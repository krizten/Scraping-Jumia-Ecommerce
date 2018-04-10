# Scraping-Jumia-Ecommerce
___________________________
This repository provides a concise explanation on how to export scraped data to MongoDB, MySQL and XLSX using Scrapy. For this example, Scrapy 1.5 was used and you can download it using:
``` $pip install scrapy ```

Also, you can find the documentation [here.](https://docs.scrapy.org/en/latest/ 'Scrapy 1.5.0 Documentation')

On completing the installation, run ``` $pip install -r requirements.txt ``` to install the modules in the requirements.txt file.

Scrapy Project Folder Tree
![Scrapy Project Folder Tree](https://github.com/krisdotcode/Scraping-Jumia-Ecommerce/blob/master/screenshots/FolderTree.PNG)


### 1. Configuring Scrapy to write data to MongoDB
__________________________________________________
Navigate to **settings.py** under the Project directory and edit the Pipeline section as follow:

```
# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Jumia.pipelines.MongoDBPipeline': 300,
}

MONGODB_HOST = 'localhost'   # modify host and port if running hosting is cloud-based.
MONGODB_PORT = 27017
MONGODB_DB = 'laptops_db'
MONGODB_COLLECTION = 'laptops_collection'

```

Once that is done, the next objective is to define the pipeline in **pipelines.py**

```
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.conf import settings


class MongoDBPipeline(object):
    def __init__(self):
        connection = MongoClient(settings['MONGODB_HOST'],
                                 settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

```

And finally, ensure MongoDB is running either on localhost or on the cloud then run ``` $scrapy crawl spider_name ```

**Result:**
![Exported to MongoDB](https://github.com/krisdotcode/Scraping-Jumia-Ecommerce/blob/master/screenshots/mongoDB_screenshot.PNG)
