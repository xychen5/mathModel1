# -*- utf:8 -*-
#!/usr/bin/bash
import pandas as pd
import numpy as np
import dataWashing
import matplotlib.pyplot as plt
# 导入随机森林基模型
from sklearn.ensemble import RandomForestRegressor
# 导入RFE方法和线性回归基模型
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression,Ridge,Lasso

# 加载数据
data = pd.read_csv('sampleData/sampleOldData_del3.csv')

# 自变量特征
feature = data[["硫含量_原料_μg/g", "辛烷值RON_原料", "饱和烃_v%（烷烃+环烷烃）", "烯烃_v%", "芳烃_v%", "溴值_gBr/100g", "密度(20℃)_kg/m³", "辛烷值RON_产品", "焦炭_wt%", "S__wt%", "焦炭_wt%", "S__wt%", "S-ZORB.CAL_H2.PV", "S-ZORB.PDI_2102.PV", "S-ZORB.PT_2801.PV", "S-ZORB.FC_2801.PV", "S-ZORB.TE_2103.PV", "S-ZORB.TE_2005.PV", "S-ZORB.PT_2101.PV", "S-ZORB.PDT_2104.PV", "S-ZORB.SIS_PDT_2103B.PV", "S-ZORB.TC_2101.PV", "S-ZORB.TE_2301.PV", "S-ZORB.PT_2301.PV", "S-ZORB.FC_2301.PV", "S-ZORB.PC_2105.PV", "S-ZORB.PC_5101.PV", "S-ZORB.TC_5005.PV", "S-ZORB.LC_5001.PV", "S-ZORB.LC_5101.PV", "S-ZORB.TE_5102.PV", "S-ZORB.TE_5202.PV", "S-ZORB.FC_5202.PV", "S-ZORB.AT_5201.PV", "S-ZORB.PT_9301.PV", "S-ZORB.FT_9301.PV", "S-ZORB.FT_1501.PV", "S-ZORB.FT_5104.PV", "S-ZORB.FT_5101.PV", "S-ZORB.FT_9101.PV", "S-ZORB.TE_9001.PV", "S-ZORB.PT_9001.PV", "S-ZORB.FT_9001.PV", "S-ZORB.FT_9403.PV", "S-ZORB.PT_9403.PV", "S-ZORB.TE_9301.PV", "S-ZORB.FT_9201.PV", "S-ZORB.FT_9202.PV", "S-ZORB.FT_9302.PV", "S-ZORB.FT_3301.PV", "S-ZORB.FT_9402.PV", "S-ZORB.PT_9402.PV", "S-ZORB.FT_9401.PV", "S-ZORB.PT_9401.PV", "S-ZORB.PDC_2502.PV", "S-ZORB.FC_2501.PV", "S-ZORB.FT_1001.PV", "S-ZORB.FT_1002.PV", "S-ZORB.FT_1003.PV", "S-ZORB.FT_1004.PV", "S-ZORB.TE_1001.PV", "S-ZORB.FC_1005.PV", "S-ZORB.FC_1101.PV", "S-ZORB.FC_1102.PV", "S-ZORB.AT_1001.PV", "S-ZORB.TE_1105.PV", "S-ZORB.PDI_1102.PV", "S-ZORB.TE_1601.PV", "S-ZORB.SIS_TE_6010.PV", "S-ZORB.PC_6001.PV", "S-ZORB.AC_6001.PV", "S-ZORB.TE_1608.PV", "S-ZORB.TC_1606.PV", "S-ZORB.PT_6002.PV", "S-ZORB.PC_1603.PV", "S-ZORB.PT_1602A.PV", "S-ZORB.PC_1301.PV", "S-ZORB.PT_1201.PV", "S-ZORB.LC_1201.PV", "S-ZORB.FC_1201.PV", "S-ZORB.TE_1201.PV", "S-ZORB.TE_1203.PV", "S-ZORB.LC_1202.PV", "S-ZORB.FC_1203.PV", "S-ZORB.FC_1202.PV", "S-ZORB.PC_1202.PV", "S-ZORB.TC_2801.PV", "S-ZORB.FC_3101.PV", "S-ZORB.FC_3103.PV", "S-ZORB.FC_2601.PV", "S-ZORB.PC_2601.PV", "S-ZORB.PDT_2604.PV", "S-ZORB.TE_2601.PV", "S-ZORB.TC_2607.PV", "S-ZORB.AI_2903.PV", "S-ZORB.PDI_2703A.PV", "S-ZORB.PDC_2607.PV", "S-ZORB.FT_9102.PV", "S-ZORB.PT_1501.PV", "S-ZORB.FT_1002.TOTAL", "S-ZORB.FT_1004.TOTAL", "S-ZORB.FT_9001.TOTAL", "S-ZORB.FT_5104.TOTAL", "S-ZORB.FT_5201.TOTAL", "S-ZORB.FT_5101.TOTAL", "S-ZORB.FT_9101.TOTAL", "S-ZORB.FT_1501.TOTAL", "S-ZORB.FT_1003.TOTAL", "S-ZORB.FT_3301.TOTAL", "S-ZORB.FT_9201.TOTAL", "S-ZORB.FT_9202.TOTAL", "S-ZORB.FT_9301.TOTAL", "S-ZORB.FT_9302.TOTAL", "S-ZORB.FT_9401.TOTAL", "S-ZORB.FT_9402.TOTAL", "S-ZORB.FT_9403.TOTAL", "S-ZORB.FT_1202.TOTAL", "S-ZORB.FT_5201.PV", "S-ZORB.FC_1101.TOTAL", "S-ZORB.FT_1204.PV", "S-ZORB.FT_5102.PV", "S-ZORB.FT_1204.TOTAL", "S-ZORB.FT_5102.TOTAL", "S-ZORB.FC_1202.TOTAL", "S-ZORB.FT_9102.TOTAL", "S-ZORB.FT_1001.TOTAL", "S-ZORB.TE_1101.DACA", "S-ZORB.PT_1102.DACA", "S-ZORB.PT_1103.DACA", "S-ZORB.TE_1104.DACA", "S-ZORB.TE_1107.DACA", "S-ZORB.TE_1103.DACA", "S-ZORB.TE_1106.DACA", "S-ZORB.LI_9102.DACA", "S-ZORB.TE_9003.DACA", "S-ZORB.TE_9002.DACA", "S-ZORB.FT_9002.DACA", "S-ZORB.PC_9002.DACA", "S-ZORB.LT_9001.DACA", "S-ZORB.LC_5002.DACA", "S-ZORB.LC_5102.DACA", "S-ZORB.LT_3801.DACA", "S-ZORB.LT_3101.DACA", "S-ZORB.PC_3101.DACA", "S-ZORB.TE_3101.DACA", "S-ZORB.FT_3303.DACA", "S-ZORB.LC_3301.DACA", "S-ZORB.PC_3301.DACA", "S-ZORB.FT_3304.DACA", "S-ZORB.LT_1501.DACA", "S-ZORB.TE_1501.DACA", "S-ZORB.TE_1502.DACA", "S-ZORB.LC_1203.DACA", "S-ZORB.LT_2101.DACA", "S-ZORB.FT_3001.DACA", "S-ZORB.FT_2701.DACA", "S-ZORB.SIS_PT_2703", "S-ZORB.FC_2702.DACA", "S-ZORB.TC_2702.DACA", "S-ZORB.PT_2905.DACA", "S-ZORB.LT_2901.DACA", "S-ZORB.FT_2901.DACA", "S-ZORB.TE_2901.DACA", "S-ZORB.TE_2902.DACA", "S-ZORB.FT_2502.DACA", "S-ZORB.TE_2501.DACA", "S-ZORB.PT_2501.DACA", "S-ZORB.PT_2502.DACA", "S-ZORB.PDT_2503.DACA", "S-ZORB.ZT_2533.DACA", "S-ZORB.FT_2433.DACA", "S-ZORB.TE_2401.DACA", "S-ZORB.FC_2432.DACA", "S-ZORB.FT_2303.DACA", "S-ZORB.FT_2302.DACA", "S-ZORB.LT_1301.DACA", "S-ZORB.SIS_TE_2802", "S-ZORB.LT_1002.DACA", "S-ZORB.TE_5002.DACA", "S-ZORB.TE_5004.DACA", "S-ZORB.FC_5203.DACA", "S-ZORB.TE_5006.DACA", "S-ZORB.TE_5003.DACA", "S-ZORB.TE_5201.DACA", "S-ZORB.TE_5101.DACA", "S-ZORB.FT_2431.DACA", "S-ZORB.TC_2201.PV", "S-ZORB.TC_2201.OP", "S-ZORB.FT_3201.DACA", "S-ZORB.SIS_PT_2602.PV", "S-ZORB.SIS_TE_2606.PV", "S-ZORB.SIS_TE_2605.PV", "S-ZORB.PDT_2704.DACA", "S-ZORB.PDT_2703B.DACA", "S-ZORB.PDC_2702.DACA", "S-ZORB.PDI_2501.DACA", "S-ZORB.AT_1001.DACA", "S-ZORB.PT_6009.DACA", "S-ZORB.LI_2107.DACA", "S-ZORB.LI_2104.DACA", "S-ZORB.TE_6002.DACA", "S-ZORB.TE_6001.DACA", "S-ZORB.PT_1101.DACA", "S-ZORB.FT_3501.DACA", "S-ZORB.PC_3001.DACA", "S-ZORB.FC_5103.DACA", "S-ZORB.TE_5001.DACA", "S-ZORB.FT_2002.DACA", "S-ZORB.PDT_3601.DACA", "S-ZORB.PDT_3602.DACA", "S-ZORB.PT_6006.DACA", "S-ZORB.SIS_TE_6009.PV", "S-ZORB.SIS_PT_6007.PV", "S-ZORB.TE_6008.DACA", "S-ZORB.PT_5201.DACA", "S-ZORB.FC_1104.DACA", "S-ZORB.PC_3501.DACA", "S-ZORB.FT_2001.DACA", "S-ZORB.FT_2803.DACA", "S-ZORB.LT_9101.DACA", "S-ZORB.PDI_2801.DACA", "S-ZORB.PT_6003.DACA", "S-ZORB.AT_6201.DACA", "S-ZORB.PDI_2301.DACA", "S-ZORB.PDI_2105.DACA", "S-ZORB.PC_2902.DACA", "S-ZORB.FT_1502.DACA", "S-ZORB.BS_LT_2401.PV", "S-ZORB.BS_AT_2402.PV", "S-ZORB.PC_2401.DACA", "S-ZORB.BS_AT_2401.PV", "S-ZORB.PC_2401B.DACA", "S-ZORB.FT_3701.DACA", "S-ZORB.FT_3702.DACA", "S-ZORB.PT_2603.DACA", "S-ZORB.LC_2601.DACA", "S-ZORB.PDT_2605.DACA", "S-ZORB.PT_2607.DACA", "S-ZORB.PDT_2606.DACA", "S-ZORB.ZT_2634.DACA", "S-ZORB.TE_2608.DACA", "S-ZORB.TE_2603.DACA", "S-ZORB.TE_2604.DACA", "S-ZORB.DT_2001.DACA", "S-ZORB.DT_2107.DACA", "S-ZORB.TE_2104.DACA", "S-ZORB.PDT_2001.DACA", "S-ZORB.TE_2002.DACA", "S-ZORB.TE_2001.DACA", "S-ZORB.TE_2004.DACA", "S-ZORB.TE_2003.DACA", "S-ZORB.PC_2401B.PIDA.SP", "S-ZORB.PC_2401B.PIDA.OP", "S-ZORB.PC_2401.PIDA.OP", "S-ZORB.PC_2401.PIDA.SP", "S-ZORB.FT_3302.DACA", "S-ZORB.PDT_1003.DACA", "S-ZORB.PDT_1002.DACA", "S-ZORB.PDT_2409.DACA", "S-ZORB.PDT_3503.DACA", "S-ZORB.PDT_3502.DACA", "S-ZORB.PDT_2906.DACA", "S-ZORB.PDT_3002.DACA", "S-ZORB.PDT_1004.DACA", "S-ZORB.PDI_2903.DACA", "S-ZORB.PT_2901.DACA", "S-ZORB.PT_2106.DACA", "S-ZORB.FT_1301.DACA", "S-ZORB.PT_7510B.DACA", "S-ZORB.TE_7508B.DACA", "S-ZORB.PT_7508B.DACA", "S-ZORB.TE_7506B.DACA", "S-ZORB.PT_7510.DACA", "S-ZORB.TE_7508.DACA", "S-ZORB.PT_7508.DACA", "S-ZORB.TE_7506.DACA", "S-ZORB.PT_7505B.DACA", "S-ZORB.TE_7504B.DACA", "S-ZORB.PT_7503B.DACA", "S-ZORB.TE_7502B.DACA", "S-ZORB.PT_7505.DACA", "S-ZORB.TE_7504.DACA", "S-ZORB.PT_7503.DACA", "S-ZORB.PT_7502.DACA", "S-ZORB.TE_7106B.DACA", "S-ZORB.TE_7108B.DACA", "S-ZORB.PT_7107B.DACA", "S-ZORB.PT_7103B.DACA", "S-ZORB.TE_7102B.DACA", "S-ZORB.TE_7106.DACA", "S-ZORB.PT_7107.DACA", "S-ZORB.PT_7103.DACA", "S-ZORB.TE_7102.DACA", "S-ZORB.HIC_2533.AUTOMANA.OP", "S-ZORB.FC_2432.PIDA.SP", "S-ZORB.PT_1604.DACA", "S-ZORB.TC_1607.DACA", "S-ZORB.PT_6005.DACA", "S-ZORB.PT_6008.DACA", "S-ZORB.PT_1601.DACA", "S-ZORB.TE_1605.DACA", "S-ZORB.TE_1604.DACA", "S-ZORB.TE_1603.DACA", "S-ZORB.TE_1602.DACA", "S-ZORB.SIS_FT_3202.PV", "S-ZORB.TXE_3202A.DACA", "S-ZORB.TXE_3201A.DACA", "S-ZORB.TC_3203.DACA", "S-ZORB.SIS_TEX_3103B.PV", "S-ZORB.TEX_3103A.DACA", "S-ZORB.TE_3111.DACA", "S-ZORB.TE_3112.DACA", "S-ZORB.TXE_2203A.DACA", "S-ZORB.TXE_2202A.DACA", "S-ZORB.TE_5008.DACA", "S-ZORB.TE_5009.DACA", "S-ZORB.FC_5001.DACA", "S-ZORB.TE_5007.DACA", "S-ZORB.TE_1504.DACA", "S-ZORB.TE_1503.DACA", "S-ZORB.TC_3102.DACA", "S-ZORB.TE_1102.DACA", "S-ZORB.AT-0001.DACA.PV", "S-ZORB.AT-0002.DACA.PV", "S-ZORB.AT-0003.DACA.PV", "S-ZORB.AT-0004.DACA.PV", "S-ZORB.AT-0005.DACA.PV", "S-ZORB.AT-0006.DACA.PV", "S-ZORB.AT-0007.DACA.PV", "S-ZORB.AT-0008.DACA.PV", "S-ZORB.AT-0009.DACA.PV", "S-ZORB.AT-0010.DACA.PV", "S-ZORB.AT-0011.DACA.PV", "S-ZORB.AT-0012.DACA.PV", "S-ZORB.AT-0013.DACA.PV", "S-ZORB.TE_2104.DACA.PV", "S-ZORB.SIS_PDT_2103A.PV", "S-ZORB.PT_2106.DACA.PV", "S-ZORB.TE_6008.DACA.PV", "S-ZORB.TE_6001.DACA.PV", "S-ZORB.FT_1204.DACA.PV", "S-ZORB.LC_1203.PIDA.PV", "S-ZORB.FT_5102.DACA.PV", "S-ZORB.LC_5102.PIDA.PV", "S-ZORB.TE_1103.DACA.PV", "S-ZORB.TE_1104.DACA.PV", "S-ZORB.TE_1102.DACA.PV", "S-ZORB.TE_1106.DACA.PV", "S-ZORB.TE_1107.DACA.PV", "S-ZORB.TE_1101.DACA.PV", "S-ZORB.CAL.LINE.PV", "S-ZORB.CAL.CANGLIANG.PV", "S-ZORB.CAL.SPEED.PV", "S-ZORB.CAL.LEVEL.PV", "S-ZORB.RXL_0001.AUXCALCA.PV", "S-ZORB.CAL_1.CANGLIANG.PV", "S-ZORB.FT_1006.DACA.PV", "S-ZORB.FT_5204.DACA.PV", "S-ZORB.FT_1006.TOTALIZERA.PV", "S-ZORB.FT_5204.TOTALIZERA.PV", "S-ZORB.FT_1503.DACA.PV", "S-ZORB.FT_1503.TOTALIZERA.PV", "S-ZORB.FT_1504.DACA.PV", "S-ZORB.FT_1504.TOTALIZERA.PV", "S-ZORB.PC_1001A.PV"]]

