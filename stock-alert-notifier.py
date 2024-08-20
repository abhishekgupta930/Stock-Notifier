import smtplib
import json
import plotly.express as px
from email.mime.multipart import MIMEMultipart
from functools import reduce
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pretty_html_table import build_table
import plotly.graph_objects as go
from email.message import EmailMessage
from dateutil.relativedelta import *

import base64

import ssl
import yfinance as yf
#import plotly.offline as pyo
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr


def cal_all_stocks_5yr(df):
    stock = {}
    curr_date = df.tail(1).index.item()
    past_date = curr_date - relativedelta(years=5)+relativedelta(days=3)
    curr_date = curr_date.strftime('%Y-%m-%d')
    past_date = past_date.strftime('%Y-%m-%d')

    for col in df.columns:
        val = (df.loc[curr_date][col].round(2)-df.loc[past_date][col].round(2))*100/df.loc[past_date][col].round(2)
        stock[col] = val.round(2)
        five_yr_df = pd.DataFrame(stock.items(), columns=['Company', '5 Yr Percentage']).dropna()

    return five_yr_df

def cal_all_stocks_3yr(df):
    stock = {}
    curr_date = df.tail(1).index.item()
    past_date = curr_date - relativedelta(years=3)+relativedelta(days=3)
    curr_date = curr_date.strftime('%Y-%m-%d')
    past_date = past_date.strftime('%Y-%m-%d')
   
    for col in df.columns:
        val = (df.loc[curr_date][col].round(2)-df.loc[past_date][col].round(2))*100/df.loc[past_date][col].round(2)
        stock[col] = val.round(2)
        three_yr_df = pd.DataFrame(stock.items(), columns=['Company', '3 Yr Percentage']).dropna()
        #three_yr_df = three_yr_df.sort_values('3 Yr Percentage', ascending=False)

    return three_yr_df

def cal_all_stocks_1yr(df):
    stock = {}
    curr_date = df.tail(1).index.item()
    past_date = curr_date - relativedelta(years=1)

    curr_date = curr_date.strftime('%Y-%m-%d')
    past_date = past_date.strftime('%Y-%m-%d')
   
    for col in df.columns:
        val = (df.loc[curr_date][col].round(2)-df.loc[past_date][col].round(2))*100/df.loc[past_date][col].round(2)
        stock[col] = val.round(2)
        one_yr_df = pd.DataFrame(stock.items(), columns=['Company', '1 Yr Percentage']).dropna()
        #three_yr_df = three_yr_df.sort_values('1 Yr Percentage', ascending=False)

    return one_yr_df

def cal_all_stocks_1mon(df):
    stock = {}
    curr_date = df.tail(1).index.item()
    past_date = curr_date - relativedelta(months=1)+relativedelta(days=3)

    curr_date = curr_date.strftime('%Y-%m-%d')
    past_date = past_date.strftime('%Y-%m-%d')
   
    for col in df.columns:
        val = (df.loc[curr_date][col].round(2)-df.loc[past_date][col].round(2))*100/df.loc[past_date][col].round(2)
        stock[col] = val.round(2)
        one_month_df = pd.DataFrame(stock.items(), columns=['Company', '1 month Percentage Change']).dropna()
        #three_yr_df = three_yr_df.sort_values('1 Yr Percentage', ascending=False)

    return one_month_df

def cal_all_stocks_6mon(df):
    stock = {}
    curr_date = df.tail(1).index.item()
    past_date = curr_date - relativedelta(months=6)+relativedelta(days=3)

    curr_date = curr_date.strftime('%Y-%m-%d')
    past_date = past_date.strftime('%Y-%m-%d')
   
    for col in df.columns:
        val = (df.loc[curr_date][col].round(2)-df.loc[past_date][col].round(2))*100/df.loc[past_date][col].round(2)
        stock[col] = val.round(2)
        three_month_df = pd.DataFrame(stock.items(), columns=['Company', '6 month Percentage Change']).dropna()
        #three_yr_df = three_yr_df.sort_values('1 Yr Percentage', ascending=False)

    return three_month_df

