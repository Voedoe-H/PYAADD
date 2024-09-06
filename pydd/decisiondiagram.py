
class LeafNode:
    """
    Class representing a generic leaf node in a decision tree.
    
    Attributes:
        value: The value stored in the leaf, which can be of any type (e.g., AffineForm, boolean).
    """
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"LeafNode(value={self.value})"

class DecisionTreeNode:
    def __init__(self, constraint_id: int, high=None, low=None):
        self.constraint_id = constraint_id
        self.high = high
        self.low = low

    def __repr__(self):
        return f"DecisionTreeNode(Condition ID: {self.constraint_id}, High: {self.high}, Low: {self.low})"

class DecisionTree:
    def __init__(self, builder):
        self.builder = builder
        self.root = None

    def build(self, node):
        self.root = node

    def apply(self, other_tree, operation):
        """
        Apply an operation to this decision tree and another decision tree.
        :param other_tree: The other decision tree to apply the operation with.
        :param operation: A function that defines the operation to apply to the leaf nodes.
        :return: A new DecisionTree resulting from the application of the operation.
        """
        new_tree = self.__class__(self.builder)
        new_tree.root = self._apply(self.root, other_tree.root, operation)
        return new_tree

    def _apply(self, node1, node2, operation):
        """
        Recursively apply the operation to the nodes of two decision trees.
        :param node1: Current node of the first tree.
        :param node2: Current node of the second tree.
        :param operation: Function to apply to the leaf nodes.
        :return: A new node resulting from the operation.
        """
        if node1 is None or node2 is None:
            return None
        
        if isinstance(node1,LeafNode) and isinstance(node2,LeafNode):
            return LeafNode(operation(node1, node2))
        
        if isinstance(node1, LeafNode) and isinstance(node2,DecisionTreeNode):
            high = self._apply(node1,node2.high, operation)
            low = self._apply(node1,node2.low, operation)
            return DecisionTreeNode(node2.constraint_id,high,low)

        if isinstance(node1,DecisionTreeNode) and isinstance(node2,LeafNode):
            high = self._apply(node1.high,node2, operation)
            low = self._apply(node1.low,node2, operation)
            return DecisionTreeNode(node1.constraint_id,high,low)

        if isinstance(node1, DecisionTreeNode) and isinstance(node2, DecisionTreeNode):
            if node1.constraint_id == node2.constraint_id:
                high = self._apply(node1.high, node2.high, operation)
                low = self._apply(node1.low, node2.low, operation)
                return DecisionTreeNode(node1.constraint_id,high, low )
            elif node1.constraint_id > node2.constraint_id:
                # Create a new node with the id of node1 and process node1's children
                high = self._apply(node1.high, node2, operation)
                low = self._apply(node1.low, node2, operation)
                return DecisionTreeNode(node1.constraint_id,high, low )
            else:
                # Create a new node with the id of node2 and process node2's children
                high = self._apply(node1, node2.high, operation)
                low = self._apply(node1, node2.low, operation)
                return DecisionTreeNode(node2.constraint_id,high, low )

        return None

    def print_tree(self):
        self._print_node(self.root, level=0)

    def _print_node(self, node, level):
        indent = "  " * level
        if node is None:
            print(f"{indent}None")
            return
        if isinstance(node,LeafNode):
            print(f"{indent}Leaf(value={node})")
        elif isinstance(node, DecisionTreeNode):
            print(f"{indent}DecisionTreeNode(Condition ID: {node.constraint_id})")
            print(f"{indent}  High:")
            self._print_node(node.high, level + 1)
            print(f"{indent}  Low:")
            self._print_node(node.low, level + 1)
