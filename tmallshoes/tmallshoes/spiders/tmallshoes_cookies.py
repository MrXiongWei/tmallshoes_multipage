# -*- coding: utf-8 -*-
import re
import time
from http.cookiejar import Cookie

import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from scrapy.http import Request

from tmallshoes import settings
from tmallshoes.items import TmallshoesItem


class TmallshoesSpider(scrapy.Spider):
    name = 'tmallshoes'
    headers = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        # 'Host': 'www.tmall.com',
        'Referer': 'https://www.tmall.com',
        "Connection": "keep-alive",
        # 'cookie': 'cna=Ze4oFLh36l8CAcotgbYrKvGF; hng=""; uc1=cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie21=UIHiLt3xSixwG45%2Bs3wzsA%3D%3D&cookie15=VT5L2FSpMGV7TQ%3D%3D&existShop=false&pas=0&cookie14=UoTfI8hZdEwraw%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByRqsBLP%2Ft3JS8AI%3D&id2=UNX6wDxbEN0L&nk2=G5eKtUAq%2Fig%3D&lg2=W5iHLLyFOGW7aA%3D%3D; tracknick=xwzjying; _l_g_=Ug%3D%3D; ck1=""; unb=351217137; lgc=xwzjying; cookie1=AiazX8pkl9KOKD%2B69Bi96Yl6pyc8UHFmM%2F6gE5ckkno%3D; login=true; cookie17=UNX6wDxbEN0L; cookie2=1b8a6a526b9ecdf4f4f6b34716b989a8; _nk_=xwzjying; t=926417a4ee0279222faadf60e4a33846; uss=""; csg=3f8d06c0; skt=beea767dde628820; _tb_token_=e4e7e31e535b6; cq=ccp%3D0; _m_h5_tk=44214b2807f6bc66026532ea2e0ba568_1538972935334; _m_h5_tk_enc=a51896692044700f377f65542350d013; enc=MIbudnN%2F9HNIqm9dTbP3%2B%2B8zh6r36WvgWTAbIg0Ko9CqGnr8rb6fpgT2VAjC1v8%2Fc%2BR9S9kFe5a8X5iyrG8RMg%3D%3D; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; isg=BBcXIuvbANRd9oRAWRBkhWxKpotrXOnPH7VFLmlEbeZNmDfacCxAD0Sy_ngjcMM2',
        'if-none-match': 'W/"38306-3Uat7IhXrGleqyDKn6S1xyinXgk"',
        'X-XHR-Referer': 'https://www.tmall.com'
    }
    cookies = {
        '_cc_': 'WqG3DMC9EA%3D%3D',
        '_l_g_': 'Ug%3D%3D',
        '_m_h5_tk': '44214b2807f6bc66026532ea2e0ba568_1538972935334',
        '_m_h5_tk_enc': 'a51896692044700f377f65542350d013',
        '_nk_': 'xwzjying',
        '_tb_token_': 'e4e7e31e535b6',
        'atpsida': 'd886d1fb7e71579759cbf05d_1538975874_1',
        'aui': '351217137',
        'cdpid': 'UNX6wDxbEN0L',
        'ck1': '',
        'cna': 'Ze4oFLh36l8CAcotgbYrKvGF',
        'cnaui': '351217137',
        'cookie1': 'AiazX8pkl9KOKD%2B69Bi96Yl6pyc8UHFmM%2F6gE5ckkno%3D',
        'cookie17': 'UNX6wDxbEN0L',
        'cookie2': '1b8a6a526b9ecdf4f4f6b34716b989a8',
        'cq': 'ccp%3D0',
        'csg': '3f8d06c0',
        'dnk': 'xwzjying',
        'enc': 'MIbudnN%2F9HNIqm9dTbP3%2B%2B8zh6r36WvgWTAbIg0Ko9CqGnr8rb6fpgT2VAjC1v8%2Fc%2BR9S9kFe5a8X5iyrG8RMg%3D%3D',
        'existShop': 'MTUzODk2NDI4NA%3D%3D',
        'hng': '',
        'isg': 'BFVVgG4Poi74i4ZS_IrqOkjMZFEFUgsVCYPHpNf6F0wbLnUgn6MRNHzn_HI9LiEc',
        'isg': 'BBcXIuvbANRd9oRAWRBkhWxKpotrXOnPH7VFLmlEbeZNmDfacCxAD0Sy_ngjcMM2',
        'l': 'AkpKJONjxKxWUSisLu/9t-PMGjvstM6V',
        'lgc': 'xwzjying',
        'login': 'TRUE',
        'mt': 'np=',
        'otherx': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0',
        'publishItemObj': 'Ng%3D%3D',
        'sca': '23d49ea8',
        'sg': 'g78',
        'skt': 'beea767dde628820',
        't': '926417a4ee0279222faadf60e4a33846',
        'tbsa': '4fca4f026b4e1142717d471e_1538964284_6',
        'tg': '0',
        'tracknick': 'xwzjying',
        'uc1': 'cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=W5iHLLyFfXVRDP8mxoRA8A%3D%3D&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&existShop=false&pas=0&cookie14=UoTfI8hZdEwraw%3D%3D&tag=8&lng=zh_CN',
        'uc1': 'cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie21=UIHiLt3xSixwG45%2Bs3wzsA%3D%3D&cookie15=VT5L2FSpMGV7TQ%3D%3D&existShop=false&pas=0&cookie14=UoTfI8hZdEwraw%3D%3D&tag=8&lng=zh_CN',
        'uc3': 'vt3=F8dByRqsBLP%2Ft3JS8AI%3D&id2=UNX6wDxbEN0L&nk2=G5eKtUAq%2Fig%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D',
        'uc3': 'vt3=F8dByRqsBLP%2Ft3JS8AI%3D&id2=UNX6wDxbEN0L&nk2=G5eKtUAq%2Fig%3D&lg2=W5iHLLyFOGW7aA%3D%3D',
        'unb': '351217137',
        'uss': '',
        'v': '0'
    }

    def __init__(self):
        super(TmallshoesSpider, self).__init__()
        self.start_urls = ['https://www.tmall.com']
        self.allowed_domain = ['.tmall.com']
        # 设置webdriver启动参数
        '''
        option = webdriver.ChromeOptions()
        option.add_argument(settings.option_headless)
        option.add_argument(settings.option_gpu)
        option.add_argument(settings.USER_AGENT)
        self.browser = webdriver.Chrome(executable_path=settings.executable_path, chrome_options=option)
        # self.browser.set_page_load_timeout(10)
        '''
        self.browser = webdriver.Chrome(executable_path=settings.executable_path)

        self.wait = WebDriverWait(self.browser, settings.wait_time)
        dispatcher.connect(self.spider_closed,
                           signals.spider_closed)  # 第二个参数是信号（spider_closed:爬虫关闭信号，信号量有很多）,第一个参数是当执行第二个参数信号时候要执行的方法

    def spider_closed(self, spider):
        # 当爬虫退出的时候关闭chrome
        print('spider closed')
        self.browser.quit()

    def start_requests(self):
        return [Request("https://www.tmall.com", cookies=self.cookies, headers=self.headers)]

    def parse(self, response):
        url_set = set()
        self.browser.get(response.url)
        self.browser.add_cookie(
            {'name': '_m_h5_tk', 'value': '44214b2807f6bc66026532ea2e0ba568_1538972935334', 'domain': '.tmall.com'})
        self.browser.add_cookie(
            {'name': '_m_h5_tk_enc', 'value': 'a51896692044700f377f65542350d013', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': '_nk_', 'value': 'xwzjying', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': '_nk_', 'value': 'xwzjying', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': '_tb_token_', 'value': 'e4e7e31e535b6', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': '_tb_token_', 'value': 'e4e7e31e535b6', 'domain': '.taobao.com'})
        self.browser.add_cookie(
            {'name': 'atpsida', 'value': 'd886d1fb7e71579759cbf05d_1538975874_1', 'domain': '.mmstat.com'})
        self.browser.add_cookie({'name': 'aui', 'value': '351217137', 'domain': '.mmstat.com'})
        self.browser.add_cookie({'name': 'cdpid', 'value': 'UNX6wDxbEN0L', 'domain': '.mmstat.com'})
        self.browser.add_cookie({'name': 'ck1', 'value': '', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'cna', 'value': 'Ze4oFLh36l8CAcotgbYrKvGF', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'cna', 'value': 'Ze4oFLh36l8CAcotgbYrKvGF', 'domain': '.mmstat.com'})
        self.browser.add_cookie({'name': 'cna', 'value': 'Ze4oFLh36l8CAcotgbYrKvGF', 'domain': '.tanx.com'})
        self.browser.add_cookie({'name': 'cna', 'value': 'Ze4oFLh36l8CAcotgbYrKvGF', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'cnaui', 'value': '351217137', 'domain': '.mmstat.com'})
        self.browser.add_cookie({'name': 'cnaui', 'value': '351217137', 'domain': '.tanx.com'})
        self.browser.add_cookie(
            {'name': 'cookie1', 'value': 'AiazX8pkl9KOKD%2B69Bi96Yl6pyc8UHFmM%2F6gE5ckkno%3D', 'domain': '.taobao.com'})
        self.browser.add_cookie(
            {'name': 'cookie1', 'value': 'AiazX8pkl9KOKD%2B69Bi96Yl6pyc8UHFmM%2F6gE5ckkno%3D', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'cookie17', 'value': 'UNX6wDxbEN0L', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'cookie17', 'value': 'UNX6wDxbEN0L', 'domain': '.taobao.com'})
        self.browser.add_cookie(
            {'name': 'cookie2', 'value': '1b8a6a526b9ecdf4f4f6b34716b989a8', 'domain': '.taobao.com'})
        self.browser.add_cookie(
            {'name': 'cookie2', 'value': '1b8a6a526b9ecdf4f4f6b34716b989a8', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'cq', 'value': 'ccp%3D0', 'domain': 'www.tmall.com'})
        self.browser.add_cookie({'name': 'csg', 'value': '3f8d06c0', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'csg', 'value': '3f8d06c0', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'dnk', 'value': 'xwzjying', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'enc',
                                 'value': 'MIbudnN%2F9HNIqm9dTbP3%2B%2B8zh6r36WvgWTAbIg0Ko9CqGnr8rb6fpgT2VAjC1v8%2Fc%2BR9S9kFe5a8X5iyrG8RMg%3D%3D',
                                 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'existShop', 'value': 'MTUzODk2NDI4NA%3D%3D', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'hng', 'value': '', 'domain': '.tmall.com'})
        self.browser.add_cookie(
            {'name': 'isg', 'value': 'BFVVgG4Poi74i4ZS_IrqOkjMZFEFUgsVCYPHpNf6F0wbLnUgn6MRNHzn_HI9LiEc',
             'domain': '.taobao.com'})
        self.browser.add_cookie(
            {'name': 'isg', 'value': 'BBcXIuvbANRd9oRAWRBkhWxKpotrXOnPH7VFLmlEbeZNmDfacCxAD0Sy_ngjcMM2',
             'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'l', 'value': 'AkpKJONjxKxWUSisLu/9t-PMGjvstM6V', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'lgc', 'value': 'xwzjying', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'lgc', 'value': 'xwzjying', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'login', 'value': 'TRUE', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'mt', 'value': 'np=', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'otherx', 'value': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0',
                                 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'publishItemObj', 'value': 'Ng%3D%3D', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'sca', 'value': '23d49ea8', 'domain': '.mmstat.com'})
        self.browser.add_cookie({'name': 'sg', 'value': 'g78', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'skt', 'value': 'beea767dde628820', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'skt', 'value': 'beea767dde628820', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 't', 'value': '926417a4ee0279222faadf60e4a33846', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 't', 'value': '926417a4ee0279222faadf60e4a33846', 'domain': '.taobao.com'})
        self.browser.add_cookie(
            {'name': 'tbsa', 'value': '4fca4f026b4e1142717d471e_1538964284_6', 'domain': '.mmstat.com'})
        self.browser.add_cookie({'name': 'tg', 'value': '0', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'tracknick', 'value': 'xwzjying', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'tracknick', 'value': 'xwzjying', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'uc1',
                                 'value': 'cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=W5iHLLyFfXVRDP8mxoRA8A%3D%3D&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&existShop=false&pas=0&cookie14=UoTfI8hZdEwraw%3D%3D&tag=8&lng=zh_CN',
                                 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'uc1',
                                 'value': 'cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie21=UIHiLt3xSixwG45%2Bs3wzsA%3D%3D&cookie15=VT5L2FSpMGV7TQ%3D%3D&existShop=false&pas=0&cookie14=UoTfI8hZdEwraw%3D%3D&tag=8&lng=zh_CN',
                                 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'uc3',
                                 'value': 'vt3=F8dByRqsBLP%2Ft3JS8AI%3D&id2=UNX6wDxbEN0L&nk2=G5eKtUAq%2Fig%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D',
                                 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'uc3',
                                 'value': 'vt3=F8dByRqsBLP%2Ft3JS8AI%3D&id2=UNX6wDxbEN0L&nk2=G5eKtUAq%2Fig%3D&lg2=W5iHLLyFOGW7aA%3D%3D',
                                 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'unb', 'value': '351217137', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'unb', 'value': '351217137', 'domain': '.taobao.com'})
        self.browser.add_cookie({'name': 'uss', 'value': '', 'domain': '.tmall.com'})
        self.browser.add_cookie({'name': 'v', 'value': '0', 'domain': '.taobao.com'})
        self.browser.refresh()
        print(self.browser.get_cookies())
        # 输入查询和排序条件，加载第一页
        input = self.wait.until(
            lambda browser: self.browser.find_element_by_xpath('//*[@id="mq"]')
        )
        input.send_keys(settings.KEY_WORDS)
        # time.sleep(3)
        submit = self.wait.until(
            lambda browser: self.browser.find_element_by_xpath('//*[@id="mallSearch"]/form/fieldset/div/button')
        )
        submit.click()
        time.sleep(2)
        input_price = self.wait.until(
            lambda browser: self.browser.find_element_by_xpath('//*[@id="J_FPrice"]/div[1]/b[1]/input')
        )
        input_price.clear()
        input_price.send_keys(settings.KEY_PRICE)
        time.sleep(2)
        submit_price = self.wait.until(
            lambda browser: self.browser.find_element_by_xpath('//*[@id="J_FPEnter"]')
        )
        submit_price.click()
        time.sleep(2)
        sort = self.wait.until(
            lambda browser: self.browser.find_element_by_xpath('//*[@id="J_Filter"]/a[4]')
        )
        sort.click()
        time.sleep(3)

        # 获取总的页数
        total = self.wait.until(
            lambda browser: self.browser.find_element_by_xpath(
                '//*[@id="content"]/div/div[@class="ui-page"]/div/b[@class="ui-page-skip"]/form')
        )
        total = int(re.compile('(\d+)').search(total.text).group(1))

        # 添加URL到set中
        url_set.add(self.browser.current_url)

        # 点击下一页或者输入页面跳转到指定页面，获取页面URL
        for i in range(2, total + 1):
            next_input = self.wait.until(
                lambda browser: self.browser.find_element_by_xpath(
                    '//*[@id="content"]/div/div[@class="ui-page"]/div/b[@class="ui-page-skip"]/form/input[@name="jumpto"]')
            )
            next_input.clear()
            next_input.send_keys(i)

            next_submit = self.wait.until(
                lambda browser: self.browser.find_element_by_xpath(
                    '//*[@id="content"]/div/div[@class="ui-page"]/div/b[@class="ui-page-skip"]/form/button')
            )
            '''
            next_submit = self.wait.until(
                lambda browser: self.browser.find_element_by_xpath(
                    '//*[@id="content"]/div/div[@class="ui-page"]/div/b[@class="ui-page-num"]/a[@class="ui-page-next"]')
            )
            '''
            next_submit.click()
            time.sleep(3)
            url_set.add(self.browser.current_url)

        with open('url_set.txt', mode='w') as f:
            f.write(repr(url_set))
        for url in url_set:
            # 循环调用Request请求解析页面内容
            yield scrapy.Request(url,
                                 callback=self.parse_content,
                                 headers=self.headers,
                                 cookies=self.browser.get_cookies(),
                                 dont_filter=True)

    def parse_content(self, response):
        # 获取页面商品List
        sites = response.xpath('//*[@id="J_ItemList"]/div[@class="product  "]/div[@class="product-iWrap"]')
        products = []
        for site in sites:
            product = TmallshoesItem()
            title = site.xpath(
                './p[@class="productTitle"]/a/@title').extract()
            product['title'] = [t for t in title]

            link = site.xpath(
                './div[@class="productImg-wrap"]/a/@href').extract()
            product['link'] = ['https:' + l for l in link]

            price = site.xpath(
                './p[@class="productPrice"]/em/text()').extract()
            product['price'] = [p for p in price]

            deal = site.xpath(
                './p[@class="productStatus"]/span/em/text()').extract()
            product['deal'] = [d[:-1] for d in deal]

            shop = site.xpath(
                './div[@class="productShop"]/a/text()').extract()
            product['shop'] = [s.replace('\n', '') for s in shop]

            products.append(product)
        return products
