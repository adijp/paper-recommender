import os, json
from collections import namedtuple
import numpy as np
import networkx as nx
from matplotlib import pyplot, patches
from sklearn.cluster import SpectralClustering


file_name = "data.json"
f = open(file_name,"r")
papers = json.load(f)
f.close()

Paper = namedtuple('Paper', ['pid', 'citations_count', 'year', 'rid'])

'''
Build mapping between paper ids and node ids in citation graph
'''
node_to_paper = [] # Mapping from node to paper
paper_to_node = {} # Mapping from paper to node
c = 0
for p in papers:
	if ("Id" not in p or "CC" not in p or "Y" not in p or "RId" not in p):
		continue
	if(p["Id"] in paper_to_node):
		continue
	pap = Paper(p["Id"], p["CC"], p["Y"], p["RId"])
	node_to_paper.append(pap)
	paper_to_node[p["Id"]] =  c
	c += 1

num_papers = len(node_to_paper)

# Filter low density nodes
dense_node_to_paper = [] # Subset of node_to_paper with only nodes with degree >= 2
dense_paper_to_node = {}
c=0
highest_degree = 0
highest_degree_node = 0
density_threshold = 10
for i in range(num_papers):
	degree = 0
	p = node_to_paper[i]
	p_node = i
	refs = p.rid
	for r in refs:
		if (r not in paper_to_node):
			continue
		degree += 1
	if (degree > highest_degree):
		highest_degree = degree
		highest_degree_node = i
	if (degree < density_threshold):
		continue
	dense_node_to_paper.append(p)
	dense_paper_to_node[p.pid] = c
	c += 1




num_dense_papers = len(dense_node_to_paper)
print(num_papers)
print(num_dense_papers)

node_to_paper = dense_node_to_paper
paper_to_node = dense_paper_to_node
num_papers = num_dense_papers


# print(papers[9])
G = nx.Graph()
G.add_nodes_from(range(num_papers))
adjacency_matrix = np.zeros((num_papers,num_papers))
for i in range(num_papers):
	p = node_to_paper[i]
	p_node = i
	refs = p.rid
	for r in refs:
		if(r not in paper_to_node):
			continue
		r_node = paper_to_node[r]
		adjacency_matrix[p_node][r_node] = 1
		adjacency_matrix[r_node][p_node] = 1
		# G.add_edge(p_node, r_node)
# G.remove_nodes_from((n for n,d in G.degree_iter() if d==0))

# Add edge from each node to highest degree node to ensure the graph has one component
for i in range(num_papers):
	adjacency_matrix[i][highest_degree_node] = 1
	adjacency_matrix[highest_degree_node][i] = 1

cluster_labels = SpectralClustering(n_clusters = 5, affinity = 'precomputed').fit_predict(adjacency_matrix)
# cluster_labels = clustering.labels_
print(len(cluster_labels))
print(num_papers)

colour_map = []
colours = ['black', 'blue', 'red', 'green', 'purple']

for i in range(num_papers):
	for j in range(i+1, num_papers):
		if(adjacency_matrix[i][j] == 0):
			continue
		if(cluster_labels[i] != cluster_labels[j]):
			continue
		G.add_edge(i,j)
	colour_map.append(colours[cluster_labels[i]])


density_threshold = 0
remove = [node for node,degree in dict(G.degree()).items() if degree < density_threshold]
G.remove_nodes_from(remove)

options = {"node_color": colour_map, "node_size": 1}
nx.draw(G, **options)
# nx.draw_spectral(G, **options)
pyplot.show()
