import sys

from ete3 import Tree


def read_phylogenetic_tree(path: str) -> list[str]:
    with open(path, "r") as f:
        tree_str = f.read()
    return [x.replace("\n", "") + ";" for x in tree_str.split(";")][:-1]


newick_strings = read_phylogenetic_tree("handins/handin1/newick.tre")


class AdjacencyList:
    # directed unweighted adjacency list representation of a graph
    # stores all outgoing edges for each vertex
    def __init__(self) -> None:
        self.adjList = {}

    def add_vertex(self, vertex: str) -> None:
        if vertex not in self.adjList.keys():
            self.adjList[vertex] = []

    def add_edge(self, start_vertex: str, end_vertex: str) -> None:
        if (start_vertex not in self.adjList.keys()) or (
            end_vertex not in self.adjList.keys()
        ):
            raise Exception("Some provided vertex does not exists in the graph")
        elif start_vertex == end_vertex:
            raise Exception("A vertex can't have an edge to itself")
        else:
            self.adjList[start_vertex].append(end_vertex)

    def __str__(self) -> str:
        result = ""
        for vertex, neighbors in self.adjList.items():
            result += f"{vertex}: {neighbors}\n"
        return result


def main():
    graph_representations = []  # stores the graph representations for each tree

    for tree in newick_strings:
        tree = Tree(tree, format=8)
        adjList = AdjacencyList()

        # give labels to intermediate nodes with no labels
        name_iterator = 0
        for node in tree.traverse():
            if node.name == "":
                node.name = str(
                    name_iterator
                )  # give unlabelled intermediate nodes a unique label

            adjList.add_vertex(node.name)
            name_iterator += 1

        # add edges
        for node in tree.traverse():
            if children := node.get_children():  # if current node is not a leaf node
                for (
                    child_node
                ) in children:  # add edges going to each child from current node
                    adjList.add_vertex(child_node.name)
                    adjList.add_edge(start_vertex=node.name, end_vertex=child_node.name)

        graph_representations.append(adjList)

    print(graph_representations[0])  # example


if __name__ == "__main__":
    main()
