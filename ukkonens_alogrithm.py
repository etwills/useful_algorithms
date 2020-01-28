import random
import time
import sys


class Edge:
    """
    Edge class for use in the suffix tree
    """
    def __init__(self, interval, start, end=None):
        """
        :param interval: an array of length 2, [x,y]. x is the index of string the edge represents, y is the end
                         so for example, if string is 'abcd' and edge represents 'abc', interval would be [0,2]
        :param start: the start node of the edge
        :param end: the end node of the edge
        """
        self.start_node = start
        self.end_node = end
        self.interval = interval

    def set_end_node(self, node):
        self.end_node = node

    def set_interval_end(self, end):
        """
        Sets the end value of the edge interval
        :param end: the end index
        :return: None
        """
        start = self.interval[0]
        self.interval = [start, end]

    def get_interval_length(self):
        start = self.interval[0]
        end = self.interval[1]
        return end - start + 1


class Node:
    """
    Node class for the suffix tree
    """
    def __init__(self, name=None):
        self.child_dict = {}  # A dictionary of edges between this node and its children, key is first letter in edge string
        self.suffix_link = None
        self.name = name

    def set_sl(self, node):
        self.suffix_link = node

    def add_edge(self, edge, key):
        self.child_dict[key] = edge

    def is_path(self, key):
        """
        Gets the edge from a node that begins with key
        :param key: a single character
        :return:
        """
        try:
            edge = self.child_dict[key]
            return edge
        except KeyError:
            return False  # No path exists


