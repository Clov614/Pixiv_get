import re
import requests
from fake_useragent import UserAgent
import random
import os
import time
from itertools import product

headers = {
            'authority': 'www.pixiv.net',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': UserAgent(verify_ssl=False).random,
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust',  # 防盗链
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'referer':'https://www.pixiv.net/artworks/87255676',  # 防盗链
            'cookie': 'first_visit_datetime_pc=2021-01-25+17%3A52%3A04; p_ab_id=2; p_ab_id_2=7; p_ab_d_id=1222487481; yuid_b=GCWEdSA; __cfduid=d4e70456039de82435bf2d68ec263371a1611638726; __utmz=235335808.1611638731.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.592285702.1611638731; _gid=GA1.2.1754984064.1611638789; device_token=073c94a0dec1fe7a566be55ad2ff83ab; c_type=19; a_type=0; b_type=1; ki_r=; login_ever=yes; __utmc=235335808; ki_s=; __utma=235335808.592285702.1611638731.1611657616.1611664200.4; PHPSESSID=49568357_wQL7nOLgxtsC5sKbz0oVTLarRNmNLqIN; privacy_policy_agreement=2; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=49568357=1^9=p_ab_id=2=1^10=p_ab_id_2=7=1^11=lang=zh=1; tag_view_ranking=OT4SuGenFI~kP7msdIeEU~18NCcMsHl5~jaqkarpwly~bXMh6mBhl8~n87ZpuRDS3~HY55MqmzzQ~lH5YZxnbfC~reR7DUAWuG~kGYw4gQ11Z~gpglyfLkWs~HLWLeyYOUF~azESOjmQSV~RTJMXD26Ak~Lt-oEicbBr~oYAm9klH0r~PTyxATIsK0~tK1rVKwWT5~y489EcSQ8H~fq5m22wNFl~jH0uD88V6F~2bq8SNVWly~j7DYHEocqe~SY1hWzTBSP~SVRsxOS1dp~tO5Om4-52p~rsKgvIMw_U~JdNgKFcAjN~eErTeDrRV4~Js5EBY4gOW~PRLZzOBnry~tr4jG_N1yz~gUIg7nrQgl~RcahSSzeRf~sFPxX8lk4q~aKhT3n4RHZ~D0nMcn6oGk~-StjcwdYwv~jk9IzfjZ6n~92z8RZmGQ6; ki_t=1611638990330%3B1611638990330%3B1611670576819%3B1%3B19; tags_sended=1; categorized_tags=CADCYLsad0~IVwLyT8B6k~RcahSSzeRf~RsIQe1tAR0~bXMh6mBhl8~kP7msdIeEU~mt-cXqHhAM; __utmt=1; __cf_bm=be3692187df7cf718e1bfbf11a7d31dc0bf00119-1611678056-1800-AZLiFR3QWIpm9kfIjrOFBX3QG0ssT9659X5pB2xMSU4rl9EHln8qreQAsZ2AP3dRcGQxXsk/iMiOsWhUo4icbqymA3a+doquASmZ15aASNA4bQjiOg5Yqwsl609jbxlT9Y8DBPKulySuu9qjIGlTP6ciriwisEducqbMO9OPFeDC; __utmb=235335808.77.9.1611678055106',
            # 此处需替换成真实的，换成你自己的cookie
        }

class Pixiv_DownLoad():

    def get_proxy(self):
        result = []
        # 读取代理池ip并随机返回一个
        with open('ip_pool_foreign.txt', 'r') as f:
            for line in f:
                result.append(line.strip('\n'))
        ips = list(filter(None, result))
        proxies = {'http': random.choice(ips)}
        return proxies

    def illust_id(self,p):
        global headers

        params = {
            'mode': 'daily',
            'content': 'illust',
            'p': p,
            'format': 'json',
        }

        url = 'https://www.pixiv.net/ranking.php'  # pixiv插画排行榜url
        totals = []
        proxies = self.get_proxy()
        headers['referer'] = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust'
        try:
            response = requests.get(url=url,headers=headers,params=params,proxies=proxies).json()
            for i in range(50):
                try:
                    target = response['contents'][i]['url']
                    ex = 'https://i.pximg.net/c/240x480/img-master/img(.*?)_p0'  # ex 皆为正则的格式
                    final = re.findall(ex, target)
                    middle = final[0]   # middle 为中间变量随便取的
                    ex2 = '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
                    name = re.search(ex2, middle).group(0)  # 用正则提取出pixivID

                    final_url = f"https://i.pximg.net/img-master/img{final[0]}_p0_master1200.jpg" # 拼接url
                    m = (final_url,name)
                    totals.append(m)

                except IndexError:
                    print('爬取已完成')
        except:
            proxies = self.get_proxy()
            response = requests.get(url=url, headers=headers, params=params, proxies=proxies).json()
            for i in range(50):
                try:
                    target = response['contents'][i]['url']
                    ex = 'https://i.pximg.net/c/240x480/img-master/img(.*?)_p0'  # ex 皆为正则的格式
                    final = re.findall(ex, target)
                    middle = final[0]  # middle 为中间变量随便取的
                    ex2 = '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
                    name = re.search(ex2, middle).group(0)  # 用正则提取出pixivID

                    final_url = f"https://i.pximg.net/img-master/img{final[0]}_p0_master1200.jpg"  # 拼接url
                    m = (final_url, name)
                    totals.append(m)


                except IndexError:
                    print('爬取已完成')
        return totals #返回最终图片url，以及pixivID

    def img_download(self,target_url,name):
        global headers
        path = os.getcwd()
        if not os.path.exists(f"{path}" + "\\\\pic_downloaded"):
            os.mkdir(f"{path}" + "\\\\pic_downloaded")
        file_path = f"{path}" + f"\\pic_downloaded\\{name}.jpg"
        with open(file_path, 'wb+') as f:
            try:
                proxies = self.get_proxy()
                headers['referer'] = f'https://www.pixiv.net/artworks/{name}'
                f.write(requests.get(url=target_url,headers=headers,proxies=proxies).content)
                # time.sleep(random.randint(2,5))
                print('成功下载图片：{}.jpg'.format(name))
            except Exception:
                print('成功下载图片：{}.jpg'.format(name))


download = Pixiv_DownLoad()
for p in range(1, 12):   # 可以修改这里 p 的循环范围（每50张一个p）
    try:
        total = download.illust_id(p=p)
        time.sleep(random.randint(10, 20))  # 随机等待时间
        for target_url,name in total:
            download.img_download(target_url,name)
    except IndexError:
        print('所有图片已爬取完成')
    print(f'循环到第{p}页了哦！')   # p为页码位置，如中途中断可自行修改for循环中的p的范围（左闭右开）






