import os
import csv
import copy
import math

BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, 'TrainingData.csv')
reader = csv.DictReader(file(file_path,'rb'))
data = []
selectedAttr = 'target_11_1601'

def missingHandler_global(data):
    dataList = []
    dataList = copy.deepcopy(data)
    for x in dataList:
        if x[selectedAttr] == 'NA':
            x[selectedAttr] = "-1000000"
            #Selected transformaed number by www.kaggle.com
    return dataList

def missingHandler_avg(data):
    dataList = []
    dataList = copy.deepcopy(data)
    avg = 0.0
    for x in dataList:
        if x[selectedAttr] != 'NA':
            avg += float(x[selectedAttr])
    avg /= len(dataList)
    for x in dataList:
        if x[selectedAttr] == 'NA':
            x[selectedAttr] = "%f" % avg
    return dataList
def standardize_minmax(data):
    dataList = []
    dataList = copy.deepcopy(data)
    dataMin = 100.0
    dataMax = -100.0
    for x in dataList:
        if x[selectedAttr] == 'NA' or x[selectedAttr] == "-1000000":
            continue
        if float(x[selectedAttr]) < dataMin:
            dataMin = float(x[selectedAttr])
        if float(x[selectedAttr]) > dataMax:
            dataMax = float(x[selectedAttr])
    for x in dataList:
        x[selectedAttr] = "%.15f" % ((float(x[selectedAttr]) - dataMin) / (dataMax - dataMin) * (1 - 0) + 0)
    return dataList

def standardize_decimal(data):
    dataList = []
    dataList = copy.deepcopy(data)
    dataMax = -100.0
    for x in dataList:
        if x[selectedAttr] == 'NA' or x[selectedAttr] == "-1000000":
            continue
        if float(x[selectedAttr]) > dataMax:
            dataMax = float(x[selectedAttr])
    p = pow(10, int(math.log10(dataMax)) + 1)

    for x in dataList:
        x[selectedAttr] = "%.15f" % (float(x[selectedAttr]) / p)
    return dataList

def pearson(x,y):
    n = len(x)
    vals = range(n)

    sumx = sum([float(x[i]) for i in vals])
    sumy = sum([float(y[i]) for i in vals])

    sumxSq = sum([x[i] ** 2.0 for i in vals])
    sumySq = sum([y[i] ** 2.0 for i in vals])

    pSum = sum([x[i] * y[i] for i in vals])

    num = pSum - (sumx * sumy / n)
    den = ((sumxSq - pow(sumx, 2) / n) * (sumySq - pow(sumy, 2) / n)) ** 0.5

    return (den == 0 and 0 or num / den)

numControl = 40
#Number of lines to be tested
index = 0

for line in reader:
    index += 1
    if index > numControl:
        break
    data.append(line)

data_missingHandeledByGlobal = missingHandler_global(data)
data_missingHandeledByAvg = missingHandler_avg(data)

data_standardize_minmax = standardize_minmax(data_missingHandeledByAvg)
data_standardize_decimal= standardize_decimal(data_missingHandeledByAvg)

solarRadiation64 = []
target157 = []
for x in data_standardize_decimal:
    solarRadiation64.append(float(x["Solar.radiation_64"]))
    target157.append(float(x["target_1_57"]))
r_solarRadiation64_target157 = pearson(solarRadiation64, target157)
print r_solarRadiation64_target157