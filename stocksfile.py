import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import datetime

timeStart = datetime.datetime.now()

def googleStrToFloat (googleValueStr):
    if googleValueStr == "-":
        googleValueFloat = None
    else:
        googleValueFloat = float(googleValueStr.replace(".","").replace(",",".").replace("%",""))
    return googleValueFloat


def stockListToStockInfoLists():
    i = 0
    while i < len(revolutStockSymbolList):
        getStockInfoLists(revolutStockSymbolList[i],revolutStockExchangeList[i])
        i += 1


def getStockInfoLists(stockSymbol,stockExchange):

    googleSymbClass = 'WuDkNe'
    googlePricID = 'vWLAgc'
    google52WkClass = "iyjjgb"

    URL= 'https://www.google.com/search?q='+stockSymbol+'+stock+'+stockExchange+'&oq='+stockSymbol+'+stock+'+stockExchange+'&aqs=chrome.1.69i57j0i22i30.7160j1j7&sourceid=chrome&ie=UTF-8'

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


    googleInfo = soup.select("td."+google52WkClass)
    if any(googleInfo):
        if len(googleInfo) < 8:
            high52Wk = None
            low52Wk = None
            peRatio = None
            divYield = None
        else:
            high52Wk = googleStrToFloat(googleInfo[7].text)
            low52Wk = googleStrToFloat(googleInfo[8].text)
            peRatio = googleStrToFloat(googleInfo[4].text)
            divYield = googleStrToFloat(googleInfo[5].text)
    else:
        high52Wk = None
        low52Wk = None
        peRatio = None
        divYield = None

    stockSymbolList.append(stockSymbol)
    stockPriceList.append(stockPrice)
    stockHigh52WkList.append(high52Wk)
    stockLow52WkList.append(low52Wk)
    stockPERatioList.append(peRatio)
    stockDivYieldList.append(divYield)

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
            high52Wk = None
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
            low52Wk = None
            return low52Wk
    else:
        low52Wk = None



def getRevolutStockList():
    URL= 'https://globefunder.com/revolut-stocks-list/#Revolut_list_of_stocks'

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    class1 = 'wp-block-table'

    num = 825*7 + 1

    while True:
        try:
            stockNameRev = soup.select("figure."+class1)[0].select("tbody")[0].select('td')[num].text
            stockSymbol = soup.select("figure."+class1)[0].select("tbody")[0].select('td')[num+1].text
            stockExchange = soup.select("figure."+class1)[0].select("tbody")[0].select('td')[num+5].text
            print(stockNameRev)
            print(stockSymbol)
            print(stockExchange)
            print('')
            revolutStockNameList.append(stockNameRev)
            revolutStockSymbolList.append(stockSymbol)
            revolutStockExchangeList.append(stockExchange)
        except:
            break

        num += 7



def comparison52Wk():
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

stockList = ['opk','pltr','txmd']
stockListNew = False


revolutStockNameList = []
revolutStockSymbolList= []
revolutStockExchangeList= []

stockSymbolList = []
stockPriceList = []
stockHigh52WkList = []
stockLow52WkList = []
stockPERatioList = []
stockDivYieldList = []

stockH52WkComparisonList=[]
stockL52WkComparisonList=[]


#for stock in stockList:
#    getStockInfoLists(stock)


# if stockListNew == True:
#     print('Please insert stocks individually then press enter. When the list is complete, insert ok')
#
# while stockListNew == True:
#     newStock = input()
#     if newStock == 'ok':
#         break
#     else:
#         getStockInfoLists(newStock)


getRevolutStockList()

stockFile = open("revolutStockSymbolList.txt","a")
for stock in revolutStockSymbolList:
   stockFile.write(stock +"\n")
stockFile.close()

stockListToStockInfoLists()

comparison52Wk()

columnsNames = ['Name',"Exchange",'Symbol','Price','52Wk High',"52Wk Low","52Wk High %","52Wk Low %","P/E Ratio","Div Yield"]
df = pd.DataFrame(list(zip(revolutStockNameList,revolutStockExchangeList,stockSymbolList,stockPriceList,stockHigh52WkList,stockLow52WkList,stockH52WkComparisonList,stockL52WkComparisonList,stockPERatioList,stockDivYieldList)),columns=columnsNames)
print(df)

df.to_csv('stocksInfoTable.csv', index=False, encoding='utf-8')


timeEnd = datetime.datetime.now()
duration = timeEnd - timeStart
print(timeStart)
print(timeEnd)
print(duration)

#print(df.loc[df['Name'] == 'TXMD'])
#print(df['Name'][1])
