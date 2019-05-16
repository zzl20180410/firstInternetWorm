# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import datetime
import time
import string
import pymysql

'''
拿到每期的url
'''
def getIssueNumberAllUrl(url):
     req = requests.get(url = url)
     req.encoding = 'GBK'  # 需要添加这一行，告知html文件解码方式
     html = req.text
     bf = BeautifulSoup(html)

     selectList = bf.find('div',class_="iSelectList")
     aList = selectList.find_all('a')
     hrefList = []
     for href in aList:
          hrefList.append(href['href'])
     return hrefList

'''
获取每页期号
'''
def getIssueNumber(table):
     trList = table.find_all('tr')

     spanList = trList[0].find_all('span')
     issueNumberArr = spanList[0].get_text().replace(' ', '').split()
     issueNumber = ''
     for item in issueNumberArr:
          issueNumber = issueNumber + item
     return int(issueNumber[4:9])

'''
获取每页的数据
'''
def getIssueNumberTable(url):
     req = requests.get(url = url)
     req.encoding = 'GBK'  # 需要添加这一行，告知html文件解码方式
     html = req.text
     bf = BeautifulSoup(html)

     return bf.find_all('table',class_='kj_tablelist02')

'''
获取每页的数据
'''
def getIssueNumberData(tableList):
     # doubleChromosphere = DoubleChromosphere()
     doubleChromosphere = {}
     chromosphere = {}
     # 获取期号
     issueNumber = getIssueNumber(tableList[0])
     chromosphere['issue_number'] = issueNumber
     doubleChromosphere['chromosphere'] = chromosphere
     # print(issueNumber)
     # 解析第一个table
     analysisFirstTable(tableList[0],doubleChromosphere)
     # 解析第二个table
     analysisSecondTable(tableList[1],issueNumber,doubleChromosphere)

     return doubleChromosphere

