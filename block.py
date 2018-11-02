import hashlib
import time

class Block:

    def __init__(self, idx=None, data=None, prevHash=None, hash=None):
        self.idx = idx
        self.tStamp = time.time()
        if not data is None:
            self.data = data
        else:
            self.data = []
        self.prevHash = prevHash
        self.nonce = 0
        self.hash = hash

    def genHash(self):
        idxStr = str(self.idx)
        tStampStr = str(self.tStamp)
        dataStr = str(self.data)
        prevHashStr = str(self.prevHash)
        nonceStr = str(self.nonce)
        self.hash = hashlib.sha256()
        self.hash.update(idxStr.encode())
        self.hash.update(tStampStr.encode())
        self.hash.update(dataStr.encode())
        self.hash.update(prevHashStr.encode())
        self.hash.update(nonceStr.encode())
        self.hash = self.hash.digest()
        return self.hash

#MUST VERIFY
