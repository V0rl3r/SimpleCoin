import random
import base64
import math
import time

#provide a random prime at maximum nBits length
def getPrime(nBits):

    min = 2**(nBits-2)
    max = 2**nBits

    num = random.randrange(min, max, 1)

    #Ensures the number is not 2 or even
    if (not num & 1) and (num != 2):
        num = num + 1

    #Fermat's primality test
    def isPrime(num):

        if num == 2:
            return True

        #Bitwise anding to check evenness
        if not num & 1:
            return False

        return pow(2, num-1, num) == 1

    while not isPrime(num):
        num = num + 2

        while num.bit_length() > nBits:
            num = num // 2

            #Ensures the number is not 2 or even
            if (not num & 1) and (num != 2):
                num = num + 1

    return num

#Iterative extended euclidean algorithm. Takes an e value and the totient of n
#e = an int, totN = an int
def iterativeExtEuclids(e, totN):
    #Represents a form of a = b(c) + d
    #a begins as totient of n, c as e
    b = totN//e
    d = totN-b*e
    #Storage represents a stack of lists of values so that the program can work backwards once it reaches the base case
    storage = [[totN, b, e, d]]
    d2 = d
    #Working down until the remainder is one, signalling its time to head back up
    while not (d2 == 1):
        a, b, c, d = storage[len(storage)-1]
        a2 = c
        c2 = d
        b2 = a2//c2
        d2 = a2 - b2*c2
        storage.append([a2, b2, c2, d2])
    #Modify the final value, changing it to as it is now 1 = a - b(c)
    storage[len(storage)-1] = [storage[len(storage)-1][3], (-1)*storage[len(storage)-1][1], storage[len(storage)-1][2], storage[len(storage)-1][0]]
    #Work your way back up through the equations
    while len(storage) > 1:
        a3, b3, c3, d3 = storage[len(storage)-1]
        storage.pop()
        a2, b2, c2, d2 = storage[len(storage)-1]
        storage.pop()
        a4 = a3
        b4 = b3*b2*(-1) #Since b2 flips
        b4 += d3//c2
        d4 = b3*a2
        c4 = c2
        storage.append([a4, b4, c4, d4])
    #Return b
    return storage[0][1]

#Number of bits for p and q
numBits = 2048
p = getPrime(numBits)
q = getPrime(numBits)
n = p*q
totN = (p-1)*(q-1)
#Number of bits for e
eBits = 3000
e = getPrime(numBits)
while totN % e == 0:
    e = getPrime(numBits)
d = iterativeExtEuclids(e, totN)
if d < 0:
    d = d % totN
#Encode the 3 values into base 64
enN = base64.b64encode(n.to_bytes(math.ceil(n.bit_length()/8), "little"))
enE = base64.b64encode(e.to_bytes(math.ceil(e.bit_length()/8), "little"))
enD = base64.b64encode(d.to_bytes(math.ceil(d.bit_length()/8), "little"))

#Removes the byte notation, leaving only base 64
enN = enN.decode()
enE = enE.decode()
enD = enD.decode()

#Constructs the strings to be stored
pu = str(enE) + ", " + str(enN)
pr = str(enD) + ", " + str(enN)

with open('public.key', 'w') as puKey:
    puKey.write(pu)

with open('private.key', 'w') as prKey:
    prKey.write(pr)
