import matplotlib.pyplot as plt

from random_walk import RandomWalk

while True:
    #创建一个RandomWalk实例，并把所有点绘制出来
    rw = RandomWalk()
    rw.fill_walk()

    point_numbers = list(range(rw.num_points))
    plt.plot(rw.x_values, rw.y_values, linewidth=1)
    #plt.scatter(rw.x_values, rw.y_values, c=point_numbers,
    #    cmap=plt.cm.Blues, s=1)

    #隐藏坐标轴
    plt.axes().get_xaxis().set_visible(False)
    plt.axes().get_yaxis().set_visible(False)

    plt.show()

    kepp_running = input("keep running? (y/n): ")
    if kepp_running == "n":
        break
        