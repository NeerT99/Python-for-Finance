# Python-for-Finance

This is an algorithm that allows you to input tickers in order to create a portfolio for which the weightings of the tickers 
within the portfolio will be optimised using the Markowitz Efficient Frontier theory. 

The program requires you to input a start date, end date, and the tickers you would like to include in the portfolio.
The algorithm then uses the tickers to run a monte carlo simulations over the chosen time period in order to obtain the
portfolio with the highest sharpe ratio (highest risk adjusted return). The algorithm will output the correlation matrix
of the tickers, the weightings and also the expected return of the optimal portfolio

note: for the program to work, you must input the tickers in capitals, and dates will be in the form of YYYY-MM-DD
