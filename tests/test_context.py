import pytest
from pydd.builder import Builder
from pydd.aadd import *
from pydd.utils import *
from pydd.bdda import *

def test_aadd_bdda_interaction():
    
    context = Builder()

    affine_form_1 = context.create_affine_form(1.0, {'x': 2.0})
    affine_form_2 = context.create_affine_form(3.0, {'x': 4.0})

    aadd_leaf_1 = AADDLeafNode(affine_form_1)
    aadd_leaf_2 = AADDLeafNode(affine_form_2)

    aadd_internal = AADDNode(constraint_id=10,high=aadd_leaf_1,low=aadd_leaf_2)
    
    bdda_leaf = BDDALeafNode(False)

    aadd = AADD(context)
    bdda = BDDA(context)

    aadd.build(aadd_internal)
    bdda.build(bdda_leaf)

    print("AADD")
    aadd.print_tree()
    print("BDDA")
    bdda.print_tree()
    
    res = multiply_aadd_bdda(aadd,bdda)
    res.print_tree()

test_aadd_bdda_interaction()