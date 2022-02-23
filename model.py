import numpy as np
from sklearn.linear_model import LinearRegression

def LM(df, lag = 3):
    data = np.array([row[1:5] for row in df])
    print(data[len(data)-lag:])
    X = np.array([data[i-lag:i].reshape((1, lag*4))[0] for i in range(lag, len(data)-1)])
    y = np.array([data[i-lag:i, 3] for i in range(lag+1, len(data))])
    # print(X)
    reg = LinearRegression().fit(X, y)
    print(f"R^2= {reg.score(X, y)}")
    past = np.array(data[len(data)-lag:len(data)].reshape((1, lag*4))[0])
    value = np.dot(reg.coef_, np.transpose(past))

    return value[0] 
