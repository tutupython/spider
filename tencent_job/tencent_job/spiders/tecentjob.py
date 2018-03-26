# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tencent_job.items import TencentJobItem

class TecentjobSpider(CrawlSpider):
    name = 'jobspider'
    allowed_domains = ['tencent.com']
    start_urls = ["http://hr.tencent.com/position.php?&start=0#a"]
    # Response里链接的提取规则，返回的符合匹配规则的链接匹配对象的列表
    pagelink=LinkExtractor(allow=("start=\d+"))

    rules = [
        # 获取这个列表里的链接，依次发送请求，并且继续跟进，调用指定回调函数处理
        Rule(pagelink, callback="parseTencent", follow=True)
    ]


    def parseTencent(self, response):
        item=TencentJobItem()
        job_list=response.xpath("//tr[@class='even' or @class='odd']")
        # job_list=response.xpath(".//tr[contains(@class,'even') or contains(@class,'odd')]")
        # print(job_list.extract())
        # print(type(job_list))
        # print(job_list[0].xpath(".//td[3]/text()").extract()[0])
        # # 职位名
        # positionname = scrapy.Field()
        # # 详情连接
        # positionlink = scrapy.Field()
        # # 职位类别
        # positionType = scrapy.Field()
        # # 招聘人数
        # peopleNum = scrapy.Field()
        # # 工作地点
        # workLocation = scrapy.Field()
        # # 发布时间
        # publishTime = scrapy.Field()
        for job in job_list:
            item['positionname']=job.xpath(".//td[1]/a/text()").extract()[0]
            item['positionlink']=job.xpath(".//td[1]/a/@href").extract()[0]
            item['positionType']=job.xpath(".//td[2]/text()").extract()[0]
            item['peopleNum'] = job.xpath(".//td[3]/text()").extract()[0]
            item['workLocation'] = job.xpath(".//td[4]/text()").extract()[0]
            item['publishTime'] = job.xpath(".//td[5]/text()").extract()[0]
            yield item
