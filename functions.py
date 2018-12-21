#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tqdm import tnrange, tqdm_notebook
import collections
import math
import numpy as np
from collections import defaultdict
import threading


# In[ ]:


def graph_dict():
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


# In[ ]:


def create_graph_and_dict():
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


# In[ ]:



# In our Algorithm for each root which is in the input category we go through graph, and each time we check each node attributes
#if it is belonging to the categories that we are looking for and at the same time it doesn't belong to input category. 
#Therefore , each time the function is called , the nodes in the path of the roots are checked for 4 category

def distance_graph(G, C0, C1):
   
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


# In[ ]:





# In[ ]:





#@autojit
def distance_graph2(G, C0, C1):
   
    c0 = category_dict[C0][0:2000]
    #for i in range(len(C1)):
        #exec(f'shortest_paths_{i}=[]')

    #with tqdm(total=value) as pbar:
    shortest_paths_1 = list()
    shortest_paths_2 = list()
    shortest_paths_3 = list()
    #shortest_paths_4 = list()

    for i in tnrange(len(c0)):
        
    #for i in range(len(c0)):
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
                  
            #elif C1[3] in G.node[vertex[0]]['Category'] and C0 not in G.node[vertex[0]]['Category']:
                    #shortest_paths_4.append(step)
                    
            
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
            #print(lc, diff, len(eval('shortest_paths_%d'% (i+1))))
            aux_l = [math.inf for i in range(diff)]
            eval("shortest_paths_{}".format(i+1)).extend(aux_l)
    
    return [(C1[0], np.median(np.array(sorted(shortest_paths_1)))), (C1[1], np.median(np.array(sorted(shortest_paths_2))))]
           (C1[2], np.median(np.array(sorted(shortest_paths_3))))#(C1[3], np.median(np.array(sorted(shortest_paths_4))))]


# In[ ]:


def steps(G):
    nodes_G = list(G.nodes())

    for n in nodes_G:
        G.node[n]['score'] = -1

    input_category='Indian_films'
    c0 = category_dict[input_category][0:2000]    
    sub = G.subgraph(c0)

    for s in sub:

        G.node[s]['score'] = len(sub.in_edges(s))

    categories = dfg['Category'].values #taking all categories from the ranking dataframe 
    categories=list(categories)
    categories.remove('Indian_films')    

    l = c0 #list of nodes in the subgraph (now only input_category nodes)

    for i in tnrange(len(categories)):
        c = categories[i]
        l1 = category_dict[c]
        l += l1
        sub1 = G.subgraph(l)
        for e1 in l1:
            if G.node[e1]['score']!=-1:
                continue
            else:
                ie1 = sub1.in_edges(e1)
                ie1 = [el[0] for el in ie1] 
                score = 0
                for f in ie1:
                    if G.node[f]['score']==-1:
                        score+=1
                        continue
                    #elif G.node[f]['score'] == -1:
                        #score +=1
                    else:
                        score += G.node[f]['score']
                G.node[e1]['score'] = score
        return G


# In[ ]:




