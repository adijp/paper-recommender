# paper-recommender

This is a joint project with [Nivasini Ananthakrishnan](https://nivasini.github.io/). 

Given a field (or subfield) of computer science, this project aims to find a set of ```n``` representative publications across different subfields. Although this question is concrete, this problem can be generalized to find the top ```n``` most "influential" nodes in a graph for some definition of influential. 

We tried out these experiments in the subfield of theoretical computer science. We used [Microsoft Knowledge API](https://docs.microsoft.com/en-us/academic-services/knowledge-exploration-service/?view=makes-3.0) to query metadata from publications from theoretical CS in conferences such as STOC, FOCS, SODA, ICALP, CCC, IPCO and CRYPTO. One can modify the ```conflist``` variable in ```relevant_papers_query.py``` to modify the list of conferences.

Data about each publication includes where it was published, the citation count, and also the list of papers citing it. In ```citationGraph.py```, we constructed a graph and its corresponding adjacency list. We processed the graph to exclude nodes with low degree (papers will low citation count). We also ensured the graph was connected by adding edges to connect disconnected components. 

We used [Spectral Clustering](https://en.wikipedia.org/wiki/Spectral_clustering) to paritition the graph into ```n``` clusters. 


sklearn 
numpy
networkx
matplotlib
