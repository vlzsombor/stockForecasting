
import azure.functions as func
import logging
import csv
from datetime import datetime
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMA



    # tickerSymbol = 'AAPL'
    # data = yf.Ticker(tickerSymbol)

    # prices = data.history(period="3mo").Close
    # returns = prices.pct_change().dropna()

    # if second_last.action == 'b':
    #     sell_price = prices.values[-1]
    #     ret = (sell_price-second_last.buy_price)/second_last.buy_price
    #     amt = (1+ret) * second_last.total_amount
    #     # Example usage
    #     additional_values = [prices.index[-1], sell_price, amt, ret]  # Values to append to the last line
    #     append_to_last_line(inputblob, additional_values)

    # if type(order) == tuple:
    #     try:
    #         #fit model
    #         a = returns[:second_last.date]
    #         model = ARIMA(a, order=order).fit()
            
    #         #get forecast
    #         pred = model.forecast().values[0]

    #     except Exception as ex:
    #         print(str(ex))
    #         pred = thresh - 1

    # if pred > thresh:
    #     create_a_new_line(inputblob, ('b', prices.values[-1], pred))
    # else:
    #     create_a_new_line(inputblob, ('n', prices.values[-1], pred))

    # outputblob.set("returns")


# Step 2: Define the class with date and action attributes
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
    


def append_to_last_line(fileContent, additional_values):
    # Step 1: Read the entire CSV file
    
    reader = list(csv.reader(fileContent.splitlines()))
    
    # Step 2: Append the additional values to the last line
    if reader:
        reader[-1].extend(additional_values)
    
    # Step 3: Write the modified data back to the CSV file
    writer = csv.writer(fileContent)
    writer.writerows(reader)

def create_a_new_line(fileContent, values):
    # Step 3: Write the modified data back to the CSV file
    writer = csv.writer(fileContent)
    writer.writerow(values)

def read_csv_serialize(textContent):
    second_to_last_line = read_second_to_last_line(textContent)
    # Parse the date

    # Extract the action
    action = second_to_last_line[0]
    buy_price = float(second_to_last_line[1])
    predicted_return = float(second_to_last_line[2])
    date = datetime.strptime(second_to_last_line[3], '%Y-%m-%d %H:%M:%S%z')
    sell_price = float(second_to_last_line[4])
    total_amount = float(second_to_last_line[5])
    total_return = float(second_to_last_line[6])

    # Create a DataRecord instance and append to the list
    return DataRecord(action, buy_price, predicted_return, date, sell_price, total_amount, total_return)

def read_second_to_last_line(textContent):
    reader = list(csv.reader(textContent.splitlines()))
    if len(reader) < 3:
        return None  # If the file has less than 3 lines (including the header), return None
    return reader[-2]  # Second to last line


inputblob = """Action,Buy_Price,Predicted_Return,Date,Sell_Price,Total_Amount,Total_Return
b,100,1,2024-08-07 00:00:00-04:00,1,1,1
b,100,1,2024-08-08 00:00:00-04:00,1,1,1
b,100,1,2024-08-12 00:00:00-04:00,217.52999877929688,2.175299987792969,1.1752999877929688
b,217.52999877929688,-0.0014657435421495712,2024-08-12 00:00:00-04:00,217.52999877929688,4.731930036892091,1.1752999877929688
n,217.52999877929688,0.0030710709193225347
"""


second_last = read_csv_serialize(inputblob)
print(second_last)


tickerSymbol = 'AAPL'
data = yf.Ticker(tickerSymbol)

prices = data.history(period="3mo").Close
returns = prices.pct_change().dropna()

if second_last.action == 'b':
    sell_price = prices.values[-1]
    ret = (sell_price-second_last.buy_price)/second_last.buy_price
    amt = (1+ret) * second_last.total_amount
    # Example usage
    additional_values = [prices.index[-1], sell_price, amt, ret]  # Values to append to the last line
    append_to_last_line(inputblob, additional_values)
else:
    additional_values = [prices.index[-1], -1, second_last.total_amount, second_last.total_return]  # Values to append to the last line
    append_to_last_line(filename, additional_values)
  
if type(order) == tuple:
    try:
        #fit model
        a = returns[:second_last.date]
        model = ARIMA(a, order=order).fit()
        
        #get forecast
        pred = model.forecast().values[0]

    except Exception as ex:
        print(str(ex))
        pred = thresh - 1

if pred > thresh:
    create_a_new_line(inputblob, ('b', prices.values[-1], pred))
else:
    create_a_new_line(inputblob, ('n', prices.values[-1], pred))