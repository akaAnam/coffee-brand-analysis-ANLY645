import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os, glob
import imageio.v2 as imageio
from IPython.display import display, Image
import math
from math import log
from itertools import accumulate

#------------------------------
# PLOT NETWORK
#------------------------------
def plot_network(G,
                 image_save_name,
                 title,
                 title_font_size,
                 node_colors,
                 node_sizes=40,
                 edge_colors='black',
                 fig_size_w=16,
                 fig_size_h=16,
                 layout='random',
                 labels=False):

    ### Set position layout
    if(layout=="random"):
        pos=nx.random_layout(G)
    elif(layout=="spring"):
        pos=nx.spring_layout(G)

    ### Initialize plot
    fig, ax = plt.subplots()
    fig.set_size_inches(fig_size_w, fig_size_h)

    ### Assign attributes for node size
    # Degree centrality
    if node_sizes=="degree":
        ns = list(dict(nx.degree(G)).values())
        node_sizes = [4000*u/(0.01+max(ns)) for u in ns]
    # Betweenness centrality
    elif node_sizes=="betweenness":
        ns = list(dict(nx.betweenness_centrality(G)).values())
        node_sizes = [4000*u/(0.01+max(ns)) for u in ns]
    # Closeness centrality
    elif node_sizes=="closeness":
        ns = list(dict(nx.closeness_centrality(G)).values())
        node_sizes = [50*u/(0.01+max(ns)) for u in ns]
    # User number of followers
    elif node_sizes=="num_followers":
        ns = [data.get("user_followers_count") for node, data in G.nodes(data=True)]
        node_sizes = [3000*u/(0.01+max(ns)) for u in ns]
    # Tweet's number of retweets
    elif node_sizes=="num_retweets":
        ns = [data.get("retweet_count") for node, data in G.nodes(data=True)]
        node_sizes = [5000*u/(0.01+max(ns)) for u in ns]
    # Tweet's number of favorites
    elif node_sizes=="num_favorites":
        ns = [data.get("favorite_count") for node, data in G.nodes(data=True)]
        node_sizes = [5000*u/(0.01+max(ns)) for u in ns]
    # Tweet's number of favorites
    elif node_sizes=="normalized_degree":
        ns = [data.get("normalized_degree") for node, data in G.nodes(data=True)]
        node_sizes = [4000*u/(0.01+max(ns)) for u in ns]

    ### Plot network
    nx.draw(G,
            with_labels=labels,
            edgecolors=edge_colors,
            node_color=node_colors,
            node_size=node_sizes,
            font_color='white',
            font_size=15,
            pos=pos
            )
    ax.set_title(title, fontsize=title_font_size)

    ### Save & show figure
    plt.savefig(image_save_name, bbox_inches='tight', format="PNG")
    plt.show()

