import numpy as np
import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import json


def get_stock_symbol(stockName):

    googleSymbClass = 'WuDkNe'

    URL= 'https://www.google.com/search?q='+stockName+'+stock&oq='+stockName+'+stock&aqs=chrome.0.69i59j35i39j0l4j69i60j69i65.3360j1j7&sourceid=chrome&ie=UTF-8'

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    symb = soup.select("span."+googleSymbClass)
    if any(symb):
        stockSymbol = symb[0].text
    else:
        stockSymbol = None

    return stockSymbol

def get_nasdaq_api_date_now():
    dateNow = datetime.datetime.now()
    dayNow = dateNow.strftime("%d")
    monthNow = dateNow.strftime("%m")
    yearNow = dateNow.strftime("%Y")
    dateNowNasdaqApiFormat = yearNow+'-'+monthNow+'-'+dayNow
    return dateNowNasdaqApiFormat

def get_stock_historical_data(stockSymbol):
    URL= 'https://api.nasdaq.com/api/quote/'+stockSymbol+'/historical?assetclass=stocks&fromdate=1900-01-01&limit=9999&todate='+get_nasdaq_api_date_now()

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    abc = json.loads(page.text)
    return abc

def clear_data(dataFrame):
    df = dataFrame[dataFrame['Volume'].astype(str) != 'N/A']
    return df

def column_string_to_float(dataFrame):
    headersList = list(dataFrame)
    del headersList[0]
    for columnName in headersList:
        dataFrame[columnName] = dataFrame[columnName].astype(str)
        dataFrame[columnName] = dataFrame[columnName].str.replace("$","",regex=True)
        dataFrame[columnName] = dataFrame[columnName].str.replace(",","",regex=True)
        dataFrame[columnName] = dataFrame[columnName].astype(float)

def find_iqr(dataFrame,columnName):
    q3, q1 = np.percentile(dataFrame[columnName],[75,25])
    iqr = q3 - q1
    return iqr

def find_nBins(dataFrame,columnName):
    iqr = find_iqr(dataFrame,columnName)
    numberOfObservations = len(dataFrame[columnName])
    binRange = 2 * iqr / (numberOfObservations**(1/3))
    columnRange = dataFrame[columnName].max() - dataFrame[columnName].min()
    nBins = int(np.ceil(columnRange / binRange))
    return(nBins)

def find_nBins_2(dataFrame,columnName):
    columnRange = dataFrame[columnName].max() - dataFrame[columnName].min()
    nBins = int(np.ceil(columnRange) * 10)
    return(nBins)

def get_date(dataFrame):
    format_date(dataFrame)
    get_day_of_week(dataFrame)
    get_day(dataFrame)
    get_month_name(dataFrame)
    get_year(dataFrame)

def format_date(dataFrame):
    dateList = []
    for date in (dataFrame['Date']):
        date = date.split("/")
        year = int(date[2])
        month = int(date[0])
        day = int(date[1])
        finalDate = datetime.datetime(year,month,day)
        dateList.append(finalDate)

    dataFrame['finalDate'] = dateList

def get_day_of_week(dataFrame):
    dayOfWeekList = []
    for finalDate in (dataFrame['finalDate']):
        dayOfWeek = finalDate.strftime("%A")
        dayOfWeekList.append(dayOfWeek)

    dataFrame['DayOfWeek'] = dayOfWeekList

def get_day(dataFrame):
    dayList = []
    for finalDate in (dataFrame['finalDate']):
        day = finalDate.strftime("%d")
        dayList.append(day)

    dataFrame['Day'] = dayList
    dataFrame['Day'] = dataFrame['Day'].astype(int)

def get_month_name(dataFrame):
    monthList = []
    for finalDate in (dataFrame['finalDate']):
        month = finalDate.strftime("%B")
        monthList.append(month)

    dataFrame['Month'] = monthList

def get_year(dataFrame):
    yearList = []
    for finalDate in (dataFrame['finalDate']):
        year = finalDate.strftime("%Y")
        yearList.append(year)

    dataFrame['Year'] = yearList
    dataFrame['Year'] = dataFrame['Year'].astype(int)

def create_chronological_graph(dataframe):
    dfChronological = dataframe.sort_values('finalDate',ascending=True)
    dfChronological = dfChronological.reset_index()
    print(dfChronological)

    fig, ax = plt.subplots()
    ax.plot('finalDate','Close/Last',data=dfChronological)
    ax.set(xlabel='Date', ylabel='Price',title=stockSymbol.upper() + ' Historical Data')
    ax.grid()
    plt.show()

def create_variable_histogram(dataFrame,columnName):
    fig, ax = plt.subplots()
    nBins = find_nBins_2(dataFrame,columnName)
    ax.hist(columnName,bins=nBins,data=dataFrame)
    ax.set(xlabel='Price', ylabel='Frequency',title=stockSymbol.upper() + ' Price Histogram')
    ax.grid()
    plt.show()

print('Please type stock name or symbol:')

stockName = input()
stockSymbol = get_stock_symbol(stockName)
historicalData = get_stock_historical_data(stockSymbol)

historicalDataRows = historicalData['data']['tradesTable']['rows']
columnsNames = historicalData['data']['tradesTable']['headers']

df = pd.DataFrame(data = historicalDataRows, columns=columnsNames)
df.rename(columns = columnsNames, inplace = True)
df = clear_data(df).reset_index()
del df['index']

column_string_to_float(df)
get_date(df)

print(stockSymbol+' historical data')
print(df)

df['High-Low'] = df['High'] - df['Low']
df['Open-Close/Last'] = df['Open'] - df['Close/Last']

print(' \n'+stockSymbol+' historical data \nGrouped by day of the week\n ')
dayOfTheWeekTable = df.groupby(['DayOfWeek']).agg(np.mean)
dayOfTheWeekTable = dayOfTheWeekTable.sort_values('Open-Close/Last',ascending=False)
print(dayOfTheWeekTable)

print(' \n'+stockSymbol+' historical data \nGrouped by month\n ')
monthTable = df.groupby(['Month']).agg(np.mean)
monthTable = monthTable.sort_values('Open-Close/Last',ascending=False)
print(monthTable)

print('What year would you like to start from:')
inputYear = int(input())
dfYear = df[df['Year'] >= inputYear] #astype duplicate
print(dfYear)

create_chronological_graph(dfYear)
create_variable_histogram(dfYear,'Close/Last')

df.info()
print(df.describe())
print(df.corr())
