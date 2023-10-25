# %%
import networkx as nx
import pandas as pd


# %%
def read_nodes(data_path):
    re_expression = "[|\t]+"

    # only read the first three columns
    df = pd.read_csv(
        data_path, sep=re_expression, header=None, engine="python", usecols=[0, 1, 2]
    )

    df.columns = ["Node ID", "Parent Node ID", "rank"]

    return df


# Store the data as a graph
def build(df: pd.DataFrame) -> nx.DiGraph:
    G = nx.DiGraph()
    for _, row in df.iterrows():
        parent_node_id = row["Parent Node ID"]
        node_id = row["Node ID"]

        # Add nodes
        if not G.has_node(parent_node_id):
            G.add_node(parent_node_id, name=parent_node_id)

        G.add_node(node_id, name=node_id)

        # Add edges
        # if parent_node_id != node_id: # no cycles
        G.add_edge(parent_node_id, node_id)
    return G


def restrict_tree(tree: nx.DiGraph, df: pd.DataFrame) -> nx.DiGraph:
    restricted_tree = total_G.copy()
    standard_taxonomic_ranks = [
        "superkingdom",  # is actually kingdom
        "phylum",
        "class",
        "order",
        "family",
        "genus",
        "species",
    ]

    non_standard_nodes = list(
        df[~df["rank"].isin(standard_taxonomic_ranks)]["Node ID"].values
    )  # list of nodes ID with non-standard taxonomic rank
    no_parent_node_counter = 0
    for node_ID in non_standard_nodes:
        if parent_nodes := [c for c, _ in restricted_tree.in_edges(node_ID)]:
            # Check that there in fact only is one parent for each node
            if len(parent_nodes) > 1:
                raise Exception(f"There are multiple parent nodes for node {node_ID}")

            parent_node_ID = parent_nodes[0]

            # connect each child node from current node to the parent node of current node
            for child_node_ID in [
                child for _, child in restricted_tree.out_edges(node_ID)
            ]:
                restricted_tree.add_edge(parent_node_ID, child_node_ID)

            # remove current node
            restricted_tree.remove_node(node_ID)
        else:
            # current node has no parents
            no_parent_node_counter += 1
            continue

    print(f"Found {no_parent_node_counter} nodes with no parents")
    return restricted_tree


def get_parent(tree: nx.DiGraph, node_ID: int) -> int:
    parent_nodes = [c for c, _ in restricted_tree.in_edges(node_ID)]
    if len(parent_nodes) > 1:
        raise Exception(f"There are multiple parent nodes for node {node_ID}")
    return parent_nodes[0]


def get_children(tree: nx.DiGraph, node_ID: int) -> list[int]:
    return [c for c, _ in restricted_tree.in_edges(node_ID)]


def contract_tree(tree: nx.DiGraph) -> nx.DiGraph:
    return_tree = tree.copy()

    for node in tree.nodes:
        # If there is only one child and parent for the node
        if tree.in_degree(node) == 1 and tree.out_degree(node) == 1:
            tree.add_edge(
                get_parent(return_tree, node), get_children(return_tree, node)[0]
            )
            return_tree.remove_node(node)

    return return_tree


def read_mapping(mapping_path):
    mappings = {}
    with open(mapping_path, "r") as f:
        for line in f:
            tokens = line.strip().split()
            sequence_id = tokens[0]
            tax_ids = list(map(int, tokens[1:]))
            mappings[sequence_id] = tax_ids
    return mappings


def find_lineage(tax_id, df):
    """Returns a list of nodes that connects the taxa to the root node"""
    lineage = []
    while tax_id != 1:
        node_info = df[df["Node ID"] == tax_id].iloc[0]
        lineage.append((node_info["Node ID"], node_info["rank"]))
        tax_id = node_info["Parent Node ID"]

    # Add the root
    node_info = df[df["Node ID"] == tax_id].iloc[0]
    lineage.append((node_info["Node ID"], node_info["rank"]))

    return lineage[::-1]  # reverse to get the lineage from root to leaf


def find_lca(G, node_list):
    ancestors_list = [nx.ancestors(G, node) for node in node_list]
    common_ancestors = set.intersection(*map(set, ancestors_list))
    common_ancestors.add(1)

    # Find the LCA among common ancestors by traversing up the tree
    lca = None
    if common_ancestors:
        lca = min(common_ancestors)
    return lca


# %%

if __name__ == "__main__":
    df = read_nodes("handins/handin6/nodes.dmp")
    total_G = build(df)
    total_G.remove_edge(1, 1)  # remove the one cycle
    # print(nx.is_tree(total_G))
    # print(nx.is_directed_acyclic_graph(total_G))

    # Restrict the tree
    restricted_tree = restrict_tree(total_G, df)

    # Find lineages in restricted tree

    mappings = read_mapping("handins/handin6/mapping.txt")

    # Find lineages
    lineages = {}
    for sequence_id, tax_ids in mappings.items():
        lineages_for_seq = []
        for tax_id in tax_ids:
            lineage = find_lineage(tax_id, df)
            lineages_for_seq.append(lineage)
        lineages[sequence_id] = lineages_for_seq

    lca_skeleton_tree = {}
    for read_id, node_list in mappings.items():
        lca = find_lca(restricted_tree, node_list)
        if lca is not None:
            # Get all nodes from the root to each node in node_list and the LCA
            nodes_to_include = set()
            nodes_to_include.add(1)
            for node in node_list:
                nodes_to_include.update(
                    nx.shortest_path(restricted_tree, source=1, target=node)
                )
                nodes_to_include.update(
                    nx.shortest_path(restricted_tree, source=1, target=lca)
                )

            skeleton_tree = restricted_tree.subgraph(nodes_to_include)

            lca_skeleton_tree[read_id] = skeleton_tree

    # Number of nodes in LCA skeleton tree for each sequences read:
    # There should be 16 in the first one
    num_nodes_per_read = {}
    for read_id, lca_tree in lca_skeleton_tree.items():
        num_nodes = len(lca_tree.nodes())
        num_nodes_per_read[read_id] = num_nodes

    print("Number of nodes in LCA skeleton tree for each sequence read:")
    for read_id, num_nodes in num_nodes_per_read.items():
        print(f"{read_id}: {num_nodes} nodes")
