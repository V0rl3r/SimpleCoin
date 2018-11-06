import block
import transaction
import base64
import signEncrypt as se

class BlockChain:

    difficulty = 2

    class Node:

        def __init__(self):
            self.next = None
            self.prev = None
            self.data = None

    def __init__(self):
        self.getKeys()
        print("Creating BlockChain...")
        self.createGenesis()
        self.tail = self.genesis
        self.genTransactions()
        self.length = 1
        self.mineBlock()
        self.verifyIntegrity()

    def getKeys(self):
        print("Reading Pair A...")
        keysA = []
        with open('publicA.key', 'r') as puKeyA:
            keysA.append(puKeyA.read())
        with open('privateA.key', 'r') as prKeyA:
            keysA.append(prKeyA.read())

        public = keysA[0]
        private = keysA[1]
        self.puKeyA = public
        self.prKeyA = private
        print("Reading Pair B...")
        keysB = []
        with open('publicB.key', 'r') as puKeyB:
            keysB.append(puKeyB.read())
        with open('privateB.key', 'r') as prKeyB:
            keysB.append(prKeyB.read())
        public = keysB[0]
        private = keysB[1]
        self.puKeyB = public
        self.prKeyB = private
        self.users = {}
        self.users[self.puKeyA] = "A"
        self.users[self.puKeyB] = "B"
        self.users["A"] = self.puKeyA
        self.users["B"] = self.puKeyB
        '''
        print("a", self.puKeyA)
        print("b", self.puKeyB)
        print("ap", self.prKeyA)
        print("bp", self.prKeyB)
        '''

    def genTransactions(self):
        self.transactions = []
        self.transactions.append(transaction.Transaction(40, self.puKeyA, self.puKeyB, self.prKeyA))
        '''
        self.transactions[0].unsign(self.transactions[0].origID)
        print(self.puKeyA == self.transactions[0].origID)
        print(self.puKeyB == self.transactions[0].destID)
        print("Original = 40", "New =", self.transactions[0].amtToAdd)
        print(self.puKeyB)
        print("***")
        print(self.transactions[0].destID)
        print("***")
        '''
        self.transactions.append(transaction.Transaction(15, self.puKeyB, self.puKeyA, self.prKeyB))
        self.transactions.append(transaction.Transaction(60, self.puKeyA, self.puKeyB, self.prKeyA))
        self.transactions.append(transaction.Transaction(20, self.puKeyA, self.puKeyB, self.prKeyA))
        self.transactions.append(transaction.Transaction(50, self.puKeyB, self.puKeyA, self.prKeyB))

    def createGenesis(self):
        data = transaction.Transaction(100, None, self.puKeyA, None)
        gen = block.Block(0, [data])
        gen.idx = 0
        self.genNonce(gen)
        self.genesis = self.Node()
        self.genesis.data = gen

    def addBlock(self, data):
        node = self.Node()
        node.data = data
        node.prev = self.tail
        self.tail.next = node
        self.tail = node
        self.length += 1

    def getLatest(self):
        return self.tail

    #Remove transaction if it fails, could take an array instead of one
    #Must check if transaction is valid, ie they have enough money
    #Do I decrypt the ID here?
    #Does my encryption actually handle lists at all?
    def mineBlock(self):
        while len(self.transactions) > 0:
            t = self.transactions[0]
            t.unsign(t.origID)
            accepted = False
            if int(t.amtToAdd) >= 0:
                bal = self.getBalance(t.origID)
                print
                #print("Sender:", self.users[t.origID])
                #print(bal)
                #print(t.amtToAdd)
                if bal >= int(t.amtToAdd):
                    accepted = True
                    print("Transaction " + str(self.length) + " (Amount: " + str(t.amtToAdd) + " ): " + self.users[t.origID] + "->" + self.users[t.destID] + " Accepted")
                    b = block.Block(self.length, [t])
                    b.prevHash = self.tail.data.hash
                    print("Mining Block " + str(self.length) + "... ", end = "")
                    self.genNonce(b)
                    print("(" + str(b.nonce) + ", " + str(b.hash) + ")")
                    self.addBlock(b)
                    accepted = True
            if not accepted:
                print("Transaction " + str(b.idx) + " (Amount: " + str(t.amtToAdd) + "): " + self.users[t.origID] + "->" + self.users[t.destID] + " Declined")
            del self.transactions[0]

    #Use private key to authenticate
    def getBalance(self, puKey):
        cur = self.genesis
        bal = 0
        #print("BL len:", self.length)
        while True:
            #print("Looped")
            ts = cur.data.data
            for t in ts:
                if (not t.origID is None) and t.origID == puKey:
                    #print("Is orig")
                    bal -= int(t.amtToAdd)
                elif t.destID == puKey:
                    #print("Is dest")
                    bal += int(t.amtToAdd)
            if cur.next is None:
                break
            cur = cur.next
        return bal

    def verifyIntegrity(self):
        cur = self.genesis
        valid = True
        print("Chain Verification...", end="")
        while True:
            '''
            if cur.data.idx == 0:
                if not cur.data.verifyPrint():
                    print("Hashwrong", cur.data.idx)
                    valid = False
                    break
            '''
            #elif not cur.data.verify():
            if not cur.data.verify():
                print("Hashwrong", cur.data.idx)
                valid = False
                break
            if not cur.next is None:
                if not cur.data.hash == cur.next.data.prevHash:
                    print("prevhashwrong", cur.data.idx)
                    valid = False
                    break

            if cur.next is None:
                break
            cur = cur.next
        if valid:
            print("Verified")
            print("Amount in A's Wallet: " + str(self.getBalance(self.users["A"])))
            print("Amount in B's Wallet: " + str(self.getBalance(self.users["B"])))
        else:
            print("Unverified")


    #SWITCH TO BASE 16
    def genNonce(self, b):
        hash = base64.b16encode(b.genHash()).decode()
        while not hash[0:BlockChain.difficulty] == "00":
            b.nonce += 1
            hash = base64.b16encode(b.genHash()).decode()
        b.hash = hash
        #if b.idx == 0:
        #base64.b16encode(b.genHashPrint()).decode()

#When your program runs, it should take in two private and public key pairs (as if you ahve two people)
#Output creating "block chain...", "Reading pair A...", "Reading pair B...", "Mining Block 1...", "Done Mining Block 1..."

if __name__ == "__main__":
    chain = BlockChain()
