#-*- coding=utf-8 -*-
from FinalLogger import logger
from Constant import inst_strategy, suffix_list
import urllib.request
import json
import sqlite3

conn = sqlite3.connect('futures.db3', check_same_thread = False)
for i in inst_strategy.keys() :
    daybar_table = i + suffix_list[0]
    cmd = "DROP TABLE IF EXISTS " + daybar_table
    conn.execute(cmd)

    cmd = "CREATE TABLE IF NOT EXISTS " + daybar_table \
          + " (id INTEGER PRIMARY KEY NULL, inst TEXT NULL, open DOUBLE NULL, high DOUBLE NULL, low DOUBLE NULL, close DOUBLE NULL, volume INTEGER NULL, TradingDay TEXT NULL, time TEXT NULL)"
    conn.execute(cmd)

def dealZhengZhou(symbol):
    if symbol[0].isupper():
        inst = symbol.lower()
        # 郑州商品交易所 CZCE TA001 -> ta2001
        inst = inst[:-3]+'2'+inst[-3:]
        return inst
    return symbol

def GetMiddleStr(content,startStr,endStr):
    startIndex = content.index(startStr)
    if startIndex>=0:
        startIndex += len(startStr)
    endIndex = content.index(endStr)
    return content[startIndex:endIndex]

if __name__=="__main__":
    # old 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=M1701'
    # new 'http://stock2.finance.sina.com.cn/futures/api/jsonp.php/myvar=/InnerFuturesNewService.getDailyKLine?symbol=M2101'
    base_url = 'http://stock2.finance.sina.com.cn/futures/api/jsonp.php/myvar=/InnerFuturesNewService.getDailyKLine?symbol='
    for symbol in inst_strategy.keys():
        inst = dealZhengZhou(symbol)
        url = base_url + inst
        print ('url = ' + url)
        trim_json_str = GetMiddleStr(urllib.request.urlopen(url).read().decode('utf-8'),'(',')')
        #print(type(trim_json_str))
        results = json.loads(trim_json_str)

        for r in results:
            # r old-- ["2016-09-05","2896.000","2916.000","2861.000","2870.000","1677366"]  open, high, low, close
            # r new-- {"d":"2020-01-16","o":"2810.000","h":"2825.000","l":"2805.000","c":"2821.000","v":"4472","p":"2768"}
            conn.execute(
                "INSERT INTO %s (inst, open, high, low, close, volume, TradingDay,time) VALUES ('%s', %f, %f, %f, %f, %d, '%s','%s')"
                % (symbol + suffix_list[0], symbol, float(r['o']), float(r['h']), float(r['l']), float(r['c']), int(r['v']), r['d'], '15:00:00'))
            conn.commit()
