class sentence:
    
    def __init__(self,words,poss,goldHeads):
        self.words = words
        self.poss = poss
        self.goldHeads = goldHeads
        
    def __repr__(self):
        return " ".join(self.words)