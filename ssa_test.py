from pyts.classification import BOSSVS
from pyts.datasets import load_gunpoint
X_train, X_test, y_train, y_test = load_gunpoint(return_X_y=True)
print(X_train)
clf = BOSSVS(window_size=28)
print(clf.fit(X_train, y_train))
print(clf.score(X_test, y_test))