
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
        new_tree = self.create_tree()
        new_tree.root = self._apply(self.root, other_tree.root, operation)
        return new_tree

    def create_tree(self):
        """
        Factory method to create a new tree of the correct type.
        Should be overridden in subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def _apply(self, node1, node2, operation):
        if node1 is None or node2 is None:
            return None

        if isinstance(node1, LeafNode) and isinstance(node2, LeafNode):
            new_value = operation(node1.value, node2.value)
            return LeafNode(new_value)

        if isinstance(node1, LeafNode) and isinstance(node2, DecisionTreeNode):
            high = self._apply(node1, node2.high, operation)
            low = self._apply(node1, node2.low, operation)
            return self.create_node(node2.constraint_id, high, low)

        if isinstance(node1, DecisionTreeNode) and isinstance(node2, LeafNode):
            high = self._apply(node1.high, node2, operation)
            low = self._apply(node1.low, node2, operation)
            return self.create_node(node1.constraint_id, high, low)

        if isinstance(node1, DecisionTreeNode) and isinstance(node2, DecisionTreeNode):
            if node1.constraint_id == node2.constraint_id:
                high = self._apply(node1.high, node2.high, operation)
                low = self._apply(node1.low, node2.low, operation)
                return self.create_node(node1.constraint_id, high, low)
            elif node1.constraint_id > node2.constraint_id:
                high = self._apply(node1.high, node2, operation)
                low = self._apply(node1.low, node2, operation)
                return self.create_node(node1.constraint_id, high, low)
            else:
                high = self._apply(node1, node2.high, operation)
                low = self._apply(node1, node2.low, operation)
                return self.create_node(node2.constraint_id, high, low)

        return None

    def create_node(self, constraint_id, high, low):
        """
        Factory method to create a new node of the correct type.
        Should be overridden in subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def create_leaf(self, value):
        """
        Factory method to create a new leaf of the correct type.
        Should be overridden in subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")

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
