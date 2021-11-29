import pandas as pd
import networkx as nx
import tldextract
import validators
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('hyperlinks.csv', index_col=[0])
color_map = []
result = pd.DataFrame()

def calcSingleColor(color, arr):
    count = 0
    for elem in arr:
        if (elem == color):
            count += 1
    
    return (count / len(arr))

def calcDoubleColor(color1, color2, arr):
    count = 0 
    for elem in arr:
        if ((elem == color1) or (elem == color2)):
            count += 1
    
    return (count / len(arr))

def calcSize(color, arr):
    count = 0 
    for elem in arr:
        if (elem == color):
            count += 1
    
    return count

def centrality(G):
    nodes = nx.out_degree_centrality(G)
    mean = sum(nodes.values()) / len(nodes)
    return mean

def checkSubDomain(source, node):
    t1 = tldextract.extract(source)
    t2 = tldextract.extract(node)

    srcSub = t1.subdomain
    nodeSub = t2.subdomain
    srcDom = t1.domain
    nodeDom = t2.domain
    
    if (srcDom == nodeDom) and (srcSub != nodeSub):
        return True
    
    return False

def main(data, color_map, result):
    for url in (data.index.unique().to_list()):
        df = data.loc[url].astype(str)
        G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())

        source = url
        if ((source.startswith("http") == False)):
            source = "https://" + source
        
        for node in G:
            if (source == node):
                color_map.append('red')
            elif (source in node):
                color_map.append('orange')
            elif (checkSubDomain(source, node)):
                color_map.append('yellow')
            elif (validators.url(node) == False):
                color_map.append('green')
            else:
                color_map.append('blue')
        
        nx.draw(G, pos=nx.spring_layout(G), node_color=color_map, node_size=50, with_labels=False)
        
        orange = calcSingleColor('orange', color_map)
        yellow = calcSingleColor('yellow', color_map)
        green = calcSingleColor('green', color_map)
        blue = calcSingleColor('blue', color_map)
        orange_yellow = calcDoubleColor('orange', 'yellow', color_map)
        green_blue = calcDoubleColor('green', 'blue', color_map)
        greenSize = calcSize('green', color_map)
        blueSize = calcSize('blue', color_map)
        srcOut = G.out_degree(source)
        outCentrality = centrality(G)
        density = nx.density(G)
        
        df = pd.DataFrame(np.array([orange, yellow, green, blue, orange_yellow, green_blue, greenSize, blueSize, srcOut, outCentrality, density])).transpose()
        result = result.append(df)
        print(result)
        del color_map[:]
        plt.show()
        exit()
    result.to_csv('features.csv', index=False)

main(data, color_map, result)