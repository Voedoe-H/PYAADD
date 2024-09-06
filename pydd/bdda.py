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
        """
        """
        self.root = node

    def apply(self, other_bdda, operation):
        """
        """
        new_bdda = BDDA(self.builder)
        new_bdda.root = self._apply(self.root, other_bdda.root, operation)
        return new_bdda

    def _apply(self, node1,node2,operation):
        """
        """
        if node1 is None and node2 is None:
            return None
        if node1 is None:
            # Process node2 down the tree
            return self._apply(node2, node1, operation)
        if node2 is None:
            # Process node1 down the tree
            return self._apply(node1, node2, operation)

        if isinstance(node1, BDDALeafNode) and isinstance(node2, BDDALeafNode):
           
            new_affine_form = operation(node1.value, node2.value)
            #new_affine_form_id = self.builder.create_affine_form(new_affine_form.constant, new_affine_form.noise_coeffs)
            return BDDALeafNode(new_affine_form)
        
        if isinstance(node1, BDDALeafNode) and isinstance(node2,BDDANode):
            high = self._apply(node1,node2.high, operation)
            low = self._apply(node1,node2.low, operation)
            return BDDANode(node2.constraint_id,high,low)

        if isinstance(node1,BDDANode) and isinstance(node2,BDDALeafNode):
            high = self._apply(node1.high,node2, operation)
            low = self._apply(node1.low,node2, operation)
            return BDDANode(node1.constraint_id,high,low)

        if isinstance(node1, BDDANode) and isinstance(node2, BDDANode):
            if node1.constraint_id == node2.constraint_id:
                high = self._apply(node1.high, node2.high, operation)
                low = self._apply(node1.low, node2.low, operation)
                return BDDANode(node1.constraint_id,high, low )
            elif node1.constraint_id > node2.constraint_id:
                # Create a new node with the id of node1 and process node1's children
                high = self._apply(node1.high, node2, operation)
                low = self._apply(node1.low, node2, operation)
                return BDDANode(node1.constraint_id,high, low )
            else:
                # Create a new node with the id of node2 and process node2's children
                high = self._apply(node1, node2.high, operation)
                low = self._apply(node1, node2.low, operation)
                return BDDANode(node2.constraint_id,high, low )

        return None

    def print_tree(self):
        """
        """
        self._print_node(self.root, level=0)

    def _print_node(self, node, level):
        """
        """
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