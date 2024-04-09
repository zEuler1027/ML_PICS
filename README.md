# Notes

> 2023.01.23

**TITLE:** 建立一种用于动态预测脓毒症患者诱发PICS的机器学习方法

## 整体思路

参考这篇论文：
*A Machine-Learning Approach for*
*Dynamic Prediction of Sepsis-Induced Coagulopathy*
*in Critically Ill Patients With Sepsis.pdf*

1. 建立 Full Model（尽可能多的变量）
2. 用 Cross Validation 比较若干模型，取最好的进行后续操作
3. 用 SHAP 解释各个变量对结果的贡献程度
4. 取 SHAP Value 最大且方便测量的部分变量建立 Compact Model（简化版模型）
5. 用 Bayesian Optimization 优化超参数
6. 基于 Compact Model 构建在线工具

## 目前进展

Full Model 已完成。具体数据信息：
使用 eICU 中的数据，选取了57个自变量，对第二天的 PICS 情况进行预测。
（训练数据的输出为：当天或第二天满足PICS条件。）
共17,729位病人、100,308条数据，正例占3.85%。

接着，使用14种模型进行了10折交叉验证，目前结果如下：

|   Model Name | Accuracy Mean | Accuracy Std | AUC Mean | AUC Std |
|-------------:|--------------:|-------------:|---------:|--------:|
|     CatBoost |        0.9956 |       0.0011 |   0.9961 |  0.0012 |
|      LightGB |        0.9952 |       0.0014 |   0.9961 |  0.0015 |
|      XGBoost |        0.9951 |       0.0011 |   0.9943 |  0.0018 |
|       HistGB |        0.9944 |       0.0015 |   0.9956 |  0.0016 |
|     AdaBoost |        0.9930 |       0.0019 |   0.9947 |  0.0017 |
| DecisionTree |        0.9892 |       0.0020 |   0.9487 |  0.0129 |
|          MLP |        0.9816 |       0.0037 |   0.9747 |  0.0083 |
|          SVM |        0.9731 |       0.0031 |   0.9573 |  0.0107 |
|     Logistic |        0.9656 |       0.0066 |   0.9555 |  0.0116 |
|   ExtraTrees |        0.9615 |       0.0065 |   0.9772 |  0.0061 |
|   NaiveBayes |        0.9615 |       0.0065 |   0.6887 |  0.0337 |
|        Ridge |        0.9614 |       0.0065 |   0.9525 |  0.0130 |
|          LDA |        0.9608 |       0.0097 |   0.9525 |  0.0130 |
|          KNN |        0.9506 |       0.0055 |   0.5439 |  0.0250 |

选取 CatBoost 作为 Full Model 的最终结果。
使用 SHAP 解释模型，得出各变量的 SHAP Value 排名。

根据 SHAP Value 和数据常见程度排序，选择前15个作为 Compact Model 的自变量:
offset、albumin、lymph、heart rate、respiration rate、total protein、
Hct、creatinine、pH、calcium、WBC、BMI、AST、platelet、MAP。

使用以上选出的自变量训练 Compact Model，并用 Bayesian Optimization 优化超参数。
目前最优参数为：

| Parameter Name  | Value   |
|:----------------|:--------|
| `depth`         | 6       |
| `iterations`    | 350     |
| `l2_leaf_reg`   | 17.6845 |
| `learning_rate` | 0.0282  |

优化后 Compact Model 的表现：

- Accuracy: 0.9612 (std: 0.0066)
- AUC: 0.9069 (std: 0.0142)

至此，得到优化后的 Compact Model。

## 后续计划

1. 使用 Compact Model 构建在线检测工具
2. 论文
3. 论文
4. 论文
