#from matplotlib import scale
#from numpy import size
import networkx 
from scipy.stats import truncnorm 
G=networkx.Graph()

#Fix this
def GetValAtoB(i):
    ll = []
    for neighbor in G.neighbors(i) :
        ll.append(G.nodes(data =True)[neighbor].get('inf'))

    A = ll.count(True)
    B = ll.count(False)

    return A/(A+B)

def get_truncated_normal(mean:float , sd=0.15, low=0.0, upp=1.0):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd).rvs();


file1 = open('facebook_combined.txt', 'r')
Lines = file1.readlines()

for line in Lines:
    Edge = line.split()
    if(Edge[0] not in G.nodes):
        G.add_node(Edge[0], inf = False)
        
    if(Edge[1] not in G.nodes):
        G.add_node(Edge[1], inf = False)
        
    G.add_edge(Edge[0], Edge[1])
    

nums1= ['1912', '2347', '2266', '2233', '2543', '2206', '1985', '2142', '2464', '2218'] #0.5% Eigenvector

nums2= [ '3437', '107', '1684', '0', '1912', '348', '686', '3980', '414', '483'] #5% Pagerank

nums3= [ '107', '1684', '3437', '1912', '1085', '0', '698', '567', '58', '428'] # 4% Betweenness

nums4= ['107','58', '428', '567', '1684', '171', '348', '483', '483', '414'] # 2.4%  Closeness

nums5 = ['1912', '107', '2347', '2266', '2206', '2233', '2543', '2464', '2218', '2142'] # 1.3% TriangleCount

nums6 = ['107', '1684', '1912', '3437', '1912', '0', '2543', '2347', '1888', '1800'] # 4% Degree

numALL = ['107', '0', '1912', '3437', '1684', '2347', '2266', '428', '348', '567', '2543']# 4% Combined

nums = nums2
for n in nums:
    G.nodes[n]['inf']=True
AVal= 5
BVal= 5

InfCount = len(nums);
for num in nums:
    List = []
    List.append(num)

    while len(List) > 0:
        ToInfect={}
        for neighbor in G.neighbors(List[0]) :
            uk = G.nodes(data =True)[neighbor]
            ToInfect.update({neighbor: uk})

        for infect in ToInfect.items():
            if infect[1]['inf']!=True:
                if GetValAtoB(infect[0]) >= get_truncated_normal(BVal/(BVal+AVal)):
                    infect[1]['inf'] = True
                    List.append(infect[0])
                    InfCount=InfCount+1;   
        List.pop(0)


print(InfCount/G.number_of_nodes());

#Results: pagerank for facebook