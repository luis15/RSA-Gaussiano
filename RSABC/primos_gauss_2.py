from random import randrange, getrandbits, randint
from itertools import repeat
from functools import reduce
import time
import math

def get_prime(n):
    def is_prime(n, t = 7):
        def is_composite(a):
            if pow(a, d, n) == 1:
                return False
            for i in range(s):
                if pow(a, 2 ** i * d, n) == n - 1:
                    return False
            return True
        assert n > 0
        if n < 3:
            return [False, False, True][n]
        elif not n & 1:
            return False
        else:
            s, d = 0, n - 1
            while not d & 1:
                s += 1
                d >>= 1
        for _ in repeat(None, t):
            if is_composite(randrange(2, n)):
                return False
        return True
    p = getrandbits(n)
    while not is_prime(p):
        p = getrandbits(n)
    return p
def get_B(a):
    return  math.ceil(math.sqrt(p - math.pow(a, 2)))
def is_gaussian(a,b,p):
    return (pow(a,2)+pow(b,2)!=p)
n = 48
p = get_prime(n)
m = math.ceil(math.sqrt(math.pow(2,n)))
m2 = math.ceil(m/2)
t1 = time.time()
a=-1
b=0
while(is_gaussian(a,b,p)):
    a+=1
    b = get_B(a)
    if(a>m2):
        a=-1
        print("Primo ", p,"não resulta em gauss")
        p = get_prime(n)
t2 = time.time()
print("Par achado após", t2-t1,"s")
print("Para o primo :", p )
print(a , " + ", b ,"i")
time.sleep(3600)
