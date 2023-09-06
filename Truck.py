# Truck class for the delivery trucks

class Truck:
    def __init__(self, load, speed, capacity, packages, mileage, address, depart_time):
        self.load = load
        self.speed = speed
        self.capacity = capacity
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        return     "%s, %s, %s, %s, %s, %s, %s" % (self.load, self.speed, self.capacity, self.packages, self.mileage, self.address, self.depart_time)
