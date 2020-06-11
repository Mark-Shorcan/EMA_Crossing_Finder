# StockAlert

This is used to find ema corssing for the stock symbol you entered. <br>
The data is read from Alpha Vantage API.<br>
Right now it uses a free token, which has a limit of 5 request a min and 500 total a day.<br>
It takes about a min to find the ema4, ema8, ema26 and ema 50 for each stock<br>

<br>
After read the EMAs, it compares today's ema4 and ema8 with yesterday's ema4 and ema8, if a cross happened, the stock will show up in the reuslt. <br>
Same for ema 26 and ema 50<br>
Note that it uses ema at market close, if today's market is not closed yet, it uses yesterday's data then compare with the day before yesterday.
