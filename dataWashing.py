# ！/usr/bin/python
# -*-coding: utf8 -*-
import math
import numpy as np

# raw data's m*n
LINENUM = 0
COLUMNNUM = 0

#the null flag
NULLSTD = -4100000.0
NULLFLAG = -4200000.0

# raw data's columns's standard range
STANDARDRANGE = {}


# load standard range:
def loadStandardRange(filePath):
    """
    读取各个位点规定范围数据, 装入全局变量STANDARDRANGE
    :param filePath: 位点数据规定位置
    :return: null
    """
    with open(filePath) as f:
        lines = f.readlines()
        #lines = []
        #maxR = -1000000000000
        #minR = 1000000000000
        for line in lines:
            line = line.strip('\n')
            posPointRange = {}
            newl = line.split(" ")
            posPointRange["idx"] = int(newl[0])
            posPointRange["enName"] = newl[1]
            extremums = [] # for example: ["-1", "0.245"]
            if len(newl) == 4:
                rStr = newl[2]
                posPointRange["delta"] = float(newl[3])
            elif len(newl) == 3:
                rStr = newl[2]
                posPointRange["delta"] = float(0)
            else:
                print("error: the standard range file format is not correct")
                print(line, newl)
            #print(newl)
            if rStr[0] == '-':  # -65-(-12.3)
                #print(rStr)
                if "(" in rStr:
                    extremums.append(rStr[:rStr.find("(") - 1])
                    extremums.append(rStr[(rStr.find("(") + 1) : rStr.find(")")])
                    #print(extremums)
                else:
                    extremums.append(rStr[:(rStr[1:].find("-") + 1)])
                    extremums.append(rStr[(rStr[1:].find("-") + 2):])
            else:  # 123-(-12.3)
                if "(" in rStr:
                    extremums.append(rStr[:rStr.find("(") - 1])
                    extremums.append(rStr[rStr.find("(") + 1 : rStr.find(")")])
                else:
                    #print(rStr)
                    extremums += rStr.split("-")
                    #print(extremums)
            posPointRange["min"] = float(extremums[0])
            posPointRange["max"] = float(extremums[1])
            #range is: -4000000.0  ->  150000000.0
            #maxR = max(posPointRange["max"], maxR)
            #minR = min(posPointRange["min"], minR)
            #print(extremums)
            STANDARDRANGE[newl[1]] = posPointRange
        #print("range is: ", minR , " -> ", maxR)
        print(STANDARDRANGE)


# load columns from file
def loadColumnsInfo(filePath):
    """
    从列数据文件中导入每一个列信息
    :param filePath: 列信息文件
    :return: 列信息
    """
    tmpColumnsInfo = []
    lines = []
    allLines = []
    with open(filePath) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip('\n')
            allLines.append(lines[i].split(" "))
    #print(allLines)
    #print("column lines is: %d" % (len(lines)))
    for i in range(len(allLines[0])):
        columnName = {}
        #print(allLines[0][0], allLines[0][1])
        columnName["cnName"] = allLines[1][i]
        columnName["enName"] = allLines[0][i]
        columnName["columnIdx"] = i
        tmpColumnsInfo.append(columnName)
    COLUMNNUM = len(tmpColumnsInfo)
    #print(tmpColumnsInfo)
    return tmpColumnsInfo


# load rawData from file, by column
def loadRawData(filePath):
    """
    按照列读取数据
    :param filePath: 数据文件
    :return: 按列读取的数据
    """
    allItems = []
    with open(filePath) as f:
        lines = f.readlines()
        global LINENUM
        LINENUM = len(lines)
        for line in lines:
            line = line.strip('\n')
            allItems.append(line.split(" "))
    global COLUMNNUM
    COLUMNNUM = len(allItems[0])
    #print(allItems)
    storeByColumn = []
    for j in range(COLUMNNUM):
        columnData = []
        for i in range(LINENUM):
            if j == 0:
                columnData.append(allItems[i][j])
            else:
                columnData.append(float(allItems[i][j]))
        storeByColumn.append(columnData)
    #print("data is", storeByColumn)
    #print(LINENUM, " ", COLUMNNUM)
    return storeByColumn

# load

