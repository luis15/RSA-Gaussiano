#!/usr/bin/python3
#
# Author: Luis Antonio Coêlho (l156435@dac.unicamp.br)
#
# Description: RSA implementation in Python for final course project
#
# Date: 2016-07-27
#
#===========================================================
from random import randrange, getrandbits
from itertools import repeat
from functools import reduce
import time

def get_prime(n):
    """Retorna um primo randômico"""
    def is_prime(n, t = 7):
        """Teste de primalidade Miller-Rabin"""
        def is_composite(a):
            """Checa se n é composto"""
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

def inv(p, q):
    """Inverso multiplicativo"""
    def xgcd(x, y):
        """Algoritmo euclidiano extendido"""
        s1, s0 = 0, 1
        t1, t0 = 1, 0
        while y:
            q = x // y
            x, y = y, x % y
            s1, s0 = s0 - q * s1, s1
            t1, t0 = t0 - q * t1, t1
        return x, s0, t0

    s, t = xgcd(p, q)[0:2]
    assert s == 1
    if t < 0:
        t += q
    return t

def get_keys(p, q):
    """Gera chaves públicas e privadas"""
    phi, mod = (p - 1) * (q - 1), p * q
    if mod < 65537:
        return (3, inv(3, phi), mod)
    else:
        return (65537, inv(65537, phi), mod)

def str_2_int(text):
    """Transforma texto em números inteiros"""
    return reduce(lambda x, y : (x << 8) + y, map(ord, text))

def int_2_str(number, size):
    """Transforma inteiro em string"""
    text = "".join([chr((number >> j) & 0xff)
                    for j in reversed(range(0, size << 3, 8))])
    return text.lstrip("\x00")

def int_2_list(number, size):
    """Converte inteiro em lista de inteiros"""
    return [(number >> j) & 0xff
            for j in reversed(range(0, size << 3, 8))]

def list_2_int(listInt):
    """Converte lisa em inteiro"""
    return reduce(lambda x, y : (x << 8) + y, listInt)

def mod_size(mod):
    """Retorna o tamanho em bytes do modulo"""
    mod_size = len("{:02x}".format(mod)) // 2
    return mod_size

def encrypt(ptext, pk, mod):
    """Encripta com chave pública"""
    size = mod_size(mod)
    output = []
    while ptext:
        nbytes = min(len(ptext), size - 1)
        aux1 = str_2_int(ptext[:nbytes])
        assert aux1 < mod
        aux2 = pow(aux1, pk, mod)
        output += int_2_list(aux2, size + 2)
        ptext = ptext[size:]
    return output

def decrypt(ctext, sk, p, q):
    """Sesencripta com chave private usando o teorema chine da lembrança"""
    mod = p * q
    size = mod_size(mod)
    output = ""
    while ctext:
        aux3 = list_2_int(ctext[:size + 2])
        assert aux3 < mod
        m1 = pow(aux3, sk % (p - 1), p)
        m2 = pow(aux3, sk % (q - 1), q)
        h = (inv(q, p) * (m1 - m2)) % p
        aux4 = m2 + h * q
        output += int_2_str(aux4, size)
        ctext = ctext[size + 2:]
    return output

if __name__ == "__main__":

    from math import log10
    from time import time

    def print_cipher_msg(cipher_msg):
        """Exibe a mensagem cifrada em hexadecimal"""
        for index, elem in enumerate(cipher_msg):
            if index % 32 == 0:
                print()
            print("{:02x}".format(elem), end = "")
        print()

    def print_larg_int(long_int):
        """Exibe primos longos formatados"""
        string = "{:02x}".format(long_int)
        for j in range(len(string)):
            if j % 64 == 0:
                print()
            print(string[j], end = "")
        print()

    def run(msg):
        """Executa o núcleo do código"""
        n=512
        t1 = time.time()
        p = get_prime(n)
        t2 = time.time()
        print("Tempo gasto para gerar um primo de {:0d} bits: ".format(n), end = "")
        print("{:0.3f} s".format(round(t2 - t1, 3)))
        t1 = time.time()
        q = get_prime(n)
        t2 = time.time()
        print("Tempo gasto para gerar um primo de {:0d} bits ".format(n), end = "")
        print("{:0.3f} s".format(round(t2 - t1, 3)))
        print("Tamanho da chave: {:0d} bits".format(round(log10(p * q) / log10(2))))
        print("Primeiro primo:", end = "")
        print_larg_int(p)
        print("Segundo primo:", end = "")
        print_larg_int(q)
        print("Texto original:", msg)
        t1 = time.time()
        pk, sk, mod = get_keys(p, q)
        cipher_msg = encrypt(msg, pk, mod)
        t2 = time.time()
        print("Tempo gasto para criptgrafar a mensagem")
        print("{:0.3f} s".format(round(t2 - t1, 3)))

        print("Texto criptografado:", end = "")
        print_cipher_msg(cipher_msg)
        t1 = time.time()
        ptext = decrypt(cipher_msg, sk, p, q)
        t2 = time.time()
        print("Tempo gasto para recuperar a mensagem")
        print("{:0.3f} s".format(round(t2 - t1, 3)))
        print("Texto recuperado:", ptext, "\n")

    # Execução teste
    msg = input("Entre com a mensagem para ser criptografada:")
    t5 = time.time()
    run(msg)
    t6 = time.time()
    print("Tempo gasto para execução da criptografia")
    print("{:0.3f} s".format(round(t6 - t5, 3)))
    time.sleep(60)
