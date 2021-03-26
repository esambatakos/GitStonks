import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import datetime

timeStart = datetime.datetime.now()

def googleStrToFloat (googlePriceStr):
    googlePriceFloat = float(googlePriceStr.replace(".","").replace(",","."))
    return googlePriceFloat

def getStockInfoLists(stockSymbol):

    googleSymbClass = 'WuDkNe'
    googlePricID = 'vWLAgc'
    google52WkClass = "iyjjgb"

    URL= 'https://www.google.com/search?q='+stockSymbol+'+stock&oq='+stockSymbol+'+stock&aqs=chrome.0.69i59j35i39j0l4j69i60j69i65.3360j1j7&sourceid=chrome&ie=UTF-8'

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')


#    symb = soup.select("span."+googleSymbClass)
#    if any(symb):
#        stockSymbol = symb[0].text
#        print(stockSymbol)
#    else:
#        stockSymbol = None

    #check if SYmbol tag can be found, if no then return

    pric = soup.find(jsname=googlePricID)
    if pric is None:
        stockPrice = None
        print(type(stockPrice))
    else:
        stockPrice = googleStrToFloat(pric.get_text())


    h52Wk = soup.select("td."+google52WkClass)
    if any(h52Wk):
        if len(h52Wk) < 7:
            high52Wk = None
        else:
            high52Wk = googleStrToFloat(h52Wk[7].text)
    else:
        high52Wk = None


    l52Wk = soup.select("td."+google52WkClass)
    if any(l52Wk):
        if len(l52Wk) < 8:
            low52Wk = None
        else:
            low52Wk = googleStrToFloat(l52Wk[8].text)
    else:
        low52Wk = None

    stockSymbolList.append(stockSymbol)
    stockPriceList.append(stockPrice)
    stockHigh52WkList.append(high52Wk)
    stockLow52WkList.append(low52Wk)

    print(stockSymbol)

def getStockPrice(stockName):

    URL= 'https://www.google.com/search?q='+stockName+'+stock&oq='+stockName+'+stock&aqs=chrome.0.69i59j35i39j0l4j69i60j69i65.3360j1j7&sourceid=chrome&ie=UTF-8'

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    pric = soup.find(jsname="vWLAgc")
    if pric is None:
        stockPrice = None
    else:
        stockPrice = googleStrToFloat(pric.get_text())

    print(stockPrice)


def getStockSymbol(stockName):
    URL= 'https://www.google.com/search?q='+stockName+'+stock&oq='+stockName+'+stock&aqs=chrome.0.69i59j35i39j0l4j69i60j69i65.3360j1j7&sourceid=chrome&ie=UTF-8'

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    symb = soup.select("span."+googleSymbClass)
    if any(symb):
        stockSymbol = symb[0].text
    else:
        stockSymbol = None

    print(stockSymbol)


def getStockHigh52Wk(stockName):
    URL= 'https://www.google.com/search?q='+stockName+'+stock&oq='+stockName+'+stock&aqs=chrome.0.69i59j35i39j0l4j69i60j69i65.3360j1j7&sourceid=chrome&ie=UTF-8'

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    googleHigh52WkClass = "iyjjgb"

    h52Wk = soup.select("td."+googleHigh52WkClass)
    if any(h52Wk):
        try:
            high52Wk = googleStrToFloat(h52Wk[7].text)
        except:
            high52Wk = float(1)
            return high52Wk
    else:
        high52Wk = None



def getStockLow52Wk(stockName):
    URL= 'https://www.google.com/search?q='+stockName+'+stock&oq='+stockName+'+stock&aqs=chrome.0.69i59j35i39j0l4j69i60j69i65.3360j1j7&sourceid=chrome&ie=UTF-8'

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    googleLow52WkClass = "iyjjgb"

    l52Wk = soup.select("td."+googleLow52WkClass)

    if any(l52Wk):
        try:
            low52Wk = googleStrToFloat(l52Wk[7].text)
        except:
            low52Wk = float(1)
            return low52Wk
    else:
        low52Wk = None



def getRevolutStockList():
    URL= 'https://globefunder.com/revolut-stocks-list/#Revolut_list_of_stocks'

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    class1 = 'wp-block-table'

    num = 1

    while True:
        try:
            stockNameRev = soup.select("figure."+class1)[0].select("tbody")[0].select('td')[num].text
            stockSymbol = soup.select("figure."+class1)[0].select("tbody")[0].select('td')[num+1].text
            stockExchange = soup.select("figure."+class1)[0].select("tbody")[0].select('td')[num+5].text
            print(stockNameRev)
            print(stockSymbol)
            print(stockExchange)
            revolutStockList.append(stockNameRev)
            revolutStockSymbolList.append(stockSymbol)
            revolutStockExchangeList.append(stockExchange)
        except:
            break

        num += 7


stockList = ['opk','pltr','txmd']
stockListNew = False
stockSymbolList = []
stockPriceList = []
stockHigh52WkList = []
stockLow52WkList = []

revolutStockList = []
revolutStockSymbolList= []
revolutStockExchangeList= []

#for stock in stockList:
#    getStockInfoLists(stock)


if stockListNew == True:
    print('Please insert stocks individually then press enter. When the list is complete, insert ok')

while stockListNew == True:
    newStock = input()
    if newStock == 'ok':
        break
    else:
        getStockInfoLists(newStock)

getRevolutStockList()
for stock in revolutStockSymbolList:
   getStockInfoLists(stock)


stockFile = open("revolutStockList.txt","a")
for stock in revolutStockSymbolList:
   stockFile.write(stock +"\n")
stockFile.close()

stockH52WkComparisonList=[]
stockL52WkComparisonList=[]

i = 0
while i < len(stockPriceList):
    if stockHigh52WkList[i] != None:
        stockH52WkComparison = (stockPriceList[i] - stockHigh52WkList[i])/stockHigh52WkList[i]*100
        stockL52WkComparison = (stockPriceList[i] - stockLow52WkList[i])/stockLow52WkList[i]*100
    else:
        stockH52WkComparison = None
        stockL52WkComparison = None

    i += 1
    stockL52WkComparisonList.append(stockL52WkComparison)
    stockH52WkComparisonList.append(stockH52WkComparison)



columnsNames = ['Name','Symbol','Price','52Wk High',"52Wk Low","H52WkComparison","L52WkComparison","Stock Exchange"]
df = pd.DataFrame(list(zip(revolutStockList,stockSymbolList,stockPriceList,stockHigh52WkList,stockLow52WkList,stockH52WkComparisonList,stockL52WkComparisonList,revolutStockExchangeList)),columns=columnsNames)
print(df)

df.to_csv('stocksInfoTable.csv', index=False, encoding='utf-8')


timeEnd = datetime.datetime.now()
print(timeStart)
print(timeEnd)

#print(df.loc[df['Name'] == 'TXMD'])
#print(df['Name'][1])

#x = 'Dow'
#print(getStockHigh52Wk(x))
#print(getStockLow52Wk(x))
#print(getStockHigh52Wk('Dow')/2)
