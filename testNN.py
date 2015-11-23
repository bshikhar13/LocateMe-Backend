import numpy as np
from decimal import Decimal

def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return (1/(1+np.exp(-x)))
	



syn0 = np.array([[ -1.65955991e-01,  -4.42840532e+03 , -9.99771250e-01  , 5.13744775e+00],[ -7.06488218e-01 , -2.85186029e+03 , -6.27479577e-01 ,  5.31970575e+00],[ -2.06465052e-01 , -4.28846351e+03 , -1.61610971e-01  , 8.41721600e+00]])
syn1 = np.array([[ 14792.10704796 , 33958.48909182],[ 14554.26118256 , 32265.24741594],[ 14792.53275306 , 33957.8502366 ],[ 14791.95818173 , 33956.98738754]])

syn0[0] = [Decimal(i) for i in syn0[0]]
syn0[1] = [Decimal(i) for i in syn0[1]]
syn0[2] = [Decimal(i) for i in syn0[2]]

syn1[0] = [Decimal(i) for i in syn1[0]]
syn1[1] = [Decimal(i) for i in syn1[1]]
syn1[2] = [Decimal(i) for i in syn1[2]]
syn1[3] = [Decimal(i) for i in syn1[3]]

a = np.array([[-73,-41,-76]])
a[0] = [Decimal(i) for i in a[0]]
print np.dot(a,syn0)[0]

#nonlin(Decimal(-10000))
inter1 = np.dot(a,syn0)[0]
inter1 = [Decimal(i) for i in inter1]
b = nonlin(np.array(inter1))
print b
print type(a[0][0])
inter2 = np.dot(b,syn1)
inter2 = [Decimal(i) for i in inter2]
c = nonlin(np.array(inter2))
#c = nonlin(np.dot(b,syn1))

print c