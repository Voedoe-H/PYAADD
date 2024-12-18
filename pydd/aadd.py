from .affine_form import AffineForm
from .builder import Builder
from .decisiondiagram import *
from .bdda import *
from scipy.optimize import linprog


class AADDLeafNode(LeafNode):

    def __init__(self, value):
        super().__init__(value)
        self.min = self.value.

    def __repr__(self):
        return f"AADDLeafNode(affine_form={self.value})"

class AADDNode(DecisionTreeNode):
    """
        Class representing an internal node of an AADD. An internal node represents a constraint of the form af <= 0 where af is an affine form. As af is a range this is interpreted as a boolean decision variable.
        This is due to the fact that the inequation can be satsified or not, depending on the assignment of the affine forms coefficients and central value as well as the assignments of the noise symbols.
        Attributes:
            constraint_id (int): An integer ID that identiefies an affine form saved in the builder and interpeted as described above. Saving it in the builder and identifying it this way allows sharing across multiple AADDs
            high (AADDNode or AADDLeafNode): Sub tree that is taken if the constraint is satisfied
            low (AADDNode or AADDLeafNode): Sub tree that is taken if the constraint is not satsfied
    """
    def __init__(self, constraint_id: int, high=None, low=None):
        # constraint_id refers to the affine form stored in the builder
        self.constraint_id = constraint_id
        self.high = high  # Left branch
        self.low = low  # Right branch

    def __repr__(self):
        return f"AADDNode(Condition ID: {self.constraint_id}, Left: {self.high}, Right: {self.low})"

class AADD(DecisionTree):
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
    
    
    def create_tree(self):
        return AADD(self.builder)

    def create_node(self, constraint_id, high, low):
        return AADDNode(constraint_id, high, low)
    
    def create_leaf(self, affine_form):
        return AADDLeafNode(affine_form)
    
    def __add__(self,other):
        if not isinstance(other,AADD):
            return NotImplemented

        def add_affine_forms(affine_form1, affine_form2):
            # Implement affine form addition logic
            return affine_form1 + affine_form2  # Placeholder logic

        return self.apply(other,add_affine_forms)

    def __sub__(self,other):
        if not isinstance(other,AADD):
            return NotImplemented
        def sub_affine_forms(affine_form1, affine_form2):
            return affine_form1 - affine_form2
        return self.apply(other,sub_affine_forms)

    def __mul__(self,other):
        if not (isinstance(other,AADD) or isinstance(other,BDDA)):
            return NotImplemented
        
        return NotImplemented