from sys import intern
import pytest
from pydd.builder import Builder
from pydd.bdda import *

def bdda_test_1():
    builder = Builder()

    leaf_node1 = BDDALeafNode(True)
    leaf_node2 = BDDALeafNode(True)
    leaf_node3 = BDDALeafNode(False)

    bdda1 = BDDA(builder)
    bdda2 = BDDA(builder)

    internal_node = BDDANode(constraint_id=10,high=leaf_node1,low=leaf_node2)

    bdda1.build(internal_node)
    bdda2.build(leaf_node3)

    def AND(node1,node2):
        return node1.value and node2.value
    
    res = bdda1.apply(bdda2,AND)

    res.print_tree()

bdda_test_1()