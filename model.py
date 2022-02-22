import numpy as np
from sklearn.linear_model import LinearRegression

def LM(ts, p):
    X = np.array([ts[i-p:i] for i in range(p, len(ts)-1)])
    y = np.array([ts[i] for i in range(p+1, len(ts))])

    reg = LinearRegression().fit(X, y)
    print(f"R^2= {reg.score(X, y)}")

    preds = np.zeros(p)
    past = ts[len(ts)-p:]
    value = None
    for i in range(p):
        value = np.dot(reg.coef_, np.transpose(past))
        preds[i] = value
        past = np.append(past, value)
        past = past[1:]

    return preds

