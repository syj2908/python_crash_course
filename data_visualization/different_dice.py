import pygal
from die import Die

#创建一个D6和D10
die1 = Die()
die2 = Die(10)

#掷几次骰子，并将结果存在一个列表里
results = []
for roll_num in range(50000):
    result = die1.roll() + die2.roll()
    results.append(result)

#分析结果
frequencies = []
max_result = die1.num_sides + die2.num_sides
for value in range(1, max_result + 1):
    frequency = results.count(value)
    frequencies.append(frequency)
    
#结果可视化
hist = pygal.Bar()
hist.title = "Results of rolling a D6 and a D10 50000 times"
hist.xlabels = []
for num in range(2, die1.num_sides + die2.num_sides + 1):
    hist.xlabels.append(str(num))
hist.x_title = "Result"
hist.y_title = "Frequency of Result"

hist.add("D6+D10", frequencies)
hist.render_to_file("different_dice.svg")