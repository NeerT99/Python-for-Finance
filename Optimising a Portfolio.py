# This Project is a program that will allow you to add tickers in order to
# generate a portfolio which will then be optimised using the Efficient Frontier
# The programme outputs the correlations between the stocks, the sharpe ratio
# and the weightings that constitute the optimal portfoliio

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web
from datetime import date

# Step 1. Using User Inputs to Create Portfolio
df = pd.DataFrame()
start = input('Please Input Start Date in the form "YYYY-MM-DD"')
end = input('Please Input End Date in the form of "YYYY-MM-DD"')
ticker1 = input('Add Ticker 1')
ticker2 = input('Add Ticker 2')
df[ticker1] = pd.DataFrame(web.DataReader(ticker1, data_source='yahoo', start=start, end=end)['Adj Close'])
df[ticker2] = pd.DataFrame(web.DataReader(ticker2, data_source='yahoo', start=start, end=end)['Adj Close'])


def add_more_tickers():
    choose_ticker = input('Please Choose another Ticker to add...')
    try:
        df[choose_ticker] = pd.DataFrame(web.DataReader(choose_ticker, data_source='yahoo', start=start, end=end)['Adj Close'])
        print('ticker has been added!')
        restart()
    except:
        print('Error, Ticker Incorrect, Please Try Again')
        add_more_tickers()

def restart():
    restart = input('Would you like to select another Ticker? - State Y or N')
    if restart == 'Y':
        add_more_tickers()
    elif restart == 'N':
        print('The Chosen Tickers are:')
        for t in df.columns:
            print(t)

restart()

# Step 2. Obtaining the Correlation Matrix
log_returns = np.log(df/df.shift())
correlation = log_returns.corr()
print('Here is the Correlation Matrix for the Portfolio', '\n', correlation)

# Step 3. Running a Monte Carlo Simulation to get the Optimal Portfolio
n = 10000
get_no_of_tickers = len(df.columns)
weights = np.zeros((n, get_no_of_tickers))
exp_rtns = np.zeros(n)
exp_vols = np.zeros(n)
sharpe_ratios = np.zeros(n)
get_risk_free_rate = web.DataReader(name='^TNX', data_source='yahoo')['Adj Close']
risk_free_rate = round(get_risk_free_rate.iloc[-1], 3)/100

print('Running Monte Carlo Simulation... Please Wait...')

for i in range(n):
    weight = weight = np.random.random(get_no_of_tickers)
    weight /= weight.sum()
    weights[i] = weight
    
    exp_rtns[i] = np.sum(log_returns.mean()*weight)*252
    exp_vols[i] = np.sqrt(np.dot(weight.T, np.dot(log_returns.cov()*252, weight)))
    sharpe_ratios[i] = (exp_rtns[i] - risk_free_rate) / exp_vols[i]

max = sharpe_ratios.max()
loc = sharpe_ratios.argmax()
optimal_weights = np.round(weights[loc], 4)

# Step 4. Outputting the Optimal Portfolio Characteristics
print('Since', start, 'the optimal portfolio has had a return of', str(round((exp_rtns[sharpe_ratios.argmax()]*100), 2)) + '%')
print('The Sharpe Ratio of this portfolio is', round(max, 4), '\n'
'Listed below are the specific weightings for this portfolio:')
stocks = df.columns.values
ow = optimal_weights.tolist()
portfolio_allocation = dict(zip(stocks, ow))
for key, value in portfolio_allocation.items():
    print(f'{key:8s}| {value}')

# Step 5. Plotting the Minimum Variance Frontier
fig, ax = plt.subplots()
ax.scatter(exp_vols, exp_rtns, c=sharpe_ratios) # colour the sharpe ratios
ax.scatter(exp_vols[sharpe_ratios.argmax()], exp_rtns[sharpe_ratios.argmax()], c='r')
ax.set_xlabel('Expected Volatility')
ax.set_ylabel('Expected Return')
ax.set_title('The Optimal Portfolio Allocation')
plt.show()



