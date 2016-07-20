'''
Luis Antonio Coêlho - 156435 - Universidade Estadual de Campinas - 2016
'''

import pickle
import random
import sys


'''
Algoritmo euclidiano para determinar o MDC
'''
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

'''
Algoritmo para determinar o inverso multiplicativo de dois números 
'''
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi
    else:
        return phi

'''
Teste de 'primidade'
'''
def is_prime(num):
    num = int(num)
    if num == 2:
        return True
    if (num < 2 or num % 2 == 0):
        return False
    for n in range(3,int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Ambos devem ser primos')
    elif p == q:
        raise ValueError('p e q não podem ser iguais')
    n = p * q
    #Phi é totiente de n
    phi = (p-1) * (q-1)

    #Escolhe o inteiro e verifica se ele é coprimo
    e = random.randrange(1, phi)

    #Usa algoritmo para verificar se phi(n) é coprimo
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    #Define a chave
    d = multiplicative_inverse(e, phi)
    
    #Chaves públicas são (e, n) e privadas são (d, n)
    return (e, n), (d, n)

def string2numList(strn):
    """Converts a string to a list of integers based on ASCII values"""
    return [ ord(chars) for chars in pickle.dumps(strn) ]


def numList2string(l):
    """Converts a list of integers to a string based on ASCII values"""
    return pickle.loads(''.join(map(chr, l)))


def numList2blocks(l, n):
    """Take a list of integers(each between 0 and 127), and combines them
    into block size n using base 256. If len(L) % n != 0, use some random
    junk to fill L to make it."""
    # Note that ASCII printable characters range is 0x20 - 0x7E
    returnList = []
    toProcess = copy.copy(l)
    if len(toProcess) % n != 0:
        for i in range(0, n - len(toProcess) % n):
            toProcess.append(random.randint(32, 126))
    for i in range(0, len(toProcess), n):
        block = 0
        for j in range(0, n):
            block += toProcess[i + j] << (8 * (n - j - 1))
        returnList.append(block)
    return returnList


def blocks2numList(blocks, n):
    """inverse function of numList2blocks."""
    toProcess = copy.copy(blocks)
    returnList = []
    for numBlock in toProcess:
        inner = []
        for i in range(0, n):
            inner.append(numBlock % 256)
            numBlock >>= 8
        inner.reverse()
        returnList.extend(inner)
    return returnList

def encrypt(message, modN, e, blockSize):
    """given a string message, public keys and blockSize, encrypt using
    RSA algorithms."""
    numList = string2numList(message)
    numBlocks = numList2blocks(numList, blockSize)
    return [modExp(blocks, e, modN) for blocks in numBlocks]


def decrypt(secret, modN, d, blockSize):
    """reverse function of encrypt"""
    numBlocks = [modExp(blocks, d, modN) for blocks in secret]
    numList = blocks2numList(numBlocks, blockSize)
    return numList2string(numList)
    

if __name__ == '__main__':
    print ("RSA Encriptador/Deesncriptador")
    p = int(input("Insira um primo (17, 19, 23, etc): "))
    q = int(input("Insira outro primo (Not one you entered above): "))
    print ("Gerando chaves...")
    public, private = generate_keypair(p, q)
    print ("A chave pública é", public ," e a privada é ", private)
    message = input("Entre com uma mensagem para encriptá-la com a chave privada: ")
    encrypted_msg = encrypt(message, public[1], public[0],15)
    print ("Sua mensagem encriptada é: ")
    print (''.join(map(lambda x: str(x), encrypted_msg)))
    print ("Desencriptando a mensagem com a chave pública ", public ," . . .")
    print ("A mensagem é:")
    decrypted_msg = decrypt(encrypted_msg, private[1], private[0],15)
    print (''.join(map(lambda x: str(x), decrypted_msg)))
