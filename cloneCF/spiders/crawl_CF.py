import scrapy
from cloneCF.items import UserInfoItem


class CrawlCfSpider(scrapy.Spider):
    name = "crawl_CF"
    allowed_domains = ["codeforces.com"]
    start_urls = [
        "https://codeforces.com/ratings/"
    ]

    custom_settings = {
        'FEEDS' : {
            'userdata.json' : {'format' : 'json', 'overwrite' : True},
        }
    }

    def parse(self, response):
        users = response.xpath("//table[@class='']/tr/td").css("a::attr(href)")

        print(len(users))

        for user in users :
            relate_url =  user.get()

            if relate_url is not None  and 'profile' in relate_url :
                if relate_url[0] == "/" :
                    user_url = "https://codeforces.com" + relate_url
                else :
                    user_url = "https://codeforces.com/" + relate_url

                yield response.follow(user_url, callback = self.parse_user_info)


        next_page = response.xpath("//div[@class='pagination']/ul/li")[-1].css('a::attr(href)').get()
        
        if next_page is not None and '2' not in next_page:
            if next_page[0] == '/' : 
                next_page_url = "https://codeforces.com" + next_page
            else :
                next_page_url = "https://codeforces.com/" + next_page

            yield {
                'next_page' : next_page_url,
            }

            yield response.follow(next_page_url, callback = self.parse)

    def parse_user_info(self, response) :
        class_list = ['main-info']    
        divs = response.xpath('//div[contains(@class, "{}")]'.format(' | '.join(class_list)))
        user_name = divs.xpath("//h1/a/@href").get().split('/')[-1]

        userInfo = UserInfoItem()
        
        userInfo['user_name'] = response.xpath('//div[contains(@class, "{}")]'.format(' | '.join(class_list))).xpath("//h1/a/@href").get().split('/')[-1]
        userInfo['current_rank'] = response.xpath("//div[@class='user-rank']/span/text()").get()
        userInfo['contests'] = ""

        # parse_contests(self, userInfo, response)
        contests_url = response.xpath("//div[@id='pageContent']/div/ul/li/a/@href")[-2].get()

        yield userInfo
        
    def parse_contests(self, response) :
        yield "ass"