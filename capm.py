#importing libraries

import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import pandas_datareader.data as web
import capm_functions
import list_of_sp
from PIL import Image

img = Image.open('LOGO.png')
st.set_page_config(page_title="CAPM", layout='wide', page_icon=img)

st.title("Capital Asset Pricing Model")

#getting input from user

col1, col2 = st.columns([1, 1])
list1 = list_of_sp.sp_lst
with col1:
    stocks_list = st.multiselect('Choose 4 stocks', list1, ['TSLA', 'AAPL', 'MSFT', 'AMZN'])

with col2:
    year = st.number_input('Number of year', 1, 10)
    
#downloading data from SP500
try:
    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year - year, datetime.date.today().month, datetime.date.today().day)
                            #  2023   -    2   =    2021

    SP500 = web.DataReader(['sp500'], 'fred', start, end)
    #print(SP500.tail())


    stocks_df = pd.DataFrame()

    for stock in stocks_list:
        data = yf.download(stock, period=f'{year}y')
        #print(data.head())
        stocks_df[f'{stock}'] = data['Close']

    #print(stocks_df.head())

    stocks_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)

    SP500.columns = ['Date', 'sp500']
    stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
    stocks_df['Date'] = stocks_df['Date'].apply(lambda x: str(x)[:10])
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner') 

    #print(stocks_df)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Dataframe Head")
        st.dataframe(stocks_df.head(), use_container_width=True)

    with col2:
        st.markdown('### Dataframe Tail')
        st.dataframe(stocks_df.tail(), use_container_width=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Price of all the Stocks")
        st.plotly_chart(capm_functions.interactive_plot(stocks_df))

    with col2:
        st.markdown('### Price of all the Stocks(After Normatization)')
        st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalization(stocks_df)))
        
    stocks_daily_return = capm_functions.daily_return(stocks_df)
    #print(stocks_daily_return)

    beta = {}
    alpha = {}

    for i in stocks_daily_return.columns:
        if i != 'Date' and i != 'sp500':
            b, a = capm_functions.calculate_beta(stocks_daily_return, i)
            
            beta[i] = b
            alpha[i] = a

    #print(beta, alpha)

    beta_df = pd.DataFrame(columns = ['Stock', 'Beta Value'])
    beta_df['Stock'] = beta.keys()
    beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]

    with col1:
        st.markdown("### Calculated Beta Value")
        st.dataframe(beta_df, use_container_width=True)
        
    rf = 0  # risk free
    rm = stocks_daily_return['sp500'].mean()*252  # market portfolio return 

    return_df = pd.DataFrame()
    return_value = []
    for stock, value in beta.items():
        return_value.append(str(round(rf + (value*(rm - rf)), 2)))
    return_df['Stock'] = stocks_list

    return_df['Return Value'] = return_value

    with col2:
        st.markdown('### Calculated Return Using CAPM')
        st.dataframe(return_df, use_container_width=True)
    
except:
    st.write('Please select valid input')