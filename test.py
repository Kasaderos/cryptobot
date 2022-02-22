from main import get_data
from binance import Client
from model import LM
import numpy as np
import matplotlib.pyplot as plt

FORECAST_STEPS = 6
WINDOW = 1000

x = np.linspace(0, 10*np.pi, WINDOW + FORECAST_STEPS)
y = np.sin(x)

train = y[:WINDOW]
test = y[WINDOW:]

preds = LM(train, FORECAST_STEPS)

t = np.arange(len(x))
plt.plot(t, y, '-')
plt.plot(t, np.append(train, preds), '--')
plt.axvline(x=WINDOW)
plt.savefig('test_1.png')

plt.clf()
_, ts = get_data()
preds = LM(ts, FORECAST_STEPS)
t = np.arange(len(ts)+FORECAST_STEPS)
plt.plot(t[:len(t)-FORECAST_STEPS], ts)
plt.plot(t, np.append(ts, preds), 'r--')
print(preds)
plt.savefig('test_2.png')
plt.close()
