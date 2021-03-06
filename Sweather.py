# coding=utf-8
import urllib2
import gzip
import json
import datetime
from StringIO import StringIO
from city import city


# day是json转的字典，n表示与当前日期的相对差值，比如说昨天 n = -1,今天 n = 0
def display_weather(day, n):
    date = datetime.date.today() + datetime.timedelta(n)  # 求出所给日期
    if n < 1:  # 如果传进来的是今天或者昨天，正常换行显示
        print u'日期: ' + str(date)
        # day['high'] = "高温 32℃" , day['low'] = "低温 21℃", 我只要温度值
        print '\t' + day['type'] + ' ' + day['low'].split(' ')[1] + ' ~ ' + day['high'].split(' ')[1]
        try:
            print '\t' + u'风向: ' + day['fengxiang']
            print '\t' + u'风力: ' + day['fengli']
        except:
            print '\t' + u'风向: ' + day['fx']
            print '\t' + u'风力: ' + day['fl']
    else:  # 如果传进来的是明天及以后，单行显示一天所有信息
        print u'日期: ' + str(date),
        print '\t' + '%2s' % day['type'] + ' ' + day['low'].split(' ')[1] + ' ~ ' + day['high'].split(' ')[1],
        print '\t' + u'风向: ' + day['fengxiang'],
        print '\t' + u'风力: ' + day['fengli']


def main():
    print '|--------------------欢迎使用天气查询系统-----------------------|'
    print '|---------------------designed by Snowood-----------------------|'
    cityname = raw_input('你想查哪个城市的天气？\n')
    citycode = city.get(cityname)  # 从city.py文件获取城市的id值
    if citycode:  # 如果查到了id
        url = ('http://wthrcdn.etouch.cn/weather_mini?citykey=%s' % citycode)
        req = urllib2.urlopen(url)
        info = req.info()  # 获取返回头信息
        # print info
        encoding = info.getheader('Content-Encoding')
        content = req.read()
        if encoding == 'gzip':  # 如果网页被gzip压缩，先解压
            buf = StringIO(content)
            gf = gzip.GzipFile(fileobj=buf)
            content = gf.read()
        data = json.loads(content)['data']  # 将json数据转成字典
        ganmao = data['ganmao']

        day = dict()
        for i in range(5):
            day[i] = data['forecast'][i]
        yesterday = data['yesterday']
        display_weather(day[0], 0)
        print ganmao  # 感冒的几率
        display_yesterday = raw_input('是否显示昨天天气？(y/n)\n')
        if display_yesterday == 'y':
            display_weather(yesterday, -1)
        display_next4 = raw_input('是否显示未来四天天气？(y/n)\n')
        if display_next4 == 'y':
            for i in range(1, 5):
                display_weather(day[i], i)

        print '|--------------------谢谢使用天气查询系统!----------------------|'
    else:
        print '|-------------------- 输入的城市名称有误！----------------------|'


if __name__ == '__main__':
    main()
