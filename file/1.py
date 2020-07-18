import json
import requests
import execjs
import re
import pandas as pd
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE


# 用execjs运行七麦数据js文件，破解analysis参数
def analysis_parser(data, url):
    with open('七麦数据.js', 'r', encoding='utf-8') as f:
        myjs = f.read()
        ctx = execjs.compile(myjs)
        new_pwd = ctx.call('getAnalysis', list(data.values()), url)
        #print(new_pwd)
    return new_pwd


# 获取APP支持的语言和应用描述
'''
def get_app_des(app_id,country):
    data={
        'appid':app_id,
        'country':country
    }
    params={
        'analysis':analysis_parser(data,url='/app/baseinfo'),
        'appid': data['appid'],
        'country': data['country']
    }
    res=requests.get(
        url='https://api.qimai.cn/app/baseinfo',
        params=params,
        headers=headers
    )
    html=res.text
    html = json.loads(html)
    # print(html)
    description=html['description']
    description=re.sub(r'<br />','',description)
    description = ILLEGAL_CHARACTERS_RE.sub(r'', description)
    appinfo=str(html['appInfo'])
    try:
        yy=re.findall(r"'name': '支持语言', 'value': '(.*?)'}",appinfo)[0]
    except:
        yy=''
    try:
        start_date = re.findall(r"'name': '发布日期', 'value': '(.*?)'}", appinfo)[0]
    except:
        start_date=''
    return (yy,description,start_date)
'''


# 获取app相关数据
def get_app_data(market, category, date, page):
    data = {
        'market': market,
        'category': category,
        'date': date,
        'page': page,
        'is_rank_index': '1'
    }
    params = {
        'analysis': analysis_parser(data, url='/rank/marketRank'),
        'market': data['market'],
        'category': data['category'],
        'date': data['date'],
        'page': data['page'],
        'is_rank_index': data['is_rank_index']
        # 'market': '6',
        # 'category': '6',  # 写一个小分类换成6
        # 'date': '2020-07-09'
    }
    #print(params)
    res = requests.get(
        url='https://api.qimai.cn/rank/marketRank',
        params=params,
        headers=headers
    )
    html = res.text
    html = html.encode('utf-8').decode('unicode_escape')
    html = json.loads(html)
    print(html)

    # 整理1111111111111111111111111111111111111111111111111111111111111111111111111
    rankInfo=html['rankInfo']
    for one in rankInfo:
        appId=one['appInfo']['appId']   #app_id
        appName = one['appInfo']['appName']   #app名称
        rank = one['rankInfo']['ranking']
        change= one['rankInfo']['change']
        downloadNum = one['downloadNum']
        genre = one['rankInfo']['genre']
        score= one['appInfo']['app_comment_score']
        publisher = one['appInfo']['publisher']
        releaseTime=one['releaseTime']   #更新日期


        # comment_rating=one['comment']['rating']   #分数
        # comment_num = one['comment']['num']     #评分数量
        # rank_b=one['rank_b']['ranking']   #总榜排名
        # rank_c = one['rank_c']['ranking']  # 分类排名
        print("appName:",appName)
        # data_dict['分类排名'].append(rank_c)
        data_dict['app名称'].append(appName)
        data_dict['排名'].append(rank)
        data_dict['排名变化'].append(change)
        data_dict['新增下载量'].append(downloadNum)
        data_dict['类别'].append(genre)
        data_dict['评分'].append(score)
        data_dict['公司'].append(publisher)
        data_dict['更新日期'].append(releaseTime)




        # data_dict['支持语言'].append(yy)
        # data_dict['发布日期'].append(start_date)
        # data_dict['更新日期'].append(lastReleaseTime)
        # data_dict['分数'].append(comment_rating)
        # data_dict['总榜排名'].append(rank_b)
        # data_dict['app描述'].append(app_description)
if __name__ == '__main__':
    headers = {
        'Cookie': 'acw_tc=76b20fee15751692420521540e2fad27598044d9ed521c364eeb58695433e8; PHPSESSID=q00duvabfu57i1d30ga8loeqc1; qm_check=SxJXQEUSChdwXV9eXFEYY0dZVkRjWFRTV0IbHBZbWFVTWxIKEgUbAhwJHAQUARJN; Hm_lvt_ff3eefaf44c797b33945945d0de0e370=1575169245; gr_user_id=eb64614f-42be-4b91-a1c9-502c2237cc9e; grwng_uid=459b9147-9bdf-4d03-b69a-a12ac87aff5f; __guid=44926452.3402173988784446000.1575170643700.4597; monitor_count=2; Hm_lpvt_ff3eefaf44c797b33945945d0de0e370=1575187713; synct=1575190672.964; syncd=-2335',
        'Referer': 'https://www.qimai.cn/rank/index/brand/free/device/iphone/country/jp/genre/6017',
        # 'Referer':'https://www.qimai.cn/rank/marketRank',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    data_dict = {
        'app名称': [],'排名': [],'排名变化': [],'新增下载量': [],'类别': [],'评分': [],'公司': [],'更新日期': [],
    }
    # 未登录只能看前4页200条数据
    for page in range(1, 2):
        try:
            get_app_data(
                market='6',
                category='6',
                date='2020-07-08',
                page=str(page),
            )
        except:
            pass
       # pd.DataFrame(data_dict).to_excel('h.xlsx', sheet_name="Sheet2",index=False, encoding='utf-8')
        df1=pd.DataFrame(data_dict)
        # 获取ExcelWriter对象
        writer = pd.ExcelWriter('h.xlsx')
        # 将df1与df2写入writer中
        df2 = df1.copy()
        df1.to_excel(writer, sheet_name='Sheet_name_1',index=False, encoding='utf-8')
        df2.to_excel(writer, sheet_name='Sheet_name_2',index=False, encoding='utf-8')
        # 保存writer
        writer.save()
        writer.close()