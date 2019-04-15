#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

x = np.random.normal(size=(1000,))
x = np.sort(x)

V = np.arange(-100, -50, 0.1)
E = -79.91


g = np.zeros((len(x), len(V)))
for i, v in enumerate(V):
    g[:, i] = 1 / (v - E + x)
del(v)


plt.figure()
plt.plot(V, g[100,:], 'r')
plt.plot(V, g[500,:])
plt.plot(V, g[900,:], 'r')

plt.ylim(-0.5, 0.5)
plt.show()


'''
g = np.zeros((len(x), len(V)))
for i, v in enumerate(V):
    g[:, i] = 1 / (v - E + x)


#g = 1 / (V - E + x)
#for i =1:length(V)
#    g(i,:) = 1.0 ./ (V(i) - E + X);
#end


print(g[0, 495:505])
print(g[1, 495:505])
print(g[2, 495:505])

print(V)

#g += x


plt.figure()
plt.plot(V, g[900, :], 'r-')
plt.plot(V, g[500, :], 'b-', lw=2)
plt.plot(V, g[100, :], 'r-')
'''

plt.show()