def cal_weekly_price(df):

    stock = {}
    df = df.asfreq('D', method = 'pad')

    #today's price
    print(df.tail)
    curr_date = df.tail(1).index.item()
    curr_date = curr_date.strftime('%Y-%m-%d')
    print(f"Current date {curr_date}")

    for col in df.columns:
        val = (df.loc[curr_date][col].round(2))
        stock[col] = val
        today_df = pd.DataFrame(stock.items(), columns=['Company', 'Today']).dropna()

    
    
    #1 week ago
    curr_date = curr_date = df.tail(1).index.item()- relativedelta(weeks=1)
    curr_date = curr_date.strftime('%Y-%m-%d')

    for col in df.columns:
        val = (df.loc[curr_date][col].round(2))
        stock[col] = val
        one_week_df = pd.DataFrame(stock.items(), columns=['Company', 'Last Week']).dropna()

    #2 week ago
    curr_date =  curr_date = df.tail(1).index.item() - relativedelta(weeks=2)
    curr_date = curr_date.strftime('%Y-%m-%d')

    for col in df.columns:
        val = (df.loc[curr_date][col].round(2))
        stock[col] = val
        two_week_df = pd.DataFrame(stock.items(), columns=['Company', 'Two Week']).dropna()

    # 3 week ago
    curr_date = curr_date = df.tail(1).index.item()- relativedelta(weeks=3)
    curr_date = curr_date.strftime('%Y-%m-%d')


    for col in df.columns:
        val = (df.loc[curr_date][col].round(2))
        stock[col] = val
        three_week_df = pd.DataFrame(stock.items(), columns=['Company', 'Three Week']).dropna()


    # Merge weekly data
    data_frames = [today_df, one_week_df, two_week_df, three_week_df]

    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Company'],
                                            how='outer'), data_frames)

    return df_merged
    

def getWeeklyprice():
    df_close = getCLoseDataframe()
    df = cal_weekly_price(df_close)
    return df

def allStock(df):

    return cal_all_stocks_3yr(df)

def getCLoseDataframe():

    #stockList = tickers.Symbol.to_list()
    #stockList = ["AAPL", "NVDA", "QCOM" ,"MSFT", "ANET", "AMD"]
    stockList = ["AAPL", "NVDA", "QCOM" ,"MSFT", "AVGO", "AMD", "META", "GOOG", "VOO", "QQQ"]

    df = yf.download(stockList,start ="2018-05-11",end = pd.to_datetime('today').date()+relativedelta(days=1)) 
    df = df.asfreq('D', method = 'pad')

    df_close= df['Close']
    return df_close

def calculate():
    tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    #stockList = tickers.Symbol.to_list()
    stockList = ["AAPL", "NVDA", "QCOM" ,"MSFT", "ANET", "AMD"]
    df = yf.download(stockList,start ="2018-05-11",end = pd.to_datetime('today').date()) 
 

def getlongTermDetails():
    df_close = getCLoseDataframe()
    df_1yr = cal_all_stocks_1yr(df_close)
    df_3yr = cal_all_stocks_3yr(df_close)
    df_5yr = cal_all_stocks_5yr(df_close)
    markersize = df_1yr["1 Yr Percentage"].abs().round()

    data_frames = [df_1yr,df_3yr, df_5yr]

    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Company'],
                                            how='outer'), data_frames)
    fig = go.Figure()
    #fig.add_trace(go.scatter(x=[1,2,3], y=[100,200,300]))
    fig.add_trace(go.Scatter(x=df_merged["Company"], y=df_merged["1 Yr Percentage"], name= '1 Yr Percentage change', mode='markers',  marker=dict(
        size=markersize,
        sizemode='area',
        sizeref=2.*max(markersize)/(40.**2),
        sizemin=4)))
    fig.add_trace(go.Scatter(x=df_merged["Company"], y=df_merged["3 Yr Percentage"], name= '3 Yr Percentage change', mode='markers',  marker=dict(
        size=markersize,
        sizemode='area',
        sizeref=2.*max(markersize)/(40.**2),
        sizemin=1)))

    fig.update_layout(
    title='Long Term Percentage Change in Stock Value',
    xaxis=dict(
        title='Company Name',
        gridcolor='white',
        gridwidth=2,
    ),
    yaxis=dict(
        title='% change in stock value',
        gridcolor='white',
        gridwidth=2,
    ),
    )
    #fig = px.scatter(df_merged, x="Company", y="1 month Percentage Change", size = marker_size, facet_col="")
    fig.write_image("long-term.png")
    return df_merged



