import block
import transaction
import base64

class BlockChain:

    difficulty = 2

    def __init__(self):
        self.getKeys()
        self.createGenesis()
        self.tail = self.genesis
        seld.genTransactions()

    def getKeys(self):
        keysA = []
        with open('publicA.key', 'r') as puKeyA:
            keys.append(puKeyA.read())
        with open('privateA.key', 'r') as prKeyA:
            keys.append(prKeyA.read())
        public = keys[0].split(", ")
        private = keys[1].split(", ")
        self.puKeyA = public
        self.prKeyA = private
        keysB = []
        with open('publicB.key', 'r') as puKeyB:
            keys.append(puKeyB.read())
        with open('privateB.key', 'r') as prKeyB:
            keys.append(prKeyB.read())
        public = keysB[0].split(", ")
        private = keysB[1].split(", ")
        self.puKeyB = public
        self.prKeyB = private

    def genTransactions(self):
        self.transactions = []
        self.transactions.append(transaction.Transaction(40, self.puKeyA, self.puKeyB, self.prKeyA, self.prKeyB))
        self.transactions.append(transaction.Transaction(15, self.puKeyB, self.puKeyA, self.prKeyB, self.prKeyA))
        self.transactions.append(transaction.Transaction(60, self.puKeyA, self.puKeyB, self.prKeyA, self.prKeyB))
        self.transactions.append(transaction.Transaction(20, self.puKeyA, self.puKeyB, self.prKeyA, self.prKeyB))
        self.transactions.append(transaction.Transaction(50, self.puKeyB, self.puKeyA, self.prKeyB, self.prKeyA))

    def createGenesis(self):
        data = transaction.Transaction(100, None, self.puKeyA, None, self.prKeyA)
        gen = block.Block(0, data)
        self.genesis = Node()
        self.genesis.data = gen

    def addBlock(self, data):
        node = Node()
        node.data = data
        node.prev = self.tail
        self.tail = node

    def getLatest(self):
        return self.tail

    #Remove transaction if it fails, could take an array instead of one
    #Must check if transaction is valid, ie they have enough money
    def mineBlock(self, transaction):
        pass

    def verifyIntegrity(self):
        pass

    #SWITCH TO BASE 16
    def genNonce(self, block):
        num = 0
        block.nonce = num
        hash = base64.b64encode(block.genHash()).decode()
        while not hash[0:BlockChain.difficulty] == "00":
            block.nonce += 1
            hash = base64.b64encode(block.genHash()).decode()
        block.hash = hash

    class Node:

        def __init__(self):
            self.next = None
            self.prev = None
            self.data = None

#When your program runs, it should take in two private and public key pairs (as if you ahve two people)
#Output creating "block chain...", "Reading pair A...", "Reading pair B...", "Mining Block 1...", "Done Mining Block 1..."

if __name__ == "__main__":
    chain = BlockChain()
