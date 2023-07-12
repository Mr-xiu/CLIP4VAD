# 计算AUROC并绘图的方法
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np
import xlrd
from scipy.integrate import trapz, simps
from sklearn import metrics


def get_auroc(y_Actual: list, y_Predicted: list,title:str):
    print(len(y_Actual), len(y_Predicted))
    assert len(y_Actual) == len(y_Predicted)
    size = len(y_Actual)

    threshold = 0  # 阈值
    TPR_list = []  # ROC 的纵坐标 真阳率
    FPR_list = []  # ROC 的横坐标 假阳率

    while threshold < 1.0001:  # 设置阈值
        y_Predicted_new = []
        for i in range(0, size):  # 二分法重置预测值
            if y_Predicted[i] >= threshold:
                y_Predicted_new.append(1)
            else:
                y_Predicted_new.append(0)
        cm = confusion_matrix(y_Actual, y_Predicted_new)  # 混淆矩阵

        TP = cm[1, 1]
        TN = cm[0, 0]
        FP = cm[0, 1]
        FN = cm[1, 0]
        FPR = round(FP / (FP + TN), 3)  # 保留小数点后三位
        TPR = round(TP / (TP + FN), 3)
        TPR_list.append(TPR)
        FPR_list.append(FPR)

        threshold += 0.0001
        # while 结束

    # 作图
    plt.figure()
    plt.plot(FPR_list, TPR_list, color='green')
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)

    # 用无穷小累加积分求AUC面积
    AUC = metrics.roc_auc_score(y_Actual, y_Predicted)
    print("AUC : ", round(AUC, 3))
