from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from node2vec import Node2Vec
import networkx as nx



def AST2Graph(parser_result):
    parser, root = parser_result
    graph = nx.Graph()
    graph.add_node(0)

    labels = dict()
    labels[0] = -1

    def fill_nx_graph(parser, node, parent):
        new_node_id = parent
        if node.getChildCount() != 1:
            label = None
            if isinstance(node, TerminalNodeImpl):
                label = node.getSymbol().type
            else:
                label = node.getRuleIndex()
                # label = parser.ruleNames[node.getRuleIndex()]

            new_node_id = graph.number_of_nodes()
            graph.add_node(new_node_id)
            graph.add_edge(parent, new_node_id)
            labels[new_node_id] = label

        for i in range(node.getChildCount()):
            child = node.getChild(i)
            fill_nx_graph(parser, child, new_node_id)

    fill_nx_graph(parser_result[0], parser_result[1], 0)
    return graph, labels



# Generate walks
def run(parser_result):
    graph, labels = AST2Graph(parser_result)
    node2vec = Node2Vec(graph, dimensions=10, walk_length=10, num_walks=9, workers=3)

    # reformatted_walks = [(labels[int(x)] for x in walk)for walk in node2vec.walks]


    reformatted_walks = [[str(labels[int(x)]) for x in walk] for walk in node2vec.walks]
    node2vec.walks = reformatted_walks


    # Learn embeddings
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    # print(model.wv.vocab)
    # for word in model.wv.vocab:
    #     print(word, model.wv[word])
    return model.wv["-1"]