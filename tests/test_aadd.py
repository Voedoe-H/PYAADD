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
    
def apply_test_2():
    builder = Builder()

    # Create affine forms to use in the leaf nodes
    form1_id = builder.create_affine_form(1.0, {'x': 2.0})
    form2_id = builder.create_affine_form(3.0, {'x': 4.0})
    form3_id = builder.create_affine_form(2.0, {'y': 1.0})
    form4_id = builder.create_affine_form(5.0, {'y': 3.0})

    # Print form IDs for debugging
    print(f"form1_id: {form1_id}, form2_id: {form2_id}, form3_id: {form3_id}, form4_id: {form4_id}")

    # Create two AADDs
    aadd1 = AADD(builder)
    aadd2 = AADD(builder)

    # Define leaf nodes with the created affine forms
    leaf_node1_aadd1 = LeafNode(form1_id)  # Affine form 1
    leaf_node2_aadd1 = LeafNode(form2_id)  # Affine form 2

    leaf_node1_aadd2 = LeafNode(form3_id)  # Affine form 3
    leaf_node2_aadd2 = LeafNode(form4_id)  # Affine form 4

    # Define internal nodes with conditions (different constraints for internal nodes)
    internal_node_aadd1 = AADDNode(constraint_id=10, left=leaf_node1_aadd1, right=leaf_node2_aadd1)
    internal_node_aadd2 = AADDNode(constraint_id=20, left=leaf_node1_aadd2, right=leaf_node2_aadd2)

    # Build the AADDs with one internal node each
    aadd1.build(internal_node_aadd1)
    aadd2.build(internal_node_aadd2)

    aadd1.print_tree()
    print("-----")
    aadd2.print_tree()

    # Define an operation for affine forms
    def add_affine_forms(affine_form1, affine_form2):
        # Implement affine form addition logic
        return affine_form1 + affine_form2  # Placeholder logic

    result_aadd = aadd1.apply(aadd2, add_affine_forms)

    # Print the result tree
    result_aadd.print_tree()

apply_test_2()