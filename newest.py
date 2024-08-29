
import azure.functions as func
import logging
import csv
from datetime import datetime
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMA
import os

def csv_serialize_predict(textContent, line_index):
    # Parse the date
    last_line = read_line(textContent, line_index)
    # Extract the action
    action = last_line[0]
    buy_price = float(last_line[1])
    predicted_return = float(last_line[2])
    
    # dd/mm/YY H:M:S
    # Create a DataRecord instance and append to the list
    return DataRecord(action, buy_price, predicted_return, datetime.now(), None, None, None)

def csv_serialize_full(textContent, line_index):
    # Parse the date
    last_line = read_line(textContent, line_index)
    # Extract the action
    action = last_line[0]
    buy_price = float(last_line[1])
    predicted_return = float(last_line[2])
    date = datetime.strptime(last_line[3], '%Y-%m-%d %H:%M:%S%z')
    sell_price = float(last_line[4])
    total_amount = float(last_line[5])
    total_return = float(last_line[6])
    return DataRecord(action, buy_price, predicted_return, date, sell_price, total_amount, total_return)

def read_line(textContent, n):
    reader = list(csv.reader(textContent.splitlines()))
    return reader[n]  # Second to last line


class DataRecord:
    def __init__(self,action, buy_price, predicted_return, date, sell_price, total_amount: int, total_return: int):
        self.date = date
        self.total_amount = total_amount
        self.sell_price = sell_price
        self.total_return = total_return
        self.action = action
        self.buy_price = buy_price
        self.predicted_value = predicted_return
    def __repr__(self):
        return f"DataRecord(date={self.date}, action='{self.action}, buy_price='{self.buy_price}')"
    


inputblob = """Action,Buy_Price,Predicted_Return,Date,Sell_Price,Total_Amount,Total_Return
b,100,1,2024-08-07 00:00:00-04:00,1,1,1
b,100,1,2024-08-08 00:00:00-04:00,1,1,1
b,100,1,2024-08-12 00:00:00-04:00,217.52999877929688,2.175299987792969,1.1752999877929688
b,217.52999877929688,-0.0014657435421495712,2024-08-12 00:00:00-04:00,217.52999877929688,4.731930036892091,1.1752999877929688
b,217.52999877929688,0.0030710709193225347"""

tickerSymbol = 'AAPL'
data = yf.Ticker(tickerSymbol)
prices = data.history(period="3mo").Close
returns = prices.pct_change().dropna()


order = (5,0,0)  
thresh = 0.005
last_line = csv_serialize_predict(inputblob, -1)
second_last_line = csv_serialize_full(inputblob, -2)

if last_line.action == 'b':
    sell_price = prices.values[-1]
    ret = (sell_price-last_line.buy_price)/last_line.buy_price
    amt = (1+ret) * second_last_line.total_amount
    # Example usage
    additional_values = []  # Values to append to the last line
    inputblob = inputblob + "," + str(prices.index[-1]) + "," + str(sell_price) + "," + str(amt) + "," + str(ret)
else:
    sell_price = prices.values[-1]
    ret = (sell_price-last_line.buy_price)/last_line.buy_price
    amt = (1+ret) * second_last_line.total_amount
    # Example usage
    additional_values = []  # Values to append to the last line
    inputblob = inputblob + "," + str(prices.index[-1]) + "," + str(sell_price) + "," + str(second_last_line.total_amount) + "," + str(second_last_line.total_return)

print(inputblob)

if type(order) == tuple:
    try:
        #fit model
        a = returns[:second_last_line.date]
        model = ARIMA(a, order=order).fit()
        
        #get forecast
        pred = model.forecast().values[0]

    except Exception as ex:
        print(str(ex))
        pred = thresh - 1

if pred > thresh:
    inputblob = inputblob + os.linesep + 'b' + "," + str(prices.values[-1]) + "," + str(pred)
else:
    inputblob = inputblob + os.linesep + 'n' + "," + str(prices.values[-1]) + "," + str(pred)



print(inputblob)