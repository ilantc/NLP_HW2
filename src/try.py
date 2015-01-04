import model

m = model.mstModel()

s = m.readFile(1)

for s_i in s:
    print s_i
    print s_i.poss
    print s_i.goldHeads