# -*- coding: utf-8 -*-
import re
import time

import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from tmallshoes import settings
from tmallshoes.items import TmallshoesItem


class TmallshoesSpider(scrapy.Spider):
    name = 'tmallshoes'

    def __init__(self):
        super(TmallshoesSpider, self).__init__()
        self.start_urls = ['https://www.tmall.com']
        self.allowed_domain = ['www.tmall.com']
        # 设置webdriver启动参数
        option = webdriver.ChromeOptions()
        option.add_argument(settings.option_headless)
        option.add_argument(settings.option_gpu)
        option.add_argument(settings.USER_AGENT)
        self.browser = webdriver.Chrome(executable_path=settings.executable_path, chrome_options=option)
        # self.browser.set_page_load_timeout(10)
        self.wait = WebDriverWait(self.browser, settings.wait_time)
        dispatcher.connect(self.spider_closed,
                           signals.spider_closed)  # 第二个参数是信号（spider_closed:爬虫关闭信号，信号量有很多）,第一个参数是当执行第二个参数信号时候要执行的方法

    def spider_closed(self, spider):
        # 当爬虫退出的时候关闭chrome
        print('spider closed')
        self.browser.quit()

    def parse(self, response):
        url_set = set()
        self.browser.get(response.url)
        time.sleep(5)

        '''
        # 模拟登陆
        login_frame = self.wait.until(
            lambda browser: browser.find_element_by_id('J_loginIframe')
        )

        self.browser.switch_to_frame('J_loginIframe')

        to_login = self.wait.until(
            lambda browser: browser.find_element_by_id('J_Quick2Static')
        )
        to_login.click()

        username = self.wait.until(
            lambda browser: browser.find_element_by_id('TPL_username_1')
        )
        username.clear()
        username.send_keys('xwzjying')

        password = self.wait.until(
            lambda browser: browser.find_element_by_id('TPL_password_1')
        )
        password.clear()
        password.send_keys('201310Xiongwei')
        time.sleep(20)
        login = self.wait.until(
            lambda browser: browser.find_element_by_id('J_SubmitStatic')
        )
        login.click()
        '''
        # 输入查询和排序条件，加载第一页
        input = self.wait.until(
            lambda browser: browser.find_element_by_xpath('//*[@id="mq"]')
        )
        input.send_keys(settings.KEY_WORDS)
        submit = self.wait.until(
            lambda browser: browser.find_element_by_xpath('//*[@id="mallSearch"]/form/fieldset/div/button')
        )
        submit.click()
        input_price = self.wait.until(
            lambda browser: browser.find_element_by_xpath('//*[@id="J_FPrice"]/div[1]/b[1]/input')
        )
        input_price.clear()
        input_price.send_keys(settings.KEY_PRICE)
        submit_price = self.wait.until(
            lambda browser: browser.find_element_by_xpath('//*[@id="J_FPEnter"]')
        )
        submit_price.click()

        sort = self.wait.until(
            lambda browser: browser.find_element_by_xpath('//*[@id="J_Filter"]/a[4]')
        )
        sort.click()
        # 获取总的页数
        total = self.wait.until(
            lambda browser: browser.find_element_by_xpath(
                '//*[@id="content"]/div/div[@class="ui-page"]/div/b[@class="ui-page-skip"]/form')
        )
        total = int(re.compile('(\d+)').search(total.text).group(1))

        # 添加URL到set中
        url_set.add(self.browser.current_url)

        # 点击下一页或者输入页面跳转到指定页面，获取页面URL
        for i in range(2, total + 1):
            next_input = self.wait.until(
                lambda browser: browser.find_element_by_xpath(
                    '//*[@id="content"]/div/div[@class="ui-page"]/div/b[@class="ui-page-skip"]/form/input[@name="jumpto"]')
            )
            next_input.clear()
            next_input.send_keys(i)
            next_submit = self.wait.until(
                lambda browser: browser.find_element_by_xpath(
                    '//*[@id="content"]/div/div[@class="ui-page"]/div/b[@class="ui-page-skip"]/form/button')
            )
            '''
            next_submit = self.wait.until(
                lambda browser: browser.find_element_by_xpath(
                    '//*[@id="content"]/div/div[@class="ui-page"]/div/b[@class="ui-page-num"]/a[@class="ui-page-next"]')
            )
          '''
            next_submit.click()
            time.sleep(2)
            # 添加URL到set中
            url_set.add(self.browser.current_url)

        for url in url_set:
            # 循环调用Request请求解析页面内容
            yield scrapy.Request(url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        # 获取页面商品List
        sites = response.xpath('//*[@id="J_ItemList"]/div[@class="product  "]/div[@class="product-iWrap"]')
        products = []
        for site in sites:
            product = TmallshoesItem()
            title = site.xpath(
                './p[@class="productTitle"]/a/@title').extract()
            product['title'] = [t for t in title]
            '''
            for t in title:
                product['title'] = t
            '''
            link = site.xpath(
                './div[@class="productImg-wrap"]/a/@href').extract()
            product['link'] = ['https:' + l for l in link]
            '''
            for l in link:
                product['link'] = 'https:' + l
            '''
            price = site.xpath(
                './p[@class="productPrice"]/em/text()').extract()
            product['price'] = [p for p in price]
            '''
            for p in price:
                product['price'] = p
            '''
            deal = site.xpath(
                './p[@class="productStatus"]/span/em/text()').extract()
            product['deal'] = [d[:-1] for d in deal]
            '''
            for d in deal:
                product['deal'] = d[:-1]
            '''
            shop = site.xpath(
                './div[@class="productShop"]/a/text()').extract()
            product['shop'] = [s.replace('\n', '') for s in shop]
            '''
            for s in shop:
                product['shop'] = s.replace('\n', '')
            '''
            products.append(product)
        return products
