# Class for packages
class Package:
    def __init__(
        self, ID, address, city, state, zipcode, deadline_time, weight, status
    ):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.status = status
        self.departue_time = None
        self.delivery_time = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.ID,
            self.address,
            self.city,
            self.state,
            self.zipcode,
            self.deadline_time,
            self.weight,
            self.delivery_time,
            self.status,
        )

    def update_status(self, convert_time):
        if self.delivery_time < convert_time:
            self.status = "Delivered"
        elif self.departue_time > convert_time:
            self.status = "En Route"
        else:
            self.status = "At Hub"        