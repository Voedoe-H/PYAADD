import pytest
from sys import intern
from pydd.builder import Builder
from pydd.bdda import *

def test_bdda__1():
    builder = Builder()

    leaf_node1 = BDDALeafNode(True)
    leaf_node2 = BDDALeafNode(True)
    leaf_node3 = BDDALeafNode(False)

    bdda1 = BDDA(builder)
    bdda2 = BDDA(builder)

    internal_node = BDDANode(constraint_id=10,high=leaf_node1,low=leaf_node2)

    bdda1.build(internal_node)
    bdda2.build(leaf_node3)

    def AND(value1,value2):
        return value1 and value2
    
    res = bdda1.apply(bdda2,AND)

    res.print_tree()

def test_bdda__2():
    builder = Builder()

    leaf_node1 = BDDALeafNode(True)
    leaf_node2 = BDDALeafNode(True)
    leaf_node3 = BDDALeafNode(False)
    leaf_node4 = BDDALeafNode(False)

    bdda1 = BDDA(builder)
    bdda2 = BDDA(builder)

    internal_node_1 = BDDANode(constraint_id=10,high=leaf_node1, low=leaf_node2)
    internal_node_2 = BDDANode(constraint_id=20,high=leaf_node3, low=leaf_node4)

    bdda1.build(internal_node_1)
    bdda2.build(internal_node_2)

    def AND(value1,value2):
        return value1 and value2

    res = bdda1.apply(bdda2,AND)
    assert res.root.high.high.value == False
    assert res.root.high.low.value == False
    assert res.root.low.high.value == False
    assert res.root.low.low.value == False

test_bdda__1()