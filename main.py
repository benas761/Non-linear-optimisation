from math import sqrt
import scipy
import numdifftools as nd

def f(x):
    return -x[0]*x[1]*x[2]
def g(x):
    return x[0]*x[1] + x[0]*x[2] + x[1]*x[2] - 0.5
def h(x):
    return [-x[0], -x[1], -x[2]]
def B(x, r):
    hsum = 0; hvals = h(x)
    for i in range(2):
        hsum += max(0,(hvals[i]))
    return f(x) + 1/r * (hsum**2 + g(x)**2)

fib = (-1+sqrt(5))/2
def goldenCut(X, gradient, R, l, r, x1, x2, L, y1, y2):
    prevy1, prevy2 = y1, y2
    # print("L: " + str(L))
    if y2 < y1:
        if L < 0.001:
            return r
        l = x1
        L = r - l
        x1 = x2
        y1 = y2
        x2 = l + fib * L
        y2 = B([X[0]-x2*gradient[0], X[1]-x2*gradient[1], X[2]-x2*gradient[2]], R)
    else:
        if L < 0.001:
            return l
        r = x2
        L = r - l
        x2 = x1
        y2 = y1
        x1 = r - fib * L
        y1 = B([X[0]-x1*gradient[0], X[1]-x1*gradient[1], X[2]-x1*gradient[2]], R)
    # if (abs(prevy1) + abs(prevy2))/2 < (abs(y1) + abs(y2))/2:
    #     print("fuck: prevy1 = " + str(prevy1) + "\n          y1 = " + str(y1))
    #     print("fuck: prevy2 = " + str(prevy2) + "\n          y2 = " + str(y2))
    return goldenCut(X, gradient, R, l, r, x1, x2, L, y1, y2)

def goldenCutFull(X, gradient, R, l, r):
    L = r - l
    x1 = r - fib * L
    x2 = l + fib * L
    y1 = B([X[0]-x1*gradient[0], X[1]-x1*gradient[1], X[2]-x1*gradient[2]], R)
    y2 = B([X[0]-x2*gradient[0], X[1]-x2*gradient[1], X[2]-x2*gradient[2]], R)
    return goldenCut(X, gradient, R, l, r, x1, x2, L, y1, y2)

accuracy = 10**-2
def gradientDescent(X, r):
    gradient = nd.Gradient(B)(X, r)
    print("Gradient: " + str(gradient))
    steps = 0
    while not (abs(gradient[0]) < accuracy*r and abs(gradient[1]) < accuracy*r and abs(gradient[2]) < accuracy*r):
        steps+=1
        gradient = nd.Gradient(B)(X, r)
        mult = goldenCutFull(X, gradient, r, accuracy*r, 1/r*steps**2)
        X[0] -= mult*gradient[0]
        X[1] -= mult*gradient[1]
        X[2] -= mult*gradient[2]
    print("Steps: " + str(steps))
    return X

print([sqrt(1/6), sqrt(1/6), sqrt(1/6)])
r = 0.5
# X = [0.1, 0.9, 0.5]
X = [sqrt(1/6), sqrt(1/6), sqrt(1/6)]
mult = 0.05
while r>10**-3: # limit: 10**-6
    X = gradientDescent(X, r)
    print('r: ' + str(r))
    print("X: " + str(X))
    print()
    mult *= 2
    r /= 2
print("Final result:   " + str(X))
print("Perfect answer: " + str([sqrt(1/6), sqrt(1/6), sqrt(1/6)]))
print("Final gradient:  " + str(nd.Gradient(B)(X, r)))
print("Answer gradient: " + str(nd.Gradient(B)([[sqrt(1/6), sqrt(1/6), sqrt(1/6)]], r)))

# print(nd.Gradient(B)([sqrt(1/6), sqrt(1/6), sqrt(1/6)], 0.5))
# print(B([sqrt(1/6), sqrt(1/6), sqrt(1/6)], 0.5))
# print(B([0, 0, 0], r))
# print(B([1, 1, 1], r))
# print(B([0.1, 0.9, 0.5], r))