def getshortTermDetails():
    #get the opening closing data frame
    df_close = getCLoseDataframe()
    df_1mon = cal_all_stocks_1mon(df_close)
    markersize = df_1mon["1 month Percentage Change"].abs().round()

    df_3mon = cal_all_stocks_6mon(df_close)
    data_frames = [df_1mon,df_3mon]

    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Company'],
                                            how='outer'), data_frames)
    fig = go.Figure()
    #fig.add_trace(go.scatter(x=[1,2,3], y=[100,200,300]))
    fig.add_trace(go.Scatter(x=df_merged["Company"], y=df_merged["1 month Percentage Change"], name= '1 month Percentage change', mode='markers',  marker=dict(
        size=markersize,
        sizemode='area',
        sizeref=2.*max(markersize)/(40.**2),
        sizemin=4)))
    fig.add_trace(go.Scatter(x=df_merged["Company"], y=df_merged["6 month Percentage Change"], name= '6 month Percentage change',  mode='markers',  marker=dict(
        size=markersize,
        sizemode='area',
        sizeref=2.*max(markersize)/(40.**2),
        sizemin=1)))

    fig.update_layout(
    title='Short Term Percentage Change in Stock Value',
    xaxis=dict(
        title='Company Name',
        gridcolor='white',
        gridwidth=2,
    ),
    yaxis=dict(
        title='% change in stock value',
        gridcolor='white',
        gridwidth=2,
    ),
    )
    #fig = px.scatter(df_merged, x="Company", y="1 month Percentage Change", size = marker_size, facet_col="")
    fig.write_image("short-term.png")
    return df_merged


def sendMail(update):
    sender_email = 'abhgqualcomm@gmail.com'
    email_password = 'uqyg qgzy rfmg gxrh'
    receiver_email = ['rahulsoni005@gmail.com', 'sonu.mnnit@gmail.com']
    email_server_host = 'smtp.gmail.com'
    subject = 'Rahul Stock alerts'
    
    #Weekly Price
    df_weekly = getWeeklyprice()
    table3 = build_table(df_weekly,"blue_light")

    html = """\
    <html>
        <body>
            <h1>Weekly Price in US dollars of Selected Stocks</h1>
        </body>
    </html>
    """
    html += table3

    df_longTerm = getlongTermDetails()
    table = build_table(df_longTerm,"blue_light")
    # We assume that the image file is in the same directory that you run your Python script from
    fp = open('long-term.png', 'rb')
    image1 = MIMEImage(fp.read())
    fp.close()

    # Specify the  ID according to the img src in the HTML part
    image1.add_header('Content-ID', '<long-term>')
    html += """\
    <html>
        <body>
            <h1>Long Term Percentage Change in Companies added in List</h1>
            <img src="cid:long-term">
        </body>
    </html>
    """
    html += table
    # To accomodate short term changes
    df_shortTerm = getshortTermDetails()
    table2 = build_table(df_shortTerm,"blue_light")
    fp = open('short-term.png', 'rb')
    image2 = MIMEImage(fp.read())
    fp.close()
    image2.add_header('Content-ID', '<short-term>')

    html += """\
    <html>
        <body>
            <h1>Short Term Percentage Change in Companies added in List</h1>
            <img src="cid:short-term">
        </body>
    </html>
    """
    html += table2

    

# Specify the  ID according to the img src in the HTML part
    em = MIMEMultipart('alternative')

    em['From'] = sender_email
    em['To'] = ", ".join(receiver_email)
    em['Subject'] = subject


    part1 = MIMEText(html, "html")
    part2 = MIMEText(table, "html")

    em.attach(part1)
    em.attach(image1)
    em.attach(image2)


# Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, email_password)
        server.sendmail(
        sender_email, receiver_email, em.as_string()
    )

def main():

    update = calculate()
    sendMail(update)
main()