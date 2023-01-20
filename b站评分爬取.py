import json
import requests

all_score = 0
rshu = 0
cps = 0
dps = 0
fb = [0,0,0,0,0]
番剧id = 4315402
url = f'https://www.bilibili.com/bangumi/media/md{番剧id}/'
long_url = f'https://api.bilibili.com/pgc/review/long/list?media_id={番剧id}&ps=20&sort=0'
short_url = f'https://api.bilibili.com/pgc/review/short/list?media_id={番剧id}&ps=20&sort=0'
base_long_url = long_url + '&cursor={next}'
base_short_url = short_url + '&cursor={next}'

def gzshorturl(next):#构造短url
    request_url = base_short_url.format(next=next)
    return request_url
def gzlongurl(next):#构造长url
    request_url = base_long_url.format(next=next)
    return request_url
def pqhtml(url):#爬取页面代码
    return requests.get(url).text
def dqshuju(data,lx):#读取打印每条评论的评分
    global all_score,rshu,cps,dps,fb,uid
    if lx == 'long':
        for a in data['data']['list']:
            score = a['score']
            fb[int(score / 2 - 1)] += 1
            all_score += score
            rshu += 1
            cps += 1
            print(f'第{cps}条长评，评分为：{score}')
            print(f'当前平均分为：{all_score / rshu}')
            print(f'评分分布：{fb}')
    elif lx == 'short':
        for a in data['data']['list']:
            score = a['score']
            fb[int(score / 2 - 1)] += 1
            all_score += score
            rshu += 1
            dps += 1
            print(f'第{dps}条短评，评分为：{score}')
            print(f'当前平均分为：{all_score / rshu}')
            print(f'评分分布：{fb}')
    return dqjdain(data)
def dqjdain(data):#查找下一跳地址
    return data['data']['next']

first_long_data = json.loads(pqhtml(long_url))
first_short_data = json.loads(pqhtml(short_url))

long_next = dqshuju(first_long_data,'long')
while True:
    long_data = json.loads(pqhtml(gzlongurl(long_next)))
    long_next = dqshuju(long_data,'long')
    if long_next == 0:
        break
short_next = dqshuju(first_short_data,'short')
while True:
    short_data = json.loads(pqhtml(gzshorturl(short_next)))
    short_next = dqshuju(short_data,'short')
    if short_next == 0:
        break

print(f'总平均分：{all_score / rshu}，共{rshu}条评价。')
print(f'评分分布：{fb}')
