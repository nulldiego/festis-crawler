# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import hashlib
import types
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


class FestisPipeline(object):
    def process_item(self, item, spider):
        return item
		
class ElasticSearchAWSPipeline(object):
    settings = None
    es = None

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings

        awsAccountId = ""
        awsSecretKey = ""
        awsEndpoint = ""
        awsRegion = ""

        if (ext.settings['ELASTICSEARCH_AWS_ACCOUNTID']):
            awsAccountId = ext.settings['ELASTICSEARCH_AWS_ACCOUNTID']

        if (ext.settings['ELASTICSEARCH_AWS_SECRETKEY']):
            awsSecretKey = ext.settings['ELASTICSEARCH_AWS_SECRETKEY']

        if (ext.settings['ELASTICSEARCH_AWS_ENDPOINT']):
            awsEndpoint = ext.settings['ELASTICSEARCH_AWS_ENDPOINT']

        if (ext.settings['ELASTICSEARCH_AWS_REGION']):
            awsRegion = ext.settings['ELASTICSEARCH_AWS_REGION']

        host = awsEndpoint
        auth = AWS4Auth(awsAccountId, awsSecretKey, awsRegion, 'es')
        ext.es = Elasticsearch(
            hosts=[{'host': host, 'port': 443}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
        return ext

    def index_item(self, item):
        if self.settings.get('ELASTICSEARCH_AWS_UNIQ_KEY'):
            uniq_key = self.settings.get('ELASTICSEARCH_AWS_UNIQ_KEY')
            local_id = hashlib.sha1(item[uniq_key]).hexdigest()
            log.msg("Generated unique key %s" % local_id, level=self.settings.get('ELASTICSEARCH_AWS_LOG_LEVEL'))
            op_type = 'index'
        else:
            op_type = 'create'
            local_id = hashlib.sha1(item['url'].encode('utf-8')).hexdigest()

        self.es.index(body=dict(item),
                      index=self.settings.get('ELASTICSEARCH_INDEX'),
                      doc_type='doc',
                      id=local_id,
                      op_type=op_type)


    def process_item(self, item, spider):
        self.index_item(item)
        log.msg("Item sent to Elastic Search %s" %
                (self.settings.get('ELASTICSEARCH_INDEX')),
                level=self.settings.get('ELASTICSEARCH_LOG_LEVEL'), spider=spider)
        return item