#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tqdm import tnrange, tqdm_notebook
import collections
import math
import numpy as np
from collections import defaultdict
import threading
import networkx as nx
import pandas as pd
import operator


def graph_dict():
    '''
    We first choose to use a dictionary for collect all the node with out_edges.
    Because each row in the txt was "node\titsadiacentnode" we needed to parse all rows 
    in order to split the to, adding the first node as key and the second has its "end of one of its edge" node.
    Of course each node can have more than one edge, thus we associated to each node-key a list. 
    '''
    graph = defaultdict(list)
    list1= list()
    with open("wiki-topcats-reduced.txt") as f:
        for line in f:
            list1 = line.strip().split("\t")
            if list1[0] in graph.keys():
                graph[list1[0]].append(list1[1])
            else:
                graph[list1[0]]=[list1[1]]
    return(graph)

def create_graph_and_dict():
    '''
    For the computation of the next method distance_graph, we needed the overall structure of the graph.
    Thus, instead of use the dictionary as before, we employed the networkx library.
    We setted for each node of the graph the attribute for the categories that each node belongs to; because at the same time we created the dictionary with all the name of categories as key, and the related list with all nodes associated to that category.
    Parsing through this last dictionary, we have been able to associate the right list of categories to each node. 
    '''
    G=nx.DiGraph() 
    with open("wiki-topcats-reduced.txt") as f:
        for line in f:
            list1 = line.strip().split("\t")
            G.add_node(list1[0])
            G.add_edge(list1[0],list1[1])
    ### adding attribute 'Category' to each node of the graph

    for i in G:
        G.node[i]['Category']=[]

    category_dict = defaultdict()

    with open("wiki-topcats-categories.txt", "r") as f:
        lst2=G.nodes()
        for line in f:
            cat_list = line.strip().split(";")
            category = cat_list[0][9:]
            lst = cat_list[1].strip().split(" ")
            if len(lst) > 3500:   

                lst1=[el for el in lst if el in lst2]
                category_dict[category] = lst1

    #Assign attributes to each node
    for cat in category_dict:
        lst=category_dict[cat]
        for e in lst:
            if e in G:
                G.node[e]['Category'].append(cat)
    return G, category_dict



# In our Algorithm for each root which is in the input category we go through graph, and each time we check each node attributes
#if it is belonging to the categories that we are looking for and at the same time it doesn't belong to input category. 
#Therefore , each time the function is called , the nodes in the path of the roots are checked for 4 category

def distance_graph(G, C0, C1,category_dict):
    '''
    This method computes all procedures in order to return the median (distance) for each category given as input in the 3rd parameter.
    Given the graph and the category_dict created above, C0 is always the same for each call, because we want the distance for this category with the others,  C1 is a list that has 4 categories.
    For each node from the category input C0, we needed to compute all the possible paths until the other nodes of the category. 
    We took only a slice of them (2000) for not getting stuck because nodes where a lot.
    
    Starting from this idea,
    We decided to have 4 categories instead of just one is because the graph is huge and for not iterating each time, checking just for one category, it checks for four.
     
    We wrote something similar to the breadth first search algorithm, with the difference that the shortest path list related to a category is updated if the algorithm finds that that node belongs to one of the category we considered in the list C1.
    
    In this way, we don't have a destination (or a loop for each node that belongs to the category that we want to reach).
    We agreed that to save and keep four long lists (shortest_paths) was less heavy than to parse through all the graph, looking for a sepcific node.  
    
    Every time we go inside one node, without differences if it was from C0 or from one of the categories in C1,
    we added it to SEEN variable, to avoid any possible loop or, of course, to not check again a node already discovered.
    
    Once got the lists with all possible paths, we added the infinites values to the lists.
    Because we start from c0 with 2000 nodes, but we go until all the other nodes from the categories of C1, there are some nodes that are not reachable. 
    And we added "manually" the infinitives: given the length of each shortest path we can get how many nodes have not been reached subtracting the combination of all passible paths (length  of the i-th category of C1 multiplied by the length of the c0).
    This value is how many nodes of the i-th category of C1 have not been reached. And we added them to the shortest path lists.
    And we returned the median related to each category of C1.    
    '''
    c0 = category_dict[C0][0:2000]

    shortest_paths_1 = list()
    shortest_paths_2 = list()
    shortest_paths_3 = list()
    shortest_paths_4 = list()

    for i in tnrange(len(c0)):
        root=c0[i]
        step = 0
        seen=set([root])
        queue=collections.deque([(root,step)])
        while queue:
            vertex=queue.popleft()
            
            
            if C1[0] in G.node[vertex[0]]['Category'] and C0 not in G.node[vertex[0]]['Category']:
                    shortest_paths_1.append(step)
                 
            elif C1[1] in G.node[vertex[0]]['Category'] and C0 not in G.node[vertex[0]]['Category']:
                    shortest_paths_2.append(step)
                   
            
            elif C1[2] in G.node[vertex[0]]['Category'] and C0 not in G.node[vertex[0]]['Category']:
                    shortest_paths_3.append(step)
                  
            elif C1[3] in G.node[vertex[0]]['Category'] and C0 not in G.node[vertex[0]]['Category']:
                    shortest_paths_4.append(step)
                    
            
            neighbors1 = list(G[vertex[0]])
            
            step=vertex[1]+1
            if neighbors1 == []:
                continue
              
            
            for i in neighbors1:
                if i not in seen:
                    queue.append((i,step))                    
                    seen.add(i)
                    
    for i in range(len(C1)):
        lc = len(category_dict[C1[i]])
        
        if len(eval('shortest_paths_%d'% (i+1))) != lc:
            
            diff = abs(len(eval('shortest_paths_%d'% (i+1))) - lc*len(c0))
            aux_l = [math.inf for i in range(diff)]
            eval("shortest_paths_{}".format(i+1)).extend(aux_l)
    
    return [(C1[0], np.median(np.array(sorted(shortest_paths_1)))), (C1[1], np.median(np.array(sorted(shortest_paths_2)))),
           (C1[2], np.median(np.array(sorted(shortest_paths_3)))), (C1[3], np.median(np.array(sorted(shortest_paths_4))))]



