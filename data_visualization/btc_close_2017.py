import json
import pygal
import math

#将数据加载到一个列表中
file_path = r"D:\Algorithm\Python_code\data_visualization\json_files\btc_close_2017.json"
with open(file_path) as f:
    btc_data = json.load(f)
#创建五个列表分别存储日期和收盘价
dates = []
months = []
weeks = []
weekdays = []
close = []

for btc_dict in btc_data:
    dates.append(btc_dict["date"])
    months.append(int(btc_dict["month"]))
    weeks.append(int(btc_dict["week"]))
    weekdays.append(btc_dict["weekday"]) 
    close.append(int(float(btc_dict["close"])))
    #小数字符串一定要先转换成float类型再转换成int

line_chart = pygal.Line(x_label_rotation=20, show_minor_x_labels=False)
line_chart.title = "收盘价对数变换（￥）"
line_chart.x_labels = dates
N = 20  #x坐标轴每隔20天显示一次
line_chart.x_labels_major = dates[::N]
close_log = [math.log10(x) for x in close]
line_chart.add("收盘价", close_log)
line_chart.render_to_file("收盘价对数变换折线图（￥）.svg")
    