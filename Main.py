# WGU C950 Judah Kerr ID: 010608610
import csv
import datetime

from Hashmap import CreateHashMap
from Package import Package
from Truck import Truck

# Read the distance csv file
with open("CSV/distance.csv") as csvfile:
    csv_distance = csv.reader(csvfile)
    csv_distance = list(csv_distance)

# Read the address csv file
with open("CSV/address.csv") as csvfile:
    csv_address = csv.reader(csvfile)
    csv_address = list(csv_address)


# Read the package csv file and create a package class from each line
# Insert each package into the Package Hash Map
def loadPackageData(fileName):
    with open(fileName, "r", encoding="utf-8-sig") as packages:
        packageData = csv.reader(packages, delimiter=",")

        for package in packageData:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pStatus = "At Hub"

            p = Package(pID, pAddress, pCity, pState, pZip, pDeadline, pWeight, pStatus)
            # Print out each package class created
            # print(p)

            packageHashMap.insert(pID, p)


# Create Hash Map instance
packageHashMap = CreateHashMap()

loadPackageData("CSV/package.csv")


# Reads the distance csv file and finds the distance. The x value is the row and the y value is the value in that row
def distance_in_between(x_value, y_value):
    distance = csv_distance[x_value][y_value]
    if distance == "":
        distance = csv_distance[y_value][x_value]

    return float(distance)


# Returns the row number as an int for an address
def extractAddress(address):
    for row in csv_address:
        if address in row[2]:
            return int(row[0])


# Create the 3 truck objects
truck1 = Truck(
    None,
    18,
    16,
    [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40],
    0.0,
    "4001 South 700 East",
    datetime.timedelta(hours=8),
)
truck1.depart_time = datetime.timedelta(hours=8)

truck2 = Truck(
    None,
    18,
    16,
    [3, 6, 7, 11, 12, 17, 18, 21, 23, 25, 28, 32, 36, 38],
    0.0,
    "4001 South 700 East",
    datetime.timedelta(hours=9, minutes=5),
)
truck2.depart_time = datetime.timedelta(hours=9, minutes=5)

truck3 = Truck(
    None,
    18,
    16,
    [2, 4, 5, 8, 9, 10, 22, 24, 26, 27, 33, 35, 39],
    0.0,
    "4001 South 700 East",
    datetime.timedelta(hours=9, minutes=5),
)
truck3.depart_time = min(truck1.time, truck2.time)


# Nearest Neighbor delivery algorithm
def nearest_neighbor_initial_route(truck):
    truckStops = []
    truckMileage = 0

    current_address = "4001 South 700 East"

    while len(truck.packages) > 0:
        shortestStop = float("inf")
        closest_package = None

        for package_id in truck.packages:
            package = packageHashMap.search(package_id)
            distance = distance_in_between(
                extractAddress(package.address), extractAddress(truck.address)
            )

            if distance < shortestStop:
                shortestStop = distance
                closest_package = package

        if closest_package:
            truckStops.append(closest_package.ID)
            truckMileage += shortestStop
            current_address = closest_package.address
            truck.packages.remove(closest_package.ID)

    return_trip_distance = distance_in_between(
        extractAddress(current_address), extractAddress("4001 South 700 East")
    )
    truckMileage += return_trip_distance

    truck.mileage = truckMileage

    # print('Total mileage with Nearest Neighbor = {:.2f}'.format(truck.mileage))
    # print('Truck stops with Nearest Neighbor = ' + str(truckStops))
    return truckStops


# 2-Opt Algorithm - Takes in the Nearest Neighbor route and reverses 2 non-adjacent edges to see if it improves
def two_opt(route):
    improved = True
    best_distance = calculate_route_distance(route)

    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue  # No improvement from reversing two adjacent edges
                new_route = route[:i] + route[i:j][::-1] + route[j:]

                new_distance = calculate_route_distance(new_route)

                # To visually see the reversing of the 2-Opt Algo
                # print(str(new_route) + ' Distance = ' + str(new_distance))

                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
                    improved = True

    return route


# Calculates the total distance of a route
def calculate_route_distance(route):
    distance = 0
    for i in range(len(route) - 1):
        packageAddress1 = packageHashMap.search(route[i])
        packageAddress2 = packageHashMap.search(route[i + 1])
        distance += distance_in_between(
            extractAddress(packageAddress1.address),
            extractAddress(packageAddress2.address),
        )
    return distance


def optimizeRoute(truck):
    # Use nearest-neighbor to generate an initial route
    current_route = nearest_neighbor_initial_route(truck)

    # Apply the 2-Opt Algorithm to improve the route
    optimized_route = two_opt(current_route)

    # Calculate total mileage using the optimized route
    total_mileage = calculate_route_distance(optimized_route)

    truck.mileage = total_mileage
    # Load the truck with the optimal route
    truck.packages = optimized_route
    # print('Total mileage with 2-Opt = {:.2f}'.format(truck.mileage))
    # print('Truck stops with 2-Opt = ' + str(optimized_route))

    return optimizeRoute


def calculate_travel_time(package1, package2, speed):
    distance = distance_in_between(
        extractAddress(package1.address), extractAddress(package2.address)
    )
    time_hours = distance / speed
    return time_hours


# Function to deliver packages and track delivery times
def deliverPackages(truck):
    current_time = datetime.timedelta(hours=0)
    print(str(truck.packages))
    delivered_packages = []

    for i in range(len(truck.packages) - 1):
        package1 = packageHashMap.search(truck.packages[i])
        package2 = packageHashMap.search(truck.packages[i + 1])

        # Calculate travel time to the next package
        travel_time_hours = calculate_travel_time(package1, package2, truck.speed)
        travel_time = datetime.timedelta(hours=travel_time_hours)

        # Update the delivery time for the next package
        current_time += travel_time
        delivery_time = truck.depart_time + current_time
        package1.delivery_time = delivery_time

        # Append the package to the list of delivered packages
        delivered_packages.append(package1)

    # Deliver the last package
    last_package = packageHashMap.search(truck.packages[-1])
    hub_address = "4001 South 700 East"
    return_to_hub_time_hours = calculate_travel_time(
        last_package, Package(-1, hub_address, "", "", "", "", "", ""), truck.speed
    )
    return_to_hub_time = datetime.timedelta(hours=return_to_hub_time_hours)

    # Update the last packages delivery time
    current_time += return_to_hub_time
    last_package.delivery_time = truck.depart_time + current_time
    delivered_packages.append(last_package)

    # Calculate and print the time when the truck gets back to the hub
    return_time_to_hub = truck.depart_time + current_time + return_to_hub_time
    print(f"Truck left at {truck.depart_time}")

    # Print out the delivery times for each package
    for package in delivered_packages:
        print(f"Package {package.ID} delivered at {package.delivery_time}")

    print(f"Truck returned to the hub at {return_time_to_hub}")
    truck.time = return_time_to_hub


# Call for each truck
print("Truck 1")
optimizeRoute(truck1)
deliverPackages(truck1)
print("-------------------------------------------------")
print("Truck 2")
optimizeRoute(truck2)
# Moving package #25 to the front of the route because of a deadline
truck2.packages.pop(10)
truck2.packages.insert(0, 25)
deliverPackages(truck2)
print("-------------------------------------------------")
print("Truck 3")
# Set truck 3's depart time to the earliest a truck gets back
truck3.depart_time = min(truck1.time, truck2.time)
optimizeRoute(truck3)
deliverPackages(truck3)