class SuffixTree:
    def __init__(self, string=None):
        """
        :param string: if string is left blank the tree is initialised without running Ukkonnen. Otherwise run
        """
        self.root = Node(0)
        self.string = string
        self.node_library = dict()
        self.node_library[0] = self.root
        self.num_nodes = 1
        self.edge_list = []
        if self.string is not None:
            self.ukkonen(string)

    def ukkonen(self, string):
        """
        Implements Ukkonen's algorithm

        :param string: The string to compute the suffix tree
        :return: None
        """
        self.string = string
        m = len(string)
        self.root.suffix_link = self.root

        remaining = 0
        active_node = self.root
        active_edge = -1
        active_length = 0
        left_index = 0
        end = m - 1  # Used for updating leaf nodes

        most_recent_internal_node = None  # Use this for making suffix links

        node_count = 1
        node_library = {}
        node_library[0] = self.root

        for i in range(m):
            # begin phase i
            remaining += 1

            while remaining > 0:

                char = string[i]

                if active_length == 0:  # We are at a node in the tree

                    if active_node.is_path(char) != False:

                        # is a path for our character
                        if active_node.is_path(char).get_interval_length() == 1:
                            # we move along the edge to next node
                            active_node = active_node.is_path(char).end_node
                        else:
                            active_edge = active_node.is_path(char).interval[0]  # Start index of edge here
                            active_length += 1
                        most_recent_internal_node = None  # Didn't create a new internal node so can't do suffix link
                        break  # Rule three extension leads to break


                    else:  # No path
                        # this iteration is not
                        edge = Edge([i, end], active_node)
                        active_node.add_edge(edge, string[i])
                        remaining -= 1  # b.c. we crated leaf node
                        left_index += 1
                        # Now find next place to start iteration
                        if active_node != self.root:
                            active_node = self.root

                            active_edge = left_index  # this is an index to begin traversal from

                            active_length = i - left_index

                            while active_length > 0:
                                if active_node.is_path(string[active_edge]):
                                    # There is an edge that goes out of the root for our next back character
                                    path_length = active_node.is_path(string[active_edge]).get_interval_length()
                                    if path_length > active_length:
                                        # active node is right.
                                        # active length is right
                                        # active edge is right
                                        break

                                    else:  # need to keep traversing to find position
                                        # step along to next node
                                        active_node = active_node.is_path(string[active_edge]).end_node
                                        active_edge += path_length
                                        active_length -= path_length
                                else:
                                    break

                else:  # We are not at node and are instead in the middle of an edge with at least one character left

                    active_position = active_node.is_path(string[active_edge]).interval[0] + active_length - 1

                    if string[active_position + 1] == string[i]:  # Are characters the same
                        most_recent_internal_node = None  # this extension is not a suffix link
                        # yes we are going with rule 3 extension
                        active_length += 1

                        if active_node.is_path(string[active_edge]).get_interval_length() == active_length:
                            # We reached the end of edge
                            # So we move along the edge to next node
                            # print(active_node.name, active_node.is_path(string[active_edge]).end_node.name)
                            active_node = active_node.is_path(string[active_edge]).end_node
                            # print("!!!", active_node.name)
                            active_edge = -1
                            active_length = 0

                        # most_recent_internal_node = None  # Didn't create a new internal node so can't do suffix link
                        break  # Rule three extension leads to break


                    else:  # We have a rule 2 extension
                        # We need to create a new internal node and two new edges from it
                        self.num_nodes += 1  # Added a new internal node

                        new_node = Node(node_count)
                        node_library[new_node.name] = new_node
                        self.node_library[node_count] = new_node
                        node_count += 1
                        remaining -= 1  # We created a new leaf node
                        left_index += 1

                        if active_node.is_path(string[active_edge]).end_node != None:  # We are on a non leaf edge
                            # print("we broke an edge")
                            # We break the internal edge in half when we add a new internal node
                            new_end = active_node.is_path(string[active_edge]).interval[1]
                            end_node = active_node.is_path(string[active_edge]).end_node
                            edge1 = Edge([active_position + 1, new_end], new_node)
                            edge1.set_end_node(end_node)
                            edge2 = Edge([i, end], new_node)
                            new_node.add_edge(edge1, string[active_position + 1])
                            new_node.add_edge(edge2, string[i])
                            active_node.is_path(string[active_edge]).set_interval_end(
                                active_position)  # Change old edge end from active node
                            active_node.is_path(string[active_edge]).set_end_node(
                                new_node)  # Add end node to the edge b.c. it's no
                            self.edge_list.append(active_node.is_path(string[active_edge]))
                            new_node.set_sl(self.root)

                        else:  # on a leaf edge
                            # print("on a leaf edge")
                            edge1 = Edge([active_position + 1, end], new_node)
                            edge2 = Edge([i, end], new_node)
                            new_node.add_edge(edge1, string[active_position + 1])
                            new_node.add_edge(edge2, string[i])
                            new_node.set_sl(self.root)  # Set suffix link of new internal to root

                            active_node.is_path(string[active_edge]).set_interval_end(
                                active_position)  # Change old edge end from active node
                            active_node.is_path(string[active_edge]).set_end_node(
                                new_node)  # Add end node to the edge b.c. it's no
                            self.edge_list.append(active_node.is_path(string[active_edge]))

                        if most_recent_internal_node != None:  # Created a new internal node in next phase so make suffix link
                            # print("made a link", most_recent_internal_node.name, new_node.name)
                            most_recent_internal_node.suffix_link = new_node

                        most_recent_internal_node = new_node  # Now change the most recent internal node

                        # Now find next place to start iteration

                        # print(active_node.name, active_node.suffix_link.name)

                        # this is the edge we begin traversal from at the root
                        if active_node.suffix_link == self.root:  # Are we moving to the root?
                            active_length = i - left_index
                            active_edge = left_index
                        active_node = active_node.suffix_link
                        # print(active_length, i, left_index, active_node.name)
                        while active_length > 0:  # if both are the same then we are meant to be at the root

                            path_length = active_node.is_path(string[active_edge]).get_interval_length()
                            if path_length > active_length:
                                # active node is right.
                                # active length is right
                                # active edge is right
                                break

                            elif active_length == path_length:  # need to keep traversing to find position
                                # our new start position is the next node
                                active_node = active_node.is_path(string[active_edge]).end_node
                                active_edge += path_length
                                active_length -= path_length
                            else:  # path length is bigger
                                active_node = active_node.is_path(string[active_edge]).end_node
                                active_edge += path_length
                                active_length -= path_length
                        # print(active_edge, active_length)

                # print("node list", self.node_library)
                # if i - left_index == 0:  # we finished a phase
                #
                #     most_recent_internal_node = None

    def get_suffixs(self):
        """
        This function starts the recursive traversal of the tree
        :return: suffix_array, an array of all the suffixes in the tree
        """
        string = ""
        suffix_array = []
        node = self.root
        self.get_suffix_aux(string, node, suffix_array)
        return suffix_array

    def get_suffix_aux(self, in_string, node, suffix_array):
        """
        Recursively traverses through tree to get all the suffixes as strings

        :param in_string: string of the current suffix we are building
        :param node: the node we want to explore now
        :param suffix_array: an array of the suffixes we have found so far
        :return: None
        """
        keys = node.child_dict.keys()
        sorted(keys)

        for x in keys:  # for all keys in dict
            new_string = ""
            for i in range(len(in_string)):
                new_string += in_string[i]
            edge = node.child_dict[x]
            # node_string = ""
            # for i in range(len(node_name)):
            #     node_string += node_name[i]
            inter = edge.interval
            start = int(inter[0])
            end = int(inter[1])
            for i in range(start, end + 1):
                new_string += self.string[i]

            if end + 1 != len(self.string):
                next_node = edge.end_node
                self.get_suffix_aux(new_string, next_node, suffix_array)
            else:
                suffix_array.append(new_string)

    def get_suffix_interval(self):
        """
        This method will return an array of lengths of suffixes.
        The suffixs will be sorted in alphabetical order based on the first character in the suffix,
        exactly what we require for the BWT.

        :return: An array with the lengths of suffixes as they would be in alphabetical order
        """
        suffix_array = []
        node = self.root
        self.get_suffix_interval_aux(0, node, suffix_array)
        return suffix_array

    def get_suffix_interval_aux(self, length, node, suffix_array):
        """
        Traverses the tree by exploring each edge of a node in alphabetical order
        So we look at the length of each suffix and then we can determine the final character in the BWT

        :param length: integer representing the current length of a substring
        :param node: the node in the tree to be explored
        :param suffix_array: an array of the lengths of suffixes found so far
        :return: None
        """
        key_array = list(node.child_dict.keys())
        key_array = sorted(key_array)

        for x in key_array:  # for all keys in dict
            new_len = length
            edge = node.child_dict[x]
            inter = edge.interval
            start = int(inter[0])
            end = int(inter[1])
            new_len += end - start + 1

            if end + 1 != len(self.string):
                next_node = edge.end_node
                self.get_suffix_interval_aux(new_len, next_node, suffix_array)
            else:
                suffix_array.append(new_len)

    def get_num_nodes(self):
        """
        Getter for the number of internal nodes in the suffix tree
        :return: self.num_nodes an int
        """
        return self.num_nodes


    def show_edges(self, node):
        """
        This function shows the substring each edge holds
        Traverses tree recursively and prints each edge
        :param node: the node to be examined
        """
        print("new")
        print(node.name)
        for x in node.child_dict:  # for all keys in dict
            print(x, node.is_path(x).interval)

        for x in node.child_dict:  # for all keys in dict

            edge = node.child_dict[x]

            if edge.end_node != None:
                new_node = edge.end_node

                self.show_edges(new_node)
                
     def computeBWT(self):
        """
        Computes the BWT of the self.string
        :return: bwt_string, the string of the Burrows-Wheeler transform
        """
        bwt_string = ""
        suf_array = self.get_suffix_interval()
        n = len(self.string)
        for suf_len in suf_array:
            # each item is the length of a suffix
            # We know the character in the final column of the BWT table will be the character in the string before the
            # first character in the suffix
            char = self.string[n - suf_len - 1]
            bwt_string += char
        return bwt_string
