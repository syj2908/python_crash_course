from random import randint

class Die():
    """表示一个骰子的类"""

    def __init__(self, num_sides=6):
        """筛子默认六面"""
        self.num_sides = num_sides
        
    def roll(self):
        """随机返回一个[1,num_sides]间的整数"""
        return randint(1, self.num_sides)