#------------------------------
# Plot Side-by-Side Networks
#------------------------------
def plot_two_networks(G_a,
                      G_b,
                      image_save_name,
                      main_title,
                      title_a,
                      title_b,
                      main_title_font_size,
                      sub_titles_font_size,
                      node_colors_a,
                      node_colors_b,
                      node_sizes_both=40,
                      node_sizes_a=None,
                      node_sizes_b=None,
                      edge_colors='black',
                      fig_size_w=16,
                      fig_size_h=10,
                      layout='random',
                      labels=False):

    ### Set position layout
    if(layout=="spring"):
        pos_a=nx.spring_layout(G_a)
        pos_b=nx.spring_layout(G_b)
    if(layout=="random"):
        pos_a=nx.random_layout(G_a)
        pos_b=nx.random_layout(G_b)

    ### Initialize plot
    fig, ax = plt.subplots(nrows=1, ncols=2)
    fig.set_size_inches(fig_size_w, fig_size_h)

    ### Assign attributes for node size
    if isinstance(node_sizes_both, str):
        # Degree centrality
        if node_sizes_both=="degree":
            ns_a=list(dict(nx.degree(G_a)).values())
            node_sizes_a=[4000*u/(0.01+max(ns_a)) for u in ns_a]
            ns_b=list(dict(nx.degree(G_b)).values())
            node_sizes_b=[4000*u/(0.01+max(ns_b)) for u in ns_b]    
        # Betweenness centrality
        elif node_sizes_both=="betweenness":
            ns_a=list(dict(nx.betweenness_centrality(G_a)).values())
            node_sizes_a=[6000*u/(0.01+max(ns_a)) for u in ns_a]
            ns_b=list(dict(nx.betweenness_centrality(G_b)).values())
            node_sizes_b=[6000*u/(0.01+max(ns_b)) for u in ns_b]    
        # Closeness centrality
        elif node_sizes_both=="closeness":
            ns_a=list(dict(nx.closeness_centrality(G_a)).values())
            node_sizes_a=[50*u/(0.01+max(ns_a)) for u in ns_a]
            ns_b=list(dict(nx.closeness_centrality(G_b)).values())
            node_sizes_b=[50*u/(0.01+max(ns_b)) for u in ns_b]
        # User number of followers
        elif node_sizes_both=="num_followers":
            ns_a = [data.get("user_followers_count") for node, data in G_a.nodes(data=True)]
            node_sizes_a=[3000*u/(0.01+max(ns_a)) for u in ns_a]
            ns_b = [data.get("user_followers_count") for node, data in G_b.nodes(data=True)]
            node_sizes_b=[3000*u/(0.01+max(ns_b)) for u in ns_b]
        # Tweet's number of retweets
        elif node_sizes_both=="num_retweets":
            ns_a=[data.get("retweet_count") for node, data in G_a.nodes(data=True)]
            node_sizes_a=[5000*u/(0.01+max(ns_a)) for u in ns_a]
            ns_b=[data.get("retweet_count") for node, data in G_b.nodes(data=True)]
            node_sizes_b=[5000*u/(0.01+max(ns_b)) for u in ns_b]
        # Tweet's number of favorites
        elif node_sizes_both=="num_favorites":
            ns_a=[data.get("favorite_count") for node, data in G_a.nodes(data=True)]
            node_sizes_a=[5000*u/(0.01+max(ns_a)) for u in ns_a]
            ns_b=[data.get("favorite_count") for node, data in G_b.nodes(data=True)]
            node_sizes_b=[5000*u/(0.01+max(ns_b)) for u in ns_b]
        elif node_sizes_both=="normalized_degree":
            ns_a = [data.get("normalized_degree") for node, data in G_a.nodes(data=True)]
            node_sizes_a = [4000*u/(0.01+max(ns_a)) for u in ns_a]
            ns_b = [data.get("normalized_degree") for node, data in G_b.nodes(data=True)]
            node_sizes_b = [4000*u/(0.01+max(ns_b)) for u in ns_b]
        elif node_sizes_both=="different":
            node_sizes_a=node_sizes_a
            node_sizes_b=node_sizes_b            
        else:
            raise ValueError('incorrect node_size option')
    else:
        node_sizes_a=node_sizes_both
        node_sizes_b=node_sizes_both

    ### Plot networks
    # Network a
    nx.draw(G_a,
            with_labels=labels,
            edgecolors=edge_colors,
            node_color=node_colors_a,
            node_size=node_sizes_a,
            font_color='white',
            font_size=15,
            pos=pos_a,
            ax=ax[0]
            )
    ax[0].set_title(title_a, fontsize=sub_titles_font_size)
    # Network b
    nx.draw(G_b,
            with_labels=labels,
            edgecolors=edge_colors,
            node_color=node_colors_b,
            node_size=node_sizes_b,
            font_color='white',
            font_size=15,
            pos=pos_b,
            ax=ax[1]
            )
    ax[1].set_title(title_b, fontsize=sub_titles_font_size)
    # Set main title
    fig.suptitle(main_title, fontsize=main_title_font_size)

    ### Save & show figure
    plt.savefig(image_save_name, bbox_inches='tight', format="PNG")
    plt.show()
        
#------------------------------
# ISOLATE GCC
#------------------------------
def isolate_GCC(G):
    comps = sorted(nx.connected_components (G),key=len, reverse=True) 
    nodes_in_giant_comp = comps[0]
    return nx.subgraph(G, nodes_in_giant_comp)
