class uniPWord():
    
    def __init__(self,pWord):
        self.pWord = pWord
    
    def val(self,pWord,pPos,cWord,cPos):
        return 1 if self.pWord == pWord else 0;

class uniPPos():
    
    def __init__(self,pPos):
        self.pPos = pPos
    
    def val(self,pWord,pPos,cWord,cPos):
        return 1 if self.pPos == pPos else 0;

class uniPWordPPos():
    
    def __init__(self,pWord,pPos):
        self.pWord = pWord
        self.pPos = pPos
    
    def val(self,pWord,pPos,cWord,cPos):
        return 1 if ((self.pWord == pWord) and (self.pPos == pPos)) else 0;
    
class uniCWord():
    
    def __init__(self,cWord):
        self.cWord = cWord
    
    def val(self,pWord,pPos,cWord,cPos):
        return 1 if self.cWord == cWord else 0;

class uniCPos():
    
    def __init__(self,cPos):
        self.cPos = cPos
    
    def val(self,pWord,pPos,cWord,cPos):
        return 1 if self.cPos == cPos else 0;

class uniCWordCPos():
    
    def __init__(self,cWord,cPos):
        self.cWord = cWord
        self.cPos = cPos
    
    def val(self,pWord,pPos,cWord,cPos):
        return 1 if ((self.cWord == cWord) and (self.cPos == cPos)) else 0;

class biPPosCWordCPos():
    
    def __init__(self,pPos,cWord,cPos):
        self.pPos = pPos
        self.cWord = cWord
        self.cPos = cPos
    
    def val(self,pWord,pPos,cWord,cPos):
        return 1 if ((self.cWord == cWord) and (self.cPos == cPos) and\
                     (self.pPos == pPos)) else 0;

class biPWordPPosCPos():
    
    def __init__(self,pWord,pPos,cPos):
        self.pWord = pWord
        self.pPos = pPos
        self.cPos = cPos
    
    def val(self,pWord,pPos,cWord,cPos):
        return 1 if ((self.pWord == pWord) and (self.pPos == pPos) and\
                     (self.cPos == cPos)) else 0;

class biPPosCPos():
    
    def __init__(self,pPos,cPos):
        self.pPos = pPos
        self.cPos = cPos
    
    def val(self,pWord,pPos,cWord,cPos):
        return 1 if ((self.pPos == pPos) and (self.cPos == cPos)) else 0;


