from numpy import loadtxt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

dataset = loadtxt('dataset.csv', delimiter=",")

X = dataset[:,0:11]
Y = dataset[:,11]

seed = 7
test_size = 0.5
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

model = XGBClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]

accuracy = metrics.accuracy_score(y_test, predictions)
matrix = metrics.confusion_matrix(y_test, predictions)
f1 = metrics.f1_score(y_test, predictions)
jaccard = metrics.jaccard_score(y_test, predictions)
precision = metrics.precision_score(y_test, predictions)
recall = metrics.recall_score(y_test, predictions)
metrics.RocCurveDisplay.from_predictions(y_test, predictions)

print("--------------------------------------")
print("Accuracy: %.2f%%" % (accuracy * 100.0))
print("--------------------------------------")
print("Confusion Matrix: ")
print(matrix)
print("--------------------------------------")
print("F1 Score: " + str(f1))
print("--------------------------------------")
print("Jaccard Score: " + str(jaccard))
print("--------------------------------------")
print("Precision: " + str(precision))
print("--------------------------------------")
print("Recall: " + str(recall))
print("--------------------------------------")
plt.show()