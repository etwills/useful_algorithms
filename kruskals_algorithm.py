import random as ran
from operator import itemgetter
import sys


def kruskal_mst(graph_text):
    """
    implements kruskals algorithm to find the minumum spanning tree
    :param graph_text: text document of a network
    :return: the list of edges that form the mst
    """
    graph_process = process_input(graph_text)
    edge_list = graph_process[1] #lsit of edges
    vertices = graph_process[0] #set of all vertices
    spanning_tree_edges = []


    vertex_set = disjoint_set(vertices)  #create disjoint set
    edge_list.sort(key=lambda x: x[2]) #Sort our edge list based on weight

    num_unions = 0
    n = len(vertices)
    while num_unions < n-1: #After n-1 unions all vertices are included in the mst
        next_edge = edge_list.pop(0) #Get the edge with smallest weight
        v = next_edge[0]
        u = next_edge[1]

        if vertex_set.find_with_PC(v) != vertex_set.find_with_PC(u):#If edge doesn't create a cycle
            spanning_tree_edges.append(next_edge)
            vertex_set.union_by_rank(v, u)
            num_unions += 1

    #output_MST(spanning_tree_edges)
    return spanning_tree_edges

        #Otherwise we've encountered an edge that will create a cycle so we do nothing



def process_input(text):
    """
    This function reads the graph text. Edges in the returned edge list with be arrays of length 3 with [u, v, weight]

    :param text: the input text containing our graph
    :return: a tuple with the set of vertices in position 0 and a list of edges in position 1
    """
    vertex_set = set()  #A set to store all the vertices we encounter in the graph
    edge_list = []     #The list of all the edges
    graph_text = open(text, 'r')

    for line in graph_text:
        edge = line.split(" ")

        for i in range(3):  #This just converts each thing in edge to an integer instead of a string
            edge[i] = int(edge[i])

        if not vertex_set.__contains__(edge[0]):#If we find a new vertex add it to the set
            vertex_set.add(edge[0])
        if not vertex_set.__contains__(edge[1]):
            vertex_set.add(edge[1])
        edge_list.append(edge)
    graph_text.close()

    return [vertex_set, edge_list]




def output_MST(edge_array):
    """
    Function used to output to txt file
    :param edge_array: the array of edges in the MST
    :return: None
    """
    output = open("output_kruskal.txt", 'w')
    for edge in edge_array:
        output_line = str(edge[0]) + " " + str(edge[1]) + " " + str(edge[2]) + "\n"
        output.write(output_line)
    output.close()





class disjoint_set:
    def __init__(self, int_set):
        """
        Assume that int_set contains all the integers in interval [a,b]. So the set {1,2,4} is not allowed
        :param full_set: a set of integers. For kruskals these integers are the nodes
        """
        self.size = 0
        self.parent_array = []
        for num in int_set:
            n = len(self.parent_array)
            if num > n - 1: #If an integer is bigger than parent array we need to extend parent array
                add_array = [-1] * (num - n + 1)
                self.parent_array.extend(add_array) #Add on enough space at the end of parent array




    def find_with_PC(self, a):
        """
        finds the parent of node a and performs path compression
        :param a: a non-negative integer
        :return: p the parent of a
        """
        if self.parent_array[a] < 0: #We've found the parent because only parents are negative
            return a
        else:
            self.parent_array[a] = self.find_with_PC(self.parent_array[a])
            return self.parent_array[a]




    def union_by_rank(self, a, b):
        """
        unions two items a and b and their trees
        :param a: a non-negative integer
        :param b: a non-negative integer
        :return: nothing
        """
        root_a = self.find_with_PC(a)
        root_b = self.find_with_PC(b)

        if root_a == root_b: #Same parent?
            return False

        height_a = -1 * self.parent_array[root_a]
        height_b = -1 * self.parent_array[root_b]

        if height_a > height_b:
            self.parent_array[root_b] = root_a
        elif height_b > height_a:
            self.parent_array[root_a] = root_b
        else: #both have the same height
            self.parent_array[root_a] = root_b
            self.parent_array[root_b] = -1 * (height_b + 1)
