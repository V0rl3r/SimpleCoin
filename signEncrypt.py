import base64
import math
import binascii
import random

#Key is in base64
#0 encrypt, 1 decrypt
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

#ONLY NEEDS TO USE AN INT, CUT DOWN ON STEPS
#Takes two keys, checks if they are a pair
def identify(a, b):

    #Gets the individual b64 keys and turns encodes them as bytes
    a = a.split(', ')
    enA = a[0].encode()
    enAN = a[1].encode()
    b = b.split(', ')
    enB = b[0].encode()
    enBN = b[1].encode()

    #Turns the b64 keys into ints
    a = int.from_bytes(base64.b64decode(enA), "little")
    an = int.from_bytes(base64.b64decode(enAN), "little")
    b = int.from_bytes(base64.b64decode(enB), "little")
    bn = int.from_bytes(base64.b64decode(enBN), "little")

    intM = random.randrange(1000, 10000, 1)
    cipherT = pow(intM, a, an)
    intM2 = pow(cipherT, b, bn)

    if intM == intM2:
        return True
    else:
        return False

#ID is the base64 string. keys are lists of base64 strings
def findUser(id, puKeys, prKeys):
    try:
        #Encodes the encrypted message into byte form
        enM = id.encode()
        #Turns the encrypted message into the int form cipher text
        cipherT = int.from_bytes(base64.b64decode(enM), "little")
        #Gets the int form of the plain text
        for key in puKeys:
            key = key.split(', ')
            a = key[0].encode()
            b = key[1].encode()
            a = int.from_bytes(base64.b64decode(enA), "little")
            b = int.from_bytes(base64.b64decode(enB), "little")
            intM = pow(cipherT, a, b)
            #Gets the byte form of the plain text
            enM = intM.to_bytes(math.ceil(intM.bit_length()/8), "little")
            #Gets the string form from the byte form
            enM64 = base64.b64encode(enM)
            for key2 in puKeys:
                if key2 == enM64:
                    return key2
        return None
    except binascii.Error:
        print("Incorrect Encryption")
        toBeWritten = None
        return None

'''
#Input is 0, 1, 2, 3, signalling: sign with public, encrypt with private, decrypt with private, decrypt with public
def enanddecrypt(mode, puKeyFile, prKeyFile, input):

    keys = []

    with open(puKeyFile, 'r') as puKey:
        keys.append(puKey.read())

    with open(prKeyFile, 'r') as prKey:
        keys.append(prKey.read())

    #Gets the individual b64 keys and turns encodes them as bytes
    public = keys[0].split(", ")
    enE = public[0].encode()
    enN = public[1].encode()
    private = keys[1].split(", ")
    enD = private[0].encode()

    enE =

    #Turns the b64 keys into ints
    e = int.from_bytes(base64.b64decode(enE), "little")
    d = int.from_bytes(base64.b64decode(enD), "little")
    n = int.from_bytes(base64.b64decode(enN), "little")

    if mode == 0 or mode == 1:
        #Encodes the message into byte form
        enM = m.encode()
        #Turns the message into an int
        intM = int.from_bytes(enM, "little")
        dMode = ""
        #Creates the cipher text
        if mode == 0:
            cipherT = pow(intM, d, n)
        else:
            cipherT = pow(intM, e, n)
        #Turns the cipher text into base 64
        cipherT64 = base64.b64encode(cipherT.to_bytes(math.ceil(cipherT.bit_length()/8), "little"))
        #Removes the byte notation from the base 64 cipher text
        toBeWritten = cipherT64.decode()
    elif mode == 2 or mode == 3:
        try:
            #Encodes the encrypted message into byte form
            enM = m.encode()
            #Turns the encrypted message into the int form cipher text
            cipherT = int.from_bytes(base64.b64decode(enM), "little")
            #Gets the int form of the plain text
            if mode == 2:
                intM = pow(cipherT, e, n)
            else:
                intM = pow(cipherT, d, n)
            #Gets the byte form of the plain text
            enM = intM.to_bytes(math.ceil(intM.bit_length()/8), "little")
            #Gets the string form from the byte form
            toBeWritten = enM.decode()
        except binascii.Error:
            print("Incorrect Encryption")
            toBeWritten = None
    return toBeWritten
'''
