from .builder import Builder
from .decisiondiagram import *

class BDDALeafNode(LeafNode):
    def __repr__(self):
        return f"BDDALeaf(value={self.value})"


class BDDANode(DecisionTreeNode):
    def __repr__(self):
        return f"BDDANode(Condition ID: {self.constraint_id}, High: {self.high}, Low: {self.low})"

class BDDA(DecisionTree):
    def __init__(self, builder: Builder):
        super().__init__(builder)

    def create_tree(self):
        return BDDA(self.builder)

    def create_node(self, constraint_id, high, low):
        return BDDANode(constraint_id, high, low)

    def create_leaf(self, boolean_value):
        return BDDALeafNode(boolean_value)

    def __and__(self,other):
        if not isinstance(other,BDDA):
            return NotImplemented
        def AND(v1,v2):
            return v1 and v2
        return self.apply(other,AND)
    
    def __or__(self,other):
        if not isinstance(other,BDDA):
            return NotImplemented
        def OR(v1,v2):
            return v1 or v2
        return self.apply(other,OR)
  