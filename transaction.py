import signEncrypt as se

class Transaction:
    #***
    #WHERE DO I CHECK VALIDITY OF AMOUNT
    #What is used to sign - private key of sender?
    #***
    def __init__(self, amt, origID, destID, origPrKey, destPrKey):
        self.signed = True
        if origID is None:
            self.signed = False
            self.destID = destID
            self.amtToAdd = amt
        else:
            self.destID = se.enanddecrypt(0, amt, origPrKey)
            self.amtToAdd = se.enanddecrypt(0, amt, origPrKey)
        self.origID = origID

    def __repr__(self):
        return str(self.destID) + str(self.origID) + str(self.amtToAdd)

    def unsign(self, origPuKey):
        if self.signed:
            self.destID = se.enanddecrypt(1, self.destID, origPuKey)
            self.amtToAdd = se.enanddecrypt(1, self.amtToAdd, origPuKey)

    def verify(self):
        if amt >= 0:
            return True
        return False
#Should verify the Transaction
#Amount is greater than 0, sender has enough money
#Only signed when its not in a Block (recvID, amt)
