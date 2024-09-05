import pytest
from pydd.builder import Builder
from pydd.aadd import *

def apply_test():
    builder = Builder()

    form1_id = builder.create_affine_form(1.0, {'x': 2.0})
    form2_id = builder.create_affine_form(3.0, {'x': 4.0})
    print(form1_id)
    # Create two AADDs
    aadd1 = AADD(builder)
    aadd2 = AADD(builder)

    # Define the leaf nodes with affine form IDs
    leaf_node1 = LeafNode(1)  # Assume constraint ID 1
    leaf_node2 = LeafNode(2)  # Assume constraint ID 2

    # Build the AADDs
    aadd1.build(leaf_node1)
    aadd2.build(leaf_node2)

    # Define an operation for affine forms
    def add_affine_forms(affine_form1, affine_form2):
        # Implement affine form addition logic
        return affine_form1 + affine_form2  # Placeholder logic

    # Apply an operation to the AADDs

    result_aadd = aadd1.apply(aadd2, add_affine_forms)
    result_aadd.print_tree()
    
apply_test()