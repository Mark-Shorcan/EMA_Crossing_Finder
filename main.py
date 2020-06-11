import math
import threading
import time
from datetime import datetime

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import tkinter as tk

# Your key here
from pytz import timezone

key = 'F8239J848BHL7DBL'
# Chose your output format, or default to JSON (python dict)
ts = TimeSeries(key, output_format='JSON')
ti = TechIndicators(key)

symbols = []
wolf = []
bear = []

window = tk.Tk()

frame_enter = tk.Frame()
frame_load = tk.Frame()
frame_result = tk.Frame()


def home():
    frame_result.pack_forget()
    frame_enter.pack()


def compare_ema(symbol, ema1, ema2):
    index = 0 if datetime.now(timezone('America/New_York')).hour >= 16 else 1
    if ema1[index]['EMA'] >= ema2[index]['EMA'] and ema1[index + 1]['EMA'] < ema2[index + 1]['EMA']:
        wolf.append(symbol) if symbol not in wolf else wolf
    elif ema1[index]['EMA'] <= ema2[index]['EMA'] and ema1[index + 1]['EMA'] > ema2[index + 1]['EMA']:
        bear.append(symbol) if symbol not in bear else bear


def find_ema(symbol):
    ema4_dict, ema4_meta = ti.get_ema(symbol=symbol, time_period='4')
    ema8_dict, ema8_meta = ti.get_ema(symbol=symbol, time_period='8')
    ema26_dict, ema26_meta = ti.get_ema(symbol=symbol, time_period='26')
    ema50_dict, ema50_meta = ti.get_ema(symbol=symbol, time_period='50')

    ema4 = list(ema4_dict.values())
    ema8 = list(ema8_dict.values())
    ema26 = list(ema26_dict.values())
    ema50 = list(ema50_dict.values())

    # EMA comparision
    compare_ema(symbol, ema4, ema8)
    compare_ema(symbol, ema26, ema50)


def start():
    print(symbols)
    for symbol in symbols:
        x = threading.Thread(target=find_ema, args=(symbol,))
        x.start()
        time.sleep(60)
    print(wolf)
    print(bear)
    lbl_wolf['text'] = 'wolf: ' + ','.join(wolf)
    lbl_bear['text'] = 'bear: ' + ','.join(bear)
    frame_load.pack_forget()
    frame_result.pack()


def load():
    global symbols
    symbols = lbl_entry.get().strip().replace(" ", "").split(",")
    frame_enter.pack_forget()
    frame_load.pack()
    lbl_symbols['text'] = "You have entered: " + ','.join(symbols)
    hour = math.floor(len(symbols) / 60)
    min = len(symbols) % 60
    lbl_total['text'] = "Total Symbols: " + str(len(symbols))
    lbl_estimate['text'] = "Estimate time: " + str(hour) + " hour " + str(min) + " min."


# enter info frame
lbl_names = tk.Label(text="Enter the symbol here, split them with comma(max 100 per day)", master=frame_enter)
lbl_names.pack()
lbl_entry = tk.Entry(width=100, master=frame_enter)
lbl_entry.pack()
btn_ok = tk.Button(text="Ok", bg="blue", fg="white", master=frame_enter, command=load)
btn_ok.pack()


# load frame
lbl_symbols = tk.Label(text="You have entered: ", master=frame_load, wraplength=600)
lbl_symbols.pack()
lbl_total = tk.Label(text="", master=frame_load)
lbl_total.pack()
lbl_estimate = tk.Label(text="", master=frame_load)
lbl_estimate.pack()
btn_start = tk.Button(text="Start", bg="blue", fg="white", master=frame_load, command=start)
btn_start.pack()

# result frame
lbl_wolf = tk.Label(text="Wolf:", master=frame_result, wraplength=600)
lbl_wolf.pack()
lbl_bear = tk.Label(text="Bear:", master=frame_result, wraplength=600)
lbl_bear.pack()
btn_home = tk.Button(text="Back",  bg="blue", fg="white", master=frame_result, command=home)
btn_home.pack()


frame_enter.pack()


btn_ok.bind()
window.mainloop()