def analysisFirstTable(table,doubleChromosphere):
     chromosphere = doubleChromosphere['chromosphere']
     trList = table.find_all('tr')

     # 获取开奖日期
     lotteryDateList = trList[0].find_all('span')
     lotteryDate = lotteryDateList[1].get_text()
     lotteryDate = lotteryDate.lstrip()
     lotteryDate = lotteryDate[5:15]
     chromosphere['lottery_date'] = lotteryDate
     # getLotteryDate(lotteryDate)

     # 获取开奖号码
     liList = trList[1].find_all('li')
     liArr = ['first','second','third','fourth','fifth','sixth','seventh']
     i = 0
     for li in liList:
          chromosphere[liArr[i]] = int(li.get_text())
          i = i + 1
     # print(liArr)

     # 获取出球顺序
     seconTrList = trList[1].find_all('tr')
     seconTdList = seconTrList[1].find_all('td')
     outOrder = seconTdList[1].get_text().strip()
     outOrder = outOrder.replace(' ','-')
     chromosphere['out_order'] = outOrder

     # 获取奖金池
     spanList = trList[4].find_all('span')
     currentSalesVolume = spanList[0].get_text()
     poolRolling = spanList[1].get_text()
     chromosphere['current_sales_volume'] = currentSalesVolume
     chromosphere['pool_rolling'] = poolRolling
     chromosphere['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
     # print(currentSalesVolume)
     # print(poolRolling)

def getLotteryDate(lotteryDate):
     lotteryDate = lotteryDate.replace('年', '-')
     lotteryDate = lotteryDate.replace('月', '-')
     lotteryDate = lotteryDate.replace('日', '')
     dataArr = lotteryDate.split('-')
     year = dataArr[0].strip()
     month = dataArr[1].strip()
     date = dataArr[2].strip()

     if (len(month) == 1):
          month = '0' + month
     if (len(date) == 1):
          date = '0' + date

     lotteryDate = year + '-' + month + '-' + date
     return time.strptime(lotteryDate, "%Y-%m-%d")


def analysisSecondTable(table,issueNumber,doubleChromosphere):
     chromospherePrizes = []
     doubleChromosphere['chromospherePrizes'] = chromospherePrizes
     trList = table.find_all('tr')

     for index in range(2,len(trList)-1):
          tdList = trList[index].find_all('td')
          prize = tdList[0].get_text().strip()
          winningTimes = int(tdList[1].get_text().strip().replace('元','').replace(',',''))
          bonus = int(tdList[2].get_text().strip().replace('元','').replace(',',''))

          chromospherePrize = {}
          chromospherePrize['issue_number'] = issueNumber
          chromospherePrize['prize'] = prize
          chromospherePrize['winningTimes'] = winningTimes
          chromospherePrize['bonus'] = bonus
          chromospherePrize['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

          chromospherePrizes.append(chromospherePrize)

          # print(chromospherePrize)

'''
导入数据
'''
def importChromosphereData(T):
     # 打开数据库连接
     db = pymysql.connect(host='localhost', port=3306,
                          user='root', passwd='root', db='chromosphere', charset='utf8')

     # 使用cursor()方法获取操作游标
     cursor = db.cursor()

     # SQL 插入语句
     sql = "INSERT INTO zzl_double_chromosphere(issue_number,lottery_date,first,second,third,fourth,fifth,sixth,seventh,out_order,current_sales_volume,pool_rolling,create_time) " \
           "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
     try:
          # 执行sql语句
          cursor.executemany(sql, T)
          # 提交到数据库执行
          db.commit()
     except Exception as e:
          print("importChromosphereData: " + repr(e))
          # 如果发生错误则回滚
          db.rollback()
     # 关闭游标
     cursor.close()
     # 关闭数据库连接
     db.close()


'''
导入数据
'''
def importChromospherePrizeData(T):
     # 打开数据库连接
     db = pymysql.connect(host='localhost', port=3306,
                          user='root', passwd='root', db='chromosphere', charset='utf8')

     # 使用cursor()方法获取操作游标
     cursor = db.cursor()

     # SQL 插入语句
     sql = "INSERT INTO zzl_double_chromosphere_prize(issue_number,prize,winning_times,bonus,create_time) VALUES (%s,%s,%s,%s,%s)"

     try:
          # 执行sql语句
          cursor.executemany(sql, T)
          # 提交到数据库执行
          db.commit()
     except Exception as e:
          print("importChromospherePrizeData: " + repr(e))
          # 如果发生错误则回滚
          db.rollback()
     # 关闭游标
     cursor.close()
     # 关闭数据库连接
     db.close()

'''
导入错误日志
'''
def importErrorData(T):
     # 打开数据库连接
     db = pymysql.connect(host='localhost', port=3306,
                          user='root', passwd='root', db='chromosphere', charset='utf8')

     # 使用cursor()方法获取操作游标
     cursor = db.cursor()

     # SQL 插入语句
     sql = "INSERT INTO zzl_double_chromosphere_error(issue_number, error_message, handle,create_time) VALUES (%s,%s,%s,%s)"
     # 一个tuple或者list
     # T = (('一期', '错误',1,now_time),)

     try:
          # 执行sql语句
          cursor.executemany(sql, T)
          # 提交到数据库执行
          db.commit()
     except Exception as e:
          print('importErrorData: ' + repr(e))
          # 如果发生错误则回滚
          db.rollback()
     # 关闭游标
     cursor.close()
     # 关闭数据库连接
     db.close()

'''
查询数据
'''
def findChromosphereData():
     # 打开数据库连接
     db = pymysql.connect(host='localhost', port=3306,
                          user='root', passwd='root', db='chromosphere', charset='utf8')
     # 使用 cursor() 方法创建一个游标对象 cursor
     cursor = db.cursor()
     # 使用 execute()  方法执行 SQL 查询
     cursor.execute("SELECT * FROM zzl_double_chromosphere")
     # 使用 fetchone() 方法获取单条数据.
     data = cursor.fetchall()
     print("Database version : %s " % str(data))

     cursor.close()
     # 关闭数据库连接
     db.close()
     return data


if __name__ == "__main__":

     target = 'http://kaijiang.500.com/shtml/ssq/19051.shtml?0_ala_baidu'
     allUrl = getIssueNumberAllUrl(target)
     print("所有的url长度: " + str(len(allUrl)))
     doubleChromosphereList = []
     for index in range(0,len(allUrl)):
          issueNumber = 0
          try:
               tableList = getIssueNumberTable(allUrl[index])
               issueNumber = getIssueNumber(tableList[0])
               doubleChromosphere = getIssueNumberData(tableList)
               doubleChromosphereList.append(doubleChromosphere)
          except Exception as e:
               print('错误期号: ' + str(issueNumber))
               print(repr(e))
               if( issueNumber > 0):
                    dataList = []
                    data = [issueNumber,repr(e),1,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))]
                    dataList.append(data)
                    importErrorData(dataList)

     # print(doubleChromosphereList)
     # 批量导入数据(一千为一批)
     i = 1
     j = 1
     chromosphereList = []
     chromospherePrizeList = []
     for item in doubleChromosphereList:
          chromosphere = item['chromosphere']

          chromosphereList.append(list(chromosphere.values()))
          if((i % 1000) == 0):
               importChromosphereData(chromosphereList)
               chromosphereList = []
          i = i + 1

          chromospherePrizes = item['chromospherePrizes']
          for pitem in chromospherePrizes:
               chromospherePrizeList.append(list(pitem.values()))
               if ((j % 1000) == 0):
                    importChromospherePrizeData(chromospherePrizeList)
                    chromospherePrizeList = []
               j = j + 1

     if(len(chromosphereList) > 0):
          importChromosphereData(chromosphereList)
     if(len(chromospherePrizeList) > 0):
          importChromospherePrizeData(chromospherePrizeList)

     # print(chromosphereList)
     # print(chromospherePrizeList)


