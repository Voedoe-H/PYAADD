from .builder import Builder


class BDDALeafNode:
    """
    """
    
    def __init__(self,boolean):
        self.value = boolean

    def __repr__(self):
        return f"Leaf(value={self.value})"


class BDDANode:
    """
    """
    def __init__(self, constraint_id: int, high=None, low=None):
        self.constraint_id = constraint_id
        self.high = high
        self.low = low

    def __repr__(self):
        return f"BDDA Node(Condition ID: {self.condition_affine_form_id}, Left: {self.left}, Right: {self.right})"

class BDDA:
    """
    
    """

    def __init__(self, builder: Builder):
        self.builder = builder
        self.root = None

    def build(self,node):
        self.root = node



    def print_tree(self):
        self._print_node(self.root, level=0)

    def _print_node(self, node, level):
        indent = " " * level
        if node is None:
            print(f"{indent}None")
            return
        if isinstance(node, BDDALeafNode):
            print(f"{indent}Leaf(value={node.value})")
        elif isinstance(node,BDDANode):
            print(f"{indent}BDDANode(Condition ID: {node.constraint_id})")
            print(f"{indent} Left:")
            self._print_node(node.high, level + 1)
            print(f"{indent} Right:")
            self._print_node(node.low, level + 1)