# Trading_Bot_9000
Ever want to make a trading bot that'll work for you so you can retire and live the good life? So did we

Do not run *_btc_XX.py files, since they are linked to databases that are currently updating dynamically.

But freely run any file ending in *_ta.py 

For each file OHLCV data is being dumped for every closed bar coming off of binance api.  To access the current bar, use the binance api directly.

the get_binance_btc_trades.py file is not OHLCV data, but rather trade by trade for every trade that hits binance.

