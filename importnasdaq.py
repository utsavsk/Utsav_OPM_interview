import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from tqdm import tqdm
from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.holiday import USFederalHolidayCalendar
from datetime import datetime


#------------------------------------------------------------
#  Import data from all the txt files in 'NASDAQData' folder
#------------------------------------------------------------

## All the data are saved in NASDAQData folder
folder_path = './NASDAQData'
names_nasdaq_df = pd.read_csv('NASDAQData/CompanyNames/NamesNasdaq.txt', delimiter='\t')

## An empty DataFrame that will store all data from txt files
all_data_df = pd.DataFrame(columns=['<ticker>', '<date>', '<close>', '<vol>'])

## Iterating through all files
for filename in os.listdir(folder_path):
    if filename.startswith('NASDAQ_') and filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)       
        data = pd.read_csv(file_path, keep_default_na=False)    

        ### Merging ticker data with company name
        data = pd.merge(data, names_nasdaq_df, left_on= '<ticker>', right_on='Symbol', how='inner')
        data.drop(columns=['Symbol'], inplace=True)
        data.rename(columns={'Description': 'Company_Name'}, inplace=True)

        data['<date>'] = pd.to_datetime(data['<date>'], format='%Y%m%d')
        all_data_df = pd.concat([all_data_df, data[['<ticker>', 'Company_Name', '<date>', '<close>', '<vol>']]], ignore_index=True)

all_data_df = all_data_df.sort_values(by=['<ticker>', '<date>'], ascending=[True, True])

# ## Debug
# print(all_data_df.dtypes)
# print(all_data_df)
# all_data_df = all_data_df[all_data_df['<ticker>'] == 'AAPL']
# print(all_data_df[all_data_df['<ticker>'] == 'AAPL'])


#------------------------------------------------------------
#  Import data from all the txt files in 'NASDAQData' folder
#------------------------------------------------------------

## unique tickers
unique_tickers = all_data_df['<ticker>'].unique()

## Getting days when market's not closed
us_business_day = CustomBusinessDay(calendar=USFederalHolidayCalendar())

## An empty DataFrame that will store the results
results_df = pd.DataFrame(columns=['Ticker', 'Company_Name', 'Close_date', 
                                   'Predicted_date', 'MaxHigh_30', 'MinHigh_30', 
                                   'MaxHigh_90', 'MinHigh_90',
                                   'Close','Predicted_price', 'average_volume'])

## Iterate through each unique ticker
for ticker in tqdm(unique_tickers, desc="Running regressions:", unit="ticker", ncols=80):
    ticker_data = all_data_df[all_data_df['<ticker>'] == ticker][['<date>', '<close>', '<vol>', 'Company_Name']]
    ticker_data = ticker_data.sort_values('<date>', ascending=True)


    company_Name = ticker_data['Company_Name'].iloc[0]
   
   ## Maximum and minimum closing prices at 30 and 90 data points
    avg_vol_30 = int(sum(ticker_data['<vol>'][-30:])/len(ticker_data['<vol>'][-30:]))
    fmt_avg_vol_30 = "{:,}".format(avg_vol_30)

    max_high_30 = ticker_data['<close>'][-30:].max() 
    min_high_30 = ticker_data['<close>'][-30:].min() 
    max_high_90 = ticker_data['<close>'][-90:].max() 
    min_high_90 = ticker_data['<close>'][-90:].min() 
   

    ## Note: this is not a typical time series analysis
    ## Linear regression of the last 7 data points
    if len(ticker_data) >= 7:
        day1 = ticker_data['<close>'].iloc[-7]
        day2 = ticker_data['<close>'].iloc[-6]
        day3 = ticker_data['<close>'].iloc[-5]
        day4 = ticker_data['<close>'].iloc[-4]
        day5 = ticker_data['<close>'].iloc[-3]
        day6 = ticker_data['<close>'].iloc[-2]
        day7 = ticker_data['<close>'].iloc[-1]

        date1 = ticker_data['<date>'].iloc[-7]
        date2 = ticker_data['<date>'].iloc[-6]
        date3 = ticker_data['<date>'].iloc[-5]
        date4 = ticker_data['<date>'].iloc[-4]
        date5 = ticker_data['<date>'].iloc[-3]
        date6 = ticker_data['<date>'].iloc[-2]
        date7 = ticker_data['<date>'].iloc[-1]

        fixed_X = np.array([1, 2, 3, 4, 5, 6, 7])
        X = fixed_X.reshape(-1, 1)

        y_high = ticker_data['<close>'].tail(7)

        model_high = LinearRegression().fit(X, y_high)
        
        ## predict 1 additional data point
        next_date = ticker_data['<date>'].iloc[-1] + us_business_day
        predicted_close = model_high.predict([[8]])[0]
        Predicted_price = "${:.2f}".format(predicted_close)
      
        ## Saving results
        for i in range(7):
            close_value = globals()["day{}".format(i + 1) ]
            close_date = globals()["date{}".format(i + 1) ]

            results_df = pd.concat([results_df, pd.DataFrame({
                'Ticker': [ticker],
                'Company_Name': [company_Name],
                'Predicted_date': [next_date],
                'MaxHigh_30': [max_high_30],
                'MinHigh_30': [min_high_30],
                'MaxHigh_90': [max_high_90],
                'MinHigh_90': [min_high_90],
                'Close': [close_value],
                'Close_date': [close_date],
                'Predicted_price': [Predicted_price],
                'average_volume': [fmt_avg_vol_30]
            })], ignore_index=True)


## Sample result
print(results_df[results_df['Ticker'] == 'AAPL'])

## Saving the final df as csv file
results_df.to_csv('Predict_NASDAQ.csv', index=False)     
today_date = datetime.today().strftime('%Y-%m-%d')
csv_filename = f'Predict_all_{today_date}.csv'
results_df.to_csv(csv_filename, index=False)