# rawData: store by column
class RawData:
    def __init__(self, columnsInfoFilePath, dataFilePath, stdRangeFilePath, defectiveThreshold):
        """
        init the raw data into RawData
        :param columnsInfoFilePath: 列信息文件
        :param dataFilePath: 数据文件
        :param stdRangeFilePath: 标准范围文件
        :param defectiveThreshold: 数据缺陷比例阈值
        """
        # initial COLUMNNUM
        self.rawDataColumnsInfo = loadColumnsInfo(columnsInfoFilePath)
        # load data by column
        self.dataByColumn = loadRawData(dataFilePath)
        # index by columnInfo's enName
        self.rawData = {}
        # column defective ratio: num(values == 0) / num(all values)
        self.defectRatio = {}
        # if a defective column data is acceptable
        self.defectiveThreshold = defectiveThreshold
        # the processed res:
        self.res = {}

        # load std range
        loadStandardRange(stdRangeFilePath)
        # initial virables
        # attention: the first column of dataByColumn is time, so, dicsize of dataBycolumn is 355
        for columnInfo in self.rawDataColumnsInfo:
            self.rawData[columnInfo["enName"]] = self.dataByColumn[columnInfo["columnIdx"] + 1]
            self.defectRatio[columnInfo["enName"]] = 1

        # according to the stdRange, set somevalue to NULLFLAG
        for optValueName in self.rawData.keys():
            #print(STANDARDRANGE[optValueName])
            maxOpt = STANDARDRANGE[optValueName]["max"]
            minOpt = STANDARDRANGE[optValueName]["min"]
            defectiveValueNum = 0
            for i in range(len(self.rawData[optValueName])):
                if self.rawData[optValueName][i] > maxOpt or \
                    self.rawData[optValueName][i] < minOpt:
                    self.rawData[optValueName][i] = NULLFLAG
                    defectiveValueNum = defectiveValueNum + 1
            # cal defective ratio, judge if defect is acceptable
            self.defectRatio[optValueName] = defectiveValueNum / LINENUM
            if self.defectRatio[optValueName] > self.defectiveThreshold:
                # this colum's all value should be set as null
                for i in range(len(self.rawData[optValueName])):
                    self.rawData[optValueName][i] = NULLFLAG
            elif self.defectRatio[optValueName] > 0 :
                # use avg values to substitue the null value in those columns who
                # have deffective values but acceptable
                avgOfThisOptValue = 0
                for i in range(len(self.rawData[optValueName])):
                    if self.rawData[optValueName][i] > NULLSTD:
                        avgOfThisOptValue += self.rawData[optValueName][i]
                avgOfThisOptValue = avgOfThisOptValue / (LINENUM - defectiveValueNum)
                # set partial defective value into avg
                for i in range(len(self.rawData[optValueName])):
                    if self.rawData[optValueName][i] < NULLSTD:
                        self.rawData[optValueName][i] = avgOfThisOptValue
            # cal Avg of this column and get the self.res
            self.res[optValueName] = np.mean(self.rawData[optValueName])

if __name__ == "__main__":
    print("hello")
    #loadStandardRange("rawData/standardRange.dat")
    #loadColumnsInfo("rawData/columnsInfo.dat")
    #loadRawData("rawData/raw285.dat")
    data285 = RawData(
        "rawData/columnsInfo.csv",
        "rawData/raw285.dat",
        "rawData/standardRange.dat",
        0.25
    )
    data313 = RawData(
        "rawData/columnsInfo.csv",
        "rawData/raw313.dat",
        "rawData/standardRange.dat",
        0.25
    )
    # print the 354 option value of sample 285 and 313
    nonOptValue285 = "285 2017/7/17 8:00:00 199 89.3 60.06 14.93 25.02 53 726.5 3.2 88.1 1.2 3.61 4.8 1.25 3.37"
    optValue285 = ""
    nonOptValue313 = "313 2017/5/15 8:00:00 392 90.3 55.05 20.89 24.06 59.09 725.2 8.5 88.9 1.4 3.77 9.24 3.45 7.29"
    optValue313 = ""
    for optKey in data285.res.keys():
        optValue285 = optValue285 + str(data285.res[optKey]) + " "
    for optKey in data313.res.keys():
        optValue313 = optValue313 + str(data313.res[optKey]) + " "
    with open("resSampleData/res285.csv", "w") as f:
        f.writelines(optValue285)
    with open("resSampleData/res313.csv", "w") as f:
        f.writelines(optValue313)
    print(optValue285, "\n", optValue313)
    print(nonOptValue285 + optValue285, "\n", nonOptValue313 + optValue285)

#285 2017/7/17 8:00:00 199 89.3 60.06 14.93 25.02 53 726.5 3.2 88.1 1.2 3.61 4.8 1.25 3.37
#313 2017/5/15 8:00:00 392 90.3 55.05 20.89 24.06 59.09 725.2 8.5 88.9 1.4 3.77 9.24 3.45 7.29



