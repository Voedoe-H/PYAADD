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
    
    def _apply(self, node1, node2, operation):
        """
        Recursively apply the operation to the nodes of two BDDA instances, ensuring that
        the resulting nodes are of BDDA types.
        
        :param node1: Current node of the first BDDA.
        :param node2: Current node of the second BDDA.
        :param operation: Function to apply to the leaf nodes.
        :return: A new node resulting from the operation.
        """
        if node1 is None or node2 is None:
            return None
        
        if isinstance(node1, BDDALeafNode) and isinstance(node2, BDDALeafNode):
            new_value = operation(node1.value, node2.value)
            return BDDALeafNode(new_value)
        
        if isinstance(node1, BDDALeafNode) and isinstance(node2, BDDANode):
            high = self._apply(node1, node2.high, operation)
            low = self._apply(node1, node2.low, operation)
            return BDDANode(node2.constraint_id, high, low)

        if isinstance(node1, BDDANode) and isinstance(node2, BDDALeafNode):
            high = self._apply(node1.high, node2, operation)
            low = self._apply(node1.low, node2, operation)
            return BDDANode(node1.constraint_id, high, low)

        if isinstance(node1, BDDANode) and isinstance(node2, BDDANode):
            if node1.constraint_id == node2.constraint_id:
                high = self._apply(node1.high, node2.high, operation)
                low = self._apply(node1.low, node2.low, operation)
                return BDDANode(node1.constraint_id, high, low)
            elif node1.constraint_id > node2.constraint_id:
                high = self._apply(node1.high, node2, operation)
                low = self._apply(node1.low, node2, operation)
                return BDDANode(node1.constraint_id, high, low)
            else:
                high = self._apply(node1, node2.high, operation)
                low = self._apply(node1, node2.low, operation)
                return BDDANode(node2.constraint_id, high, low)

        return None
