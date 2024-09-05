from .builder import Builder

class BDDANode:
    def __init__(self, condition_affine_form_id: int, left=None, right=None):
        self.condition_affine_form_id = condition_affine_form_id
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BDDA Node(Condition ID: {self.condition_affine_form_id}, Left: {self.left}, Right: {self.right})"

class BDDA:
    def __init__(self, builder: Builder):
        self.builder = builder
        self.root = None

    def insert(self, affine_form_id: int, left_value: bool, right_value: bool):
        self.root = BDDANode(affine_form_id, left_value, right_value)

    def evaluate(self, x: dict):
        return self._evaluate_node(self.root, x)

    def _evaluate_node(self, node, x):
        if isinstance(node, bool):
            return node  # Leaf reached, return boolean value
        condition_affine_form = self.builder.get_affine_form(node.condition_affine_form_id)
        if condition_affine_form.evaluate(x) <= 0:
            return self._evaluate_node(node.left, x)
        else:
            return self._evaluate_node(node.right, x)

    def __repr__(self):
        return f"BDDA(Root: {self.root})"
