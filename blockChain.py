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
        self.createGenesis()
        self.tail = self.genesis
        self.genTransactions()
        self.length = 1
        self.mineBlock()

    def getKeys(self):
        keysA = []
        with open('publicA.key', 'r') as puKeyA:
            keysA.append(puKeyA.read())
        with open('privateA.key', 'r') as prKeyA:
            keysA.append(prKeyA.read())

        public = keysA[0]
        private = keysA[1]
        self.puKeyA = public
        self.prKeyA = private
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
        print("a", self.puKeyA)
        print("b", self.puKeyB)
        print("ap", self.prKeyA)
        print("bp", self.prKeyB)

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
            #DO NOT USE IDENTIFY. ATTEMPT TO DECODE t.blank, and if it matches a public id you're good
            t.unsign(t.origID)
            #Need the private key of sender!
            bal = self.getBalance(t.origID)
            print
            print("Sender:", self.users[t.origID])
            print(bal)
            print(t.amtToAdd)
            if bal >= int(t.amtToAdd):
                b = block.Block(self.length, [t])
                self.genNonce(b)
                self.addBlock(b)
                print("Added Block")
            del self.transactions[0]

    #Use private key to authenticate
    def getBalance(self, puKey):
        cur = self.genesis
        bal = 0
        print("BL len:", self.length)
        while True:
            print("Looped")
            ts = cur.data.data
            for t in ts:
                if (not t.origID is None) and t.origID == puKey:
                    print("Is orig")
                    bal -= int(t.amtToAdd)
                elif t.destID == puKey:
                    print("Is dest")
                    bal += int(t.amtToAdd)
            if cur.next is None:
                break
            cur = cur.next
        return bal

    def verifyIntegrity(self):
        pass

    #SWITCH TO BASE 16
    def genNonce(self, b):
        hash = base64.b16encode(b.genHash()).decode()
        while not hash[0:BlockChain.difficulty] == "00":
            b.nonce += 1
            hash = base64.b16encode(b.genHash()).decode()
        b.hash = hash

#When your program runs, it should take in two private and public key pairs (as if you ahve two people)
#Output creating "block chain...", "Reading pair A...", "Reading pair B...", "Mining Block 1...", "Done Mining Block 1..."

if __name__ == "__main__":
    chain = BlockChain()
