# ADM-HW5

### Data source:

- wiki-topcats-categories : txt file with the names of categories with all the nodes associated. Some nodes compare in different categories.
- wiki-topcats-reduced: informations in txt extension for the creation of the graph. 
- wiki-topcats-page-names: each node is a page, so this file keeps the information between the id of the node with the name of the page.

<p align="center">
  <img width="460" height="300" src="https://s3-ap-south-1.amazonaws.com/av-blog-media/wp-content/uploads/2018/03/Graph-Theory.jpg">
</p>

### Description of the project:

1. Homework_5.ipynb: the Jupyter file that contains executions of each method for each request. 

2. functions.py : all the methods runned in Homework_5 are written in this file.

#### Scripts:
  * graph_dict()
  * create_graph_and_dict()
  * distance_graph(G, C0, C1,category_dict)
  * distance_graph2(G, C0, C1,category_dict) (the same as before but with a different length for C1 (type list))
  * steps(G,category_dict)

### Our output source
#### Type : csv

- ranking_table.csv : it keeps saved the rank distance between our input category 'Indian_films' with the others.
- dfgscore_sort_with_names.csv : it keeps the scores computed for each node in the subgraph created.
- top_5_score_with_names.csv : it takes from the last csv just the first 5 most scored nodes per each category.