lr = Ridge(alpha=100000, fit_intercept=True, normalize=True,
           copy_X=True, max_iter=1500, tol=1e-4, solver='auto')

# estimator=LinearRegression(),  # 选择lin线性回归为基模型
rfe = RFE(
    #estimator=LinearRegression(normalize=True),
    #estimator=Lasso(normalize=True),
    estimator=lr,
    #n_features_to_select=28  # 选区特征数
    n_features_to_select = 27  # 选区特征数
)

# 由于选择了一个目标，导致geature中实际上只有 367 = 366 - 1 列
# fit 方法训练选择特征属性
#sFeature = rfe.fit_transform(feature, data["RON损失（不是变量）"])
sFeature = rfe.fit_transform(feature, data[["RON损失（不是变量）", "硫含量_产品_μg/g"]])

# 2d matrix: clonum: opt Value, row:
FRMatrix = sFeature.tolist()
#print(rfe.get_support(), "type is: ", type(rfe.get_support()))
chosenFlags = rfe.get_support().tolist()
print(sFeature.tolist(), "\n\n1->", chosenFlags, "\n\n2", )
print(feature.columns[rfe.get_support()]) #查看满足条件的属性

# we delelte column 0, 1, 64, (1, 2, 65)so the real index should be:
## RON损失（不是变量）'s original index is 11(12)，
#chosenFlags = [False, False] + chosenFlags[:11] + [False] +  chosenFlags[11:62] + [False] + chosenFlags[62:]

