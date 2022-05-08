class Car:
    def __init__(self,brand,color,weigh,gasoline,category,series):
        self.brand = brand
        self.color = color
        self.weigh = weigh
        self.gasoline = gasoline
        self.category = category
        self.series = series
class Bmw(Car):
    def __init__(self,brand,color,weigh,gasoline,category,series):
        super().__init__(brand,color,weigh,gasoline,category,series)
        self.gasoline = 20

    def details(self):
        print(f"Brand:{self.brand} \nSeries:{self.series} \nColor:{self.color} \nWeigh:{self.weigh} \nBensine Gasoline to 100km: {self.gasoline} Litre \nCategory:{self.category}" )

class Mercedes(Car):
    def __init__(self,brand,color,weigh,gasoline,category,series):
        super().__init__(brand,color,weigh,gasoline,category,series)
        self.gasoline = 25

    def details(self):
        print(f"Brand:{self.brand} \nSeries:{self.series} \nColor:{self.color} \nWeigh:{self.weigh} \nBensine Gasoline to 100km: {self.gasoline} Litre \nCategory:{self.category}")


bmw = Bmw("BMW","RED","1T",0,"SEDAN","E46")
bmw.details()
print("--Second--")
merc = Mercedes("Mercedes Benz","Blue","1.5T",0,"Coupe","C300")
merc.details()