#@autojit
def distance_graph2(G, C0, C1,category_dict):
    '''
    We have done the same as before, but we runned this method for the last 2 categories + the input category.
    '''
    c0 = category_dict[C0][0:2000]
    #with tqdm(total=value) as pbar:
    shortest_paths_1 = list()
    shortest_paths_2 = list()
    shortest_paths_3 = list()
    #shortest_paths_4 = list()

    for i in tnrange(len(c0)):
        
        root=c0[i]
        #pbar.write("proccesed: %d"  %c0)
        #pbar.update(1)
        step = 0
        seen=set([root])
        queue=collections.deque([(root,step)])
        while queue:
            vertex=queue.popleft()
            
            
            if C1[0] in G.node[vertex[0]]['Category'] and C0 not in G.node[vertex[0]]['Category']:
                    shortest_paths_1.append(step)
                 
            elif C1[1] in G.node[vertex[0]]['Category'] and C0 not in G.node[vertex[0]]['Category']:
                    shortest_paths_2.append(step)
                   
            
            elif C1[2] in G.node[vertex[0]]['Category'] and C0 not in G.node[vertex[0]]['Category']:
                    shortest_paths_3.append(step)
                   
            neighbors1 = list(G[vertex[0]])
            
            step=vertex[1]+1
            if neighbors1 == []:
                continue
              
            
            for i in neighbors1:
                if i not in seen:
                    queue.append((i,step))                    
                    seen.add(i)
                    
    for i in range(len(C1)):
        lc = len(category_dict[C1[i]])
        
        if len(eval('shortest_paths_%d'% (i+1))) != lc:
            
            diff = abs(len(eval('shortest_paths_%d'% (i+1))) - lc*len(c0))
            aux_l = [math.inf for i in range(diff)]
            eval("shortest_paths_{}".format(i+1)).extend(aux_l)
    
    return [(C1[0], np.median(np.array(sorted(shortest_paths_1)))), (C1[1], np.median(np.array(sorted(shortest_paths_2))))
           (C1[2], np.median(np.array(sorted(shortest_paths_3))))]#(C1[3], np.median(np.array(sorted(shortest_paths_4))))]


def steps(G,category_dict):
    '''
    This method is been created for computing the subgraph.
    At first, we re-assign for each node only one category: exactly the category to which it belongs and that is the closest category to the input category ( C0 ).
    
    After this, we initialize each node of the original graph with a new attribute: 'Score'.
    Hence, we compute the subgraph for the list of nodes present in the input category, as first nodes in the subgraph and separately from the others.
    And then we iterate through each following category that is present into the distance ranking.
    For each category we create the subgraph from all the nodes (also the previouses),
    but the iteration for give scores is done only with the nodes of the category considered;
    For each of these nodes we checked in_edges and the nodes related if:
    - the nodes haven't still had the score. 
    - if the nodes belong to that category as well.
    - if they already have been assigned the score
    In this way we could assign scores to each node of each category    
    '''
    dfg=pd.read_csv('ranking_table.csv')
    for e in G:
        Distance={}
        if len(G.node[e]['Category'])>1:
            for i in G.node[e]['Category']:
                Distance[i]=(dfg.loc[dfg.Category==i]['Distance'].values)[0]
            sorted_d = sorted(Distance.items(), key=operator.itemgetter(1))
            G.node[e]['Category']=sorted_d[0][0]
        else:
            G.node[e]['Category']=G.node[e]['Category'][0]
    
    category_dict1={}
    for k in category_dict:
        m=category_dict[k]
        l=[]
        for n in m:
            if G.node[n]['Category']==k:
                l.append(n)
        category_dict1[k]=l
    
    nodes_G = G.nodes()
    for n in nodes_G:
        G.node[n]['score'] = -1
    
    input_category='Indian_films'
    c0 = category_dict[input_category][0:2000]    
    sub = G.subgraph(c0)
    for s in sub:
        G.node[s]['score'] = len(sub.in_edges(s))
    categories = list(dfg['Category'].values) #taking all categories from the ranking dataframe 
    categories.remove('Indian_films')
    
    from collections import defaultdict
    l = c0 #list of nodes in the subgraph (now only input_category nodes)
    for i in tnrange(len(categories)):
        c = categories[i]
        l1 = category_dict1[c]
        l += l1
        sub1 = G.subgraph(l)
        d1=dict.fromkeys(l1, -2)
        for e1 in l1:
            if G.node[e1]['score']!=-1:
                continue
            else:
                ie1 = sub1.in_edges(e1)
                ie1 = [el[0] for el in ie1] 
                score = 0
                for f in ie1:
                    try:
                        if d1[f]== -2:
                            score+=1
                            continue
                        elif G.node[f]['score'] == -1:
                            score+=1
                            continue
                        else:
                            score += G.node[f]['score'] 
                    except:
                        score += G.node[f]['score']
                    #elif G.node[f]['score'] == -1:
                        #score +=1                    
                G.node[e1]['score'] = score
        del d1
    return G