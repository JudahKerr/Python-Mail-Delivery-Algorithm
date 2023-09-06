import csv

from Hashmap import CreateHashMap
from Package import Package

def loadPackageData(fileName):
    with open(fileName, 'r', encoding='utf-8-sig') as packages:
        packageData = csv.reader(packages, delimiter=',')
        
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

            packageHashMap.insert(pID, p)

# Create Hash Map instance
packageHashMap = CreateHashMap()

loadPackageData('CSV/package.csv')

for i in range (len(packageHashMap.table)):
    print("Key: {} and Value: {}".format(i+1, packageHashMap.search(i+1)))