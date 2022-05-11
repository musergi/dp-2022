import numpy as np
import matplotlib.pyplot as plt

with open('adult_train.csv') as f:
    data = list(map(lambda l: int(l.split(',')[0]), f.readlines()[1:]))
print(f'{min(data)=}')
print(f'{max(data)=}')

min_age = 0
max_age = 126
data = np.array(data)
gs1 = max(map(abs, [max_age - min(data), max(data) - min_age]))
print(f'{gs1=}')
epsilons = np.logspace(0.01, 3, 30)
mses = []
"""
for epsilon in epsilons:
    it_results = []
    for iteration in range(25):
        noise = np.random.laplace(0, gs1 / epsilon, len(data))
        perturbed = data + noise
        m = np.mean(perturbed)
        it_results.append(m)
    true_mean = np.mean(data)
    diff = np.array(it_results) - true_mean
    mse = sum(diff * diff) / len(it_results)
    mses.append(mse)
plt.plot(epsilons, mses)
plt.xscale('log')
plt.show()
"""

gs2 = 1
print(f'{gs2=}')
"""
bins = list(map(lambda age: sum(data == age), range(min_age, max_age + 1)))
for epsilon in epsilons:
    it_results = []
    for iteration in range(25):
        noise = np.random.laplace(0, gs2 / epsilon, len(bins))
        perturbed = bins + noise
        m = sum(map(lambda p: p[0] * p[1], enumerate(perturbed))) / sum(perturbed)
        it_results.append(m)
    true_mean = np.mean(data)
    diff = np.array(it_results) - true_mean
    mse = sum(diff * diff) / len(it_results)
    mses.append(mse)
plt.plot(epsilons, mses)
plt.xscale('log')
plt.show()
"""

gs3 = gs1
print(f'{gs3=}')
for epsilon in epsilons:
    it_results = []
    true_mean = np.mean(data)
    for iteration in range(25):
        noise = np.random.laplace(0, gs2 / epsilon, 1)
        perturbed = true_mean + noise
        it_results.append(perturbed)
    diff = np.array(it_results) - true_mean
    mse = sum(diff * diff) / len(it_results)
    mses.append(mse)
plt.plot(epsilons, mses)
plt.xscale('log')
plt.show()