# RON损失（不是变量）'s original index is 11(12)， 硫含量_产品_μg/g‘s original index is 9(10)
chosenFlags = [False, False] + chosenFlags[:9] + [False] + chosenFlags[9:11] + [False] +  chosenFlags[11:62] + [False] + chosenFlags[62:]

chosenIndex = []
chosenEnName = []
chosenCnName = []
#rawColumnsInfo = dataWashing.loadColumnsInfo("rawData/columnsInfo.csv")
rawColumnsInfo = dataWashing.loadColumnsInfo("sampleData/allCloumnInfo_en_cn.csv")

for i in range(len(rawColumnsInfo)):
    if chosenFlags[i] == True:
        # 16 nonOptvalues exists, the index starts from 1
        chosenIndex.append(i+1)
        chosenEnName.append(rawColumnsInfo[i]["enName"])
        chosenCnName.append(rawColumnsInfo[i]["cnName"])

# write the chosen flags into file
with open("demensionDecrease/chosenOptValues_rfeRidge2.csv", "w") as f:
    for i in chosenIndex:
        f.write(str(i) + " ")
    f.write("\n")
    for i in chosenEnName:
        f.write(str(i) + " ")
    f.write("\n")
    for i in chosenCnName:
        f.write(str(i) + " ")
    for i in range(len(chosenCnName)):
        print(chosenEnName[i], " ", chosenCnName[i])

## write the feature relationship matrix
#with open("demensinoDecrease/FRMatrix.csv", "w") as f:
#    for line in FRMatrix:
#        for item in line:
#            f.write(str(i) + " ")
#        f.write("\n")

#datafile = 'sampleData/sampleOldData_del3.csv'
#data = pd.read_csv(datafile)
#data_fea = data.iloc[:, 1:]  # 取数据中指标所在的列
#
#model = RandomForestRegressor(random_state=1, max_depth=10)
#data_fea = data_fea.fillna(0)  # 随机森林只接受数字输入，不接受空值、逻辑值、文字等类型
#data_fea = pd.get_dummies(data_fea)
#model.fit(data_fea, data.y_增长率)
#
## 根据特征的重要性绘制柱状图
#features = data_fea.columns
#importances = model.feature_importances_
#indices = np.argsort(importances[0:9])  # 因指标太多，选取前10个指标作为例子
#plt.title('Index selection')
#plt.barh(range(len(indices)), importances[indices], color='pink', align='center')
#plt.yticks(range(len(indices)), [features[i] for i in indices])
#plt.xlabel('Relative importance of indicators')
#plt.show()
#print(rfe.get_support().tolist())

