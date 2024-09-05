from .affine_form import AffineForm
from .builder import Builder

class LeafNode:
    """
        Class representing a leaf of an AADDD
        Attributes:
            affine_form (affine_form): Affine form representing a value range that the variable represneted by the 
                                      corresponding variable can take.
    """
    def __init__(self, affine_form):
         self.affine_form = affine_form

    def __repr__(self):
        return f"LeafNode(affine_form={self.affine_form})"

class AADDNode:
    """
        Class representing an internal node of an AADD. An internal node represents a constraint of the form af <= 0 where af is an affine form. As af is a range this is interpreted as a boolean decision variable.
        This is due to the fact that the inequation can be satsified or not, depending on the assignment of the affine forms coefficients and central value as well as the assignments of the noise symbols.
        Attributes:
            constraint_id (int): An integer ID that identiefies an affine form saved in the builder and interpeted as described above. Saving it in the builder and identifying it this way allows sharing across multiple AADDs
            high (AADDNode or LeafNode): Sub tree that is taken if the constraint is satisfied
            low (AADDNode or LeafNode): Sub tree that is taken if the constraint is not satsfied
    """
    def __init__(self, constraint_id: int, high=None, low=None):
        # constraint_id refers to the affine form stored in the builder
        self.constraint_id = constraint_id
        self.high = high  # Left branch
        self.low = low  # Right branch

    def __repr__(self):
        return f"AADDNode(Condition ID: {self.constraint_id}, Left: {self.high}, Right: {self.low})"

class AADD:
    """
        Class that represents generally an AADD and implements arithmetic operations over AADDs. AADDs are decision trees that represent potential value ranges of a continuous variable. The potential value ranges are the affine 
        forms saved in the leafs who are taken depending if the constraints in the internal nodes are satsified on the path from the root to the specific leaf.
        Attributes:
            builder (Builder): The context object in which the AADD exists
            root (AADDNode or LeafNode): the root of the tree
    """
    def __init__(self, builder: Builder):
        self.builder = builder
        self.root = None

    def build(self, node):
        self.root = node

    def apply(self, other_aadd, operation):
        """
        Apply an operation to this AADD and another AADD.
        
        :param other_aadd: The other AADD to apply the operation with.
        :param operation: A function that defines the operation to apply to the leaf affine forms.
        :return: A new AADD resulting from the application of the operation.
        """
        new_aadd = AADD(self.builder)
        new_aadd.root = self._apply(self.root, other_aadd.root, operation)
        return new_aadd

    def _apply(self, node1, node2, operation):
        """
        Recursively apply the operation to the nodes of two AADDs.
        
        :param node1: Current node of the first AADD.
        :param node2: Current node of the second AADD.
        :param operation: Function to apply to the leaf affine forms.
        :return: A new node resulting from the operation.
        """
        if node1 is None and node2 is None:
            return None
        if node1 is None:
            # Process node2 down the tree
            return self._apply(node2, node1, operation)
        if node2 is None:
            # Process node1 down the tree
            return self._apply(node1, node2, operation)

        if isinstance(node1, LeafNode) and isinstance(node2, LeafNode):
            affine_form1 = node1.affine_form
            affine_form2 = node2.affine_form
            new_affine_form = operation(affine_form1, affine_form2)
            #new_affine_form_id = self.builder.create_affine_form(new_affine_form.constant, new_affine_form.noise_coeffs)
            return LeafNode(new_affine_form)
        
        if isinstance(node1, LeafNode) and isinstance(node2,AADDNode):
            high = self._apply(node1,node2.high, operation)
            low = self._apply(node1,node2.low, operation)
            return AADDNode(high,low,node2.constraint_id)

        if isinstance(node1,AADDNode) and isinstance(node2,LeafNode):
            high = self._apply(node1.high,node2, operation)
            low = self._apply(node1.low,node2, operation)
            return AADDNode(high,low,node1.constraint_id)

        if isinstance(node1, AADDNode) and isinstance(node2, AADDNode):
            if node1.constraint_id == node2.constraint_id:
                high = self._apply(node1.high, node2.high, operation)
                low = self._apply(node1.low, node2.low, operation)
                return AADDNode(high, low, node1.constraint_id)
            elif node1.constraint_id > node2.constraint_id:
                # Create a new node with the id of node1 and process node1's children
                high = self._apply(node1.high, node2, operation)
                low = self._apply(node1.low, node2, operation)
                return AADDNode(high, low, node1.constraint_id)
            else:
                # Create a new node with the id of node2 and process node2's children
                high = self._apply(node1, node2.high, operation)
                low = self._apply(node1, node2.low, operation)
                return AADDNode(high, low, node2.constraint_id)

        return None


    def print_tree(self):
        """
        Print the AADD tree starting from the root.
        """
        self._print_node(self.root, level=0)

    def _print_node(self, node, level):
        """
        Recursively print a node and its children.
        
        :param node: The node to print.
        :param level: The current level in the tree for indentation.
        """
        indent = "  " * level
        if node is None:
            print(f"{indent}None")
            return

        if isinstance(node, LeafNode):
            print(f"{indent}LeafNode(affine_form_id={node.affine_form})")
        elif isinstance(node, AADDNode):
            print(f"{indent}AADDNode(Condition ID: {node.constraint_id})")
            print(f"{indent}  Left:")
            self._print_node(node.high, level + 1)
            print(f"{indent}  Right:")
            self._print_node(node.low, level + 1)