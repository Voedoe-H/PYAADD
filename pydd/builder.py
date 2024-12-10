from .affine_form import AffineForm


class Builder:
    
    def __init__(self):
        """
        Constraint is interpreted as x <= 0 where x is the affine form of the constraint
        """
        self.id_counter = 0
        self.noise_symbol_counter = 200000
        self.constraints = {} # Disctionary to store the constraints that exist in the builders context. (key: constraint_id, value: affine form)
        self.noise_symbols = {}  # Dictionary to store unique noise symbols (key: symbol name, value: coefficient)

    def create_affine_form(self, constant: float, noise_coeffs: dict) -> AffineForm:
        """
        Creates an AffineForm without adding it as a constraint.
        
        :param constant: Constant term for the affine form.
        :param noise_coeffs: Dictionary of noise symbol coefficients.
        :return: Created AffineForm instance.
        """
        affine_form = AffineForm(constant, noise_coeffs, self)
        # Register noise symbols
        self.register_noise_symbols(noise_coeffs)
        return affine_form

    def add_constraint(self, affine_form: AffineForm) -> int:
        """
        Adds an AffineForm to the builder's constraints and returns its ID.

        :param affine_form: AffineForm instance to be added as a constraint.
        :return: Unique ID of the added constraint.
        """
        
        constraint_id = self.id_counter
        self.id_counter+=1  # New unique ID
        self.constraints[constraint_id] = affine_form
        return constraint_id

    def get_constraint(self, constraint_id: int) -> AffineForm:
        """
        Retrieves an AffineForm by its ID.

        :param constraint_id: ID of the constraint.
        :return: AffineForm instance.
        """
        return self.constraints.get(constraint_id, None)

    def register_noise_symbols(self, noise_coeffs: dict):
        """
        Registers noise symbols from the given coefficients.

        :param noise_coeffs: Dictionary of noise symbol coefficients.
        """
        for symbol in noise_coeffs.keys():
            if symbol not in self.noise_symbols:
                self.noise_symbols[symbol] = True  

    def ensure_unique_noise_symbol(self, symbol_id: str):
        """
        Ensures the noise symbol is unique, throws an error if it's not.

        :param symbol_id: ID of the noise symbol.
        :raises ValueError: If the noise symbol already exists.
        """
        if symbol_id in self.noise_symbols:
            raise ValueError(f"Noise symbol '{symbol_id}' already exists.")
        else:
            self.noise_symbols[symbol_id] = 0  # Initialize with a default coefficient (0)

    def addBddmul(self,aadd,bdd):
        
        pass

    def __repr__(self):
        return f"AffineFormBuilder(Constraints: {self.constraints}, Noise Symbols: {self.noise_symbols})"

