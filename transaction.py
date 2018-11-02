import signEncrypt as se

class Transaction:
    #FIGURE OUT WHERE THE PRIVATE KEY SHOULD COME FROM
    def __init__(self, amt, origID, destID, origPrKey, destPrKey):
        self.destID = se.enanddecrypt(0, amt, destPrKey)
        self.origID = origID
        self.isAmtSigned = True
        if(origPrKey is None):
            self.amtToAdd = amt
            self.isAmtSigned = False
        else:
            self.amtToAdd = se.enanddecrypt(0, amt, origPrKey)
        encrypted = True

    def __repr__(self):
        return str(self.destID) + str(self.origID) + str(self.amtToAdd)

    def unsign(self, destPuKey, origPuKey):
        self.destID = enanddecrypt(1, destID, destPuKey)
        if self.isAmtSigned:
            self.amtToAdd = enanddecrypt(1, amt, origPuKey)
        encrpted = False

    def verify(self):
        if amt >= 0:
            return True
        return False
#Should verify the Transaction
#Amount is greater than 0, sender has enough money
#Only signed when its not in a Block (recvID, amt)
