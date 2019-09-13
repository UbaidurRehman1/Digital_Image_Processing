import numpy as np

#list of values
cvalues = [20.1, 20.8, 21.9, 22.5, 22.7, 22.3, 21.8, 21.2, 20.9, 20.1]

#C is one dimensional array
C = np.array(cvalues)

#printing the one dimensional array
print('Celcius', C)

#converting whole one dimensional array into Farenheit value
F = C * 9 / 5 + 32;

print('Farenheit', F)

print('Type of C', type(C))

#------------------------------metplotlib------------------------#
import matplotlib.pyplot as plt
plt.plot(C)
plt.show()
