import numpy as np
import MySQLdb

Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="", db="len")

train_dataX = np.array([0,0,0])
train_dataY = np.array([0,0])


def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)

    return 1/(1+np.exp(-x))



Cursor = Con.cursor()
#print "y"
Cursor.execute("SELECT * FROM finalnndata")
rev = Cursor.fetchall()
for r in rev:
    temp = np.array([int(r[0]),int(r[1]),int(r[2])])
    temp2 = np.array([int(r[3]),int(r[4])])
    train_dataX = np.vstack([train_dataX,temp])
    train_dataY = np.vstack([train_dataY,temp2])
print train_dataX
print train_dataY
X = train_dataX
y = train_dataY


# X = np.array([[0,0,1],
#             [0,1,1],
#             [1,0,1],
#             [1,1,1]])
                

print y
np.random.seed(1)

# randomly initialize our weights with mean 0
syn0 = 2*np.random.random((3,4)) - 1
syn1 = 2*np.random.random((4,2)) - 1

for j in xrange(60000):

	# Feed forward through layers 0, 1, and 2
    l0 = X
    l1 = nonlin(np.dot(l0,syn0))
    l2 = nonlin(np.dot(l1,syn1))

    # how much did we miss the target value?
    l2_error = y - l2
    
    if (j% 10000) == 0:
        print "Error:" + str(np.mean(np.abs(l2_error))) + " : "+str(j)
        
    # in what direction is the target value?
    # were we really sure? if so, don't change too much.
    l2_delta = l2_error*nonlin(l2,deriv=True)

    # how much did each l1 value contribute to the l2 error (according to the weights)?
    l1_error = l2_delta.dot(syn1.T)
    
    # in what direction is the target l1?
    # were we really sure? if so, don't change too much.
    l1_delta = l1_error * nonlin(l1,deriv=True)

    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)


print syn0
print syn1
a = np.array([[0,5,8]])
b = nonlin(np.dot(a,syn0))
c = nonlin(np.dot(b,syn1))

print c