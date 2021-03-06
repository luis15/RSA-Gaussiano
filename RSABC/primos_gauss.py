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
n = 20
p = get_prime(n)
m = math.ceil(math.sqrt(math.pow(2,n)))
t1 = time.time()
a=randint(0, m)
b=randint(0,m)
tp1 = time.time()
while(pow(a,2)+pow(b,2)!=p):
    a=randint(0,m)
    b=randint(0,m)
    tp2 = time.time()
    if(tp2 - tp1 > 1):
        p = get_prime(n)
        tp1 = time.time()
t2 = time.time()
print("Par achado após", t2-t1,"s")
print("Para o primo :", p )
print(a , " + ", b ,"i")
time.sleep(60)
