import json
import requests
import execjs
import re
import pandas as pd
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

class apple():
    headers = {
        'Cookie': 'acw_tc=76b20fee15751692420521540e2fad27598044d9ed521c364eeb58695433e8; PHPSESSID=q00duvabfu57i1d30ga8loeqc1; qm_check=SxJXQEUSChdwXV9eXFEYY0dZVkRjWFRTV0IbHBZbWFVTWxIKEgUbAhwJHAQUARJN; Hm_lvt_ff3eefaf44c797b33945945d0de0e370=1575169245; gr_user_id=eb64614f-42be-4b91-a1c9-502c2237cc9e; grwng_uid=459b9147-9bdf-4d03-b69a-a12ac87aff5f; __guid=44926452.3402173988784446000.1575170643700.4597; monitor_count=2; Hm_lpvt_ff3eefaf44c797b33945945d0de0e370=1575187713; synct=1575190672.964; syncd=-2335',
        'Referer': 'https://www.qimai.cn/rank/index/brand/free/device/iphone/country/jp/genre/6017',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    # 用execjs运行七麦数据js文件，破解analysis参数
    def analysis_parser(self,data, url):
        with open('七麦数据.js', 'r', encoding='utf-8') as f:
            myjs = f.read()
            ctx = execjs.compile(myjs)
            new_pwd = ctx.call('getAnalysis', list(data.values()), url)
            # print(new_pwd)
        return new_pwd
    # 获取app相关数据
    def get_app_data(self,brand, device, country, genre, date, page, data_dict):
        data = {
            'brand': brand,
            'device': device,
            'country': country,
            'genre': genre,
            'date': date,
            'page': page,
            'is_rank_index': '1'
        }
        params = {
            'analysis': self.analysis_parser(data, url='/rank/index'),
            'brand': data['brand'],
            'device': data['device'],
            'country': data['country'],
            'genre': data['genre'],
            'date': data['date'],
            'page': data['page'],
            'is_rank_index': data['is_rank_index']
        }
        # print(params)
        res = requests.get(
            url='https://api.qimai.cn/rank/index',
            params=params,
            headers=apple.headers
        )
        html = res.text
        html = html.encode('utf-8').decode('unicode_escape')
        html = json.loads(html)
        print("apple:",html)
        rankInfo = html['rankInfo']
        for one in rankInfo:
            appId = one['appInfo']['appId']  # app_id
            appName = one['appInfo']['appName']  # app名称
            comment_rating = one['comment']['rating']  # 分数
            comment_num = one['comment']['num']  # 评分数量
            rank_b = one['rank_b']['ranking']  # 总榜排名
            rank_b_change = one['rank_b']['change']  # 总榜排名变化
            rank_c = one['rank_c']['ranking']  # 分类排名
            lastReleaseTime = one['lastReleaseTime']  # 更新日期
            #print(appId)
            data_dict['分类排名'].append(rank_c)
            data_dict['app名称'].append(appName)
            data_dict['更新日期'].append(lastReleaseTime)
            data_dict['分数'].append(comment_rating)
            data_dict['总榜排名'].append(rank_b)
            data_dict['总榜排名变化'].append(rank_b_change)

    def shuchu(self,date):

        data_dict1 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='5000',
                    date=date,
                    page=str(page),
                    data_dict=data_dict1,
                )
            except:
                pass
            # pd.DataFrame(data_dict).to_excel('h.xlsx', sheet_name="Sheet2",index=False, encoding='utf-8')
            df1 = pd.DataFrame(data_dict1)
            # 获取ExcelWriter对象
            # writer = pd.ExcelWriter('')
            writer = pd.ExcelWriter(r'苹果商店\苹果商店.xlsx')
            # 将df1与df2写入writer中
            df1.to_excel(writer, sheet_name='全部应用', index=False, encoding='utf-8')




        data_dict2 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6000',
                    date=date,
                    page=str(page),
                    data_dict=data_dict2,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict2)
            df1.to_excel(writer, sheet_name='商务', index=False, encoding='utf-8')



        data_dict3 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6001',
                    date=date,
                    page=str(page),
                    data_dict=data_dict3,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict3)
            df1.to_excel(writer, sheet_name='天气', index=False, encoding='utf-8')



        data_dict4 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6002',
                    date=date,
                    page=str(page),
                    data_dict=data_dict4,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict4)
            df1.to_excel(writer, sheet_name='工具', index=False, encoding='utf-8')




        data_dict5 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6003',
                    date=date,
                    page=str(page),
                    data_dict=data_dict5,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict5)
            df1.to_excel(writer, sheet_name='旅游', index=False, encoding='utf-8')




        data_dict6 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6004',
                    date=date,
                    page=str(page),
                    data_dict=data_dict6,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict6)
            df1.to_excel(writer, sheet_name='体育', index=False, encoding='utf-8')



        data_dict7 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6005',
                    date=date,
                    page=str(page),
                    data_dict=data_dict7,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict7)
            df1.to_excel(writer, sheet_name='社交', index=False, encoding='utf-8')



        data_dict8 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6006',
                    date=date,
                    page=str(page),
                    data_dict=data_dict8,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict8)
            df1.to_excel(writer, sheet_name='参考', index=False, encoding='utf-8')



        data_dict9 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6007',
                    date=date,
                    page=str(page),
                    data_dict=data_dict9,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict9)
            df1.to_excel(writer, sheet_name='效率', index=False, encoding='utf-8')



        data_dict10 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6008',
                    date=date,
                    page=str(page),
                    data_dict=data_dict10,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict10)
            df1.to_excel(writer, sheet_name='摄影与录像', index=False, encoding='utf-8')



        data_dict11 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6009',
                    date=date,
                    page=str(page),
                    data_dict=data_dict11,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict11)
            df1.to_excel(writer, sheet_name='新闻', index=False, encoding='utf-8')



        data_dict12 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6010',
                    date=date,
                    page=str(page),
                    data_dict=data_dict12,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict12)
            df1.to_excel(writer, sheet_name='导航', index=False, encoding='utf-8')



        data_dict13 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6011',
                    date=date,
                    page=str(page),
                    data_dict=data_dict13,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict13)
            df1.to_excel(writer, sheet_name='音乐', index=False, encoding='utf-8')



        data_dict14 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6012',
                    date=date,
                    page=str(page),
                    data_dict=data_dict14,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict14)
            df1.to_excel(writer, sheet_name='生活', index=False, encoding='utf-8')



        data_dict15 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6013',
                    date=date,
                    page=str(page),
                    data_dict=data_dict15,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict15)
            df1.to_excel(writer, sheet_name='健康健美', index=False, encoding='utf-8')



        data_dict16 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6015',
                    date=date,
                    page=str(page),
                    data_dict=data_dict16,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict16)
            df1.to_excel(writer, sheet_name='财务', index=False, encoding='utf-8')



        data_dict17 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6016',
                    date=date,
                    page=str(page),
                    data_dict=data_dict17,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict17)
            df1.to_excel(writer, sheet_name='娱乐', index=False, encoding='utf-8')



        data_dict18 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6017',
                    date=date,
                    page=str(page),
                    data_dict=data_dict18,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict18)
            df1.to_excel(writer, sheet_name='教育', index=False, encoding='utf-8')



        data_dict19 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6018',
                    date=date,
                    page=str(page),
                    data_dict=data_dict19,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict19)
            df1.to_excel(writer, sheet_name='图书', index=False, encoding='utf-8')



        data_dict20 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6020',
                    date=date,
                    page=str(page),
                    data_dict=data_dict20,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict20)
            df1.to_excel(writer, sheet_name='医疗', index=False, encoding='utf-8')



        data_dict21 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6021',
                    date=date,
                    page=str(page),
                    data_dict=data_dict21,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict21)
            df1.to_excel(writer, sheet_name='报刊杂志', index=False, encoding='utf-8')



        data_dict22 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6023',
                    date=date,
                    page=str(page),
                    data_dict=data_dict22,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict22)
            df1.to_excel(writer, sheet_name='美食佳饮', index=False, encoding='utf-8')



        data_dict23 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6024',
                    date=date,
                    page=str(page),
                    data_dict=data_dict23,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict23)
            df1.to_excel(writer, sheet_name='购物', index=False, encoding='utf-8')


        data_dict24 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6026',
                    date=date,
                    page=str(page),
                    data_dict=data_dict24,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict24)
            df1.to_excel(writer, sheet_name='软件开发工具', index=False, encoding='utf-8')



        data_dict25 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6027',
                    date=date,
                    page=str(page),
                    data_dict=data_dict25,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict25)
            df1.to_excel(writer, sheet_name='图形和设计', index=False, encoding='utf-8')


        data_dict26 = {
            '分类排名': [], 'app名称': [], '更新日期': [], '分数': [], '总榜排名': [], '总榜排名变化': [],
        }
        # 未登录只能看前4页200条数据
        for page in range(1, 5):
            try:
                self.get_app_data(
                    brand='free',
                    device='iphone',
                    country='cn',
                    genre='6061',
                    date=date,
                    page=str(page),
                    data_dict=data_dict26,
                )
            except:
                pass
            df1 = pd.DataFrame(data_dict26)
            df1.to_excel(writer, sheet_name='儿童', index=False, encoding='utf-8')









        # 保存writer
        writer.save()
        writer.close()

