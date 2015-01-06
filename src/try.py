import model
import networkx as nx

m = model.mstModel()

# s = m.readFile(1)
# 
# for s_i in s:
#     print s_i
#     print s_i.poss
#     print s_i.goldHeads

G = nx.DiGraph()
# Root John Saw Mary
# 0    1    2   3
G.add_nodes_from([0,1,2,3])
edgesContainer = [{'u':0,'v':1,'weight':9},
                  {'u':0,'v':2,'weight':10},
                  {'u':0,'v':3,'weight':9},
                  {'u':1,'v':2,'weight':20},
                  {'u':1,'v':3,'weight':3},
                  {'u':2,'v':1,'weight':30},
                  {'u':2,'v':3,'weight':30},
                  {'u':3,'v':1,'weight':11},
                  {'u':3,'v':2,'weight':0}]
for e in edgesContainer:
    G.add_edge(e['u'], e['v'], {'weight':e['weight']})

optG = m.chuLiuEdmonds(G) 
print (optG.edges())
for edge in optG.edges():
    print edge,optG.get_edge_data(edge[0],edge[1])['weight']