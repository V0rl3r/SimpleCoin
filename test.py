import base64
import math
import binascii
import random

def enanddecrypt(mode, input, key):

    #Gets the individual b64 keys and turns encodes them as bytes
    key = key.split(', ')
    enK = key[0].encode()
    enN = key[1].encode()

    #Turns the b64 keys into ints
    k = int.from_bytes(base64.b64decode(enK), "little")
    n = int.from_bytes(base64.b64decode(enN), "little")
    m = str(input)

    if mode == 0:
        #Encodes the message into byte form
        enM = m.encode()
        #Turns the message into an int
        intM = int.from_bytes(enM, "little")
        #Creates the cipher text
        cipherT = pow(intM, k, n)
        #Turns the cipher text into base 64
        cipherT64 = base64.b64encode(cipherT.to_bytes(math.ceil(cipherT.bit_length()/8), "little"))
        #Removes the byte notation from the base 64 cipher text
        toBeWritten = cipherT64.decode()
    elif mode == 1:
        try:
            #Encodes the encrypted message into byte form
            enM = m.encode()
            #Turns the encrypted message into the int form cipher text
            cipherT = int.from_bytes(base64.b64decode(enM), "little")
            #Gets the int form of the plain text
            intM = pow(cipherT, k, n)
            #Gets the byte form of the plain text
            enM = intM.to_bytes(math.ceil(intM.bit_length()/8), "little")
            #Gets the string form from the byte form
            toBeWritten = enM.decode()
        except binascii.Error:
            print("Incorrect Encryption")
            toBeWritten = None
    return toBeWritten


keysA = []
with open('publicA.key', 'r') as puKeyA:
    keysA.append(puKeyA.read())
with open('privateA.key', 'r') as prKeyA:
    keysA.append(prKeyA.read())

public = keysA[0]
private = keysA[1]
puKeyA = public
prKeyA = private
keysB = []
with open('publicB.key', 'r') as puKeyB:
    keysB.append(puKeyB.read())
with open('privateB.key', 'r') as prKeyB:
    keysB.append(prKeyB.read())
public = keysB[0]
private = keysB[1]
puKeyB = public
prKeyB = private
users = {}
users[puKeyA] = "A"
users[puKeyB] = "B"

orig = puKeyB
print(orig)
encrypted = enanddecrypt(0, puKeyB, prKeyA)
print(encrypted)
decrypted = enanddecrypt(1, encrypted, puKeyA)
