#from .builder import Builder

import importlib

class AffineForm:
    def __init__(self, constant: float, noise_symbols: dict, builder):
        """
        Initializes an AffineForm.

        :param constant: The constant term (x0).
        :param noise_symbols: Dictionary {noise_symbol: coefficient}.
        :param builder: The builder (context) this affine form belongs to.
        """
        self.constant = constant
        self.noise_symbols = noise_symbols
        self.builder = builder  # Reference to the builder (context)

    def __add__(self, other):
        """
        Adds two affine forms, ensuring they belong to the same context (builder).
        
        :param other: Another AffineForm instance.
        :return: A new AffineForm with the combined constant and noise symbols.
        :raises ValueError: If the affine forms belong to different contexts.
        """
        if self.builder is not other.builder:
            raise ValueError("Cannot add affine forms from different contexts (builders).")

        new_constant = self.constant + other.constant
        new_noise_symbols = self.noise_symbols.copy()

        # Combine the noise symbols without introducing new ones
        for key, value in other.noise_symbols.items():
            if key in new_noise_symbols:
                new_noise_symbols[key] += value
            else:
                new_noise_symbols[key] = value

        return self.builder.create_affine_form(new_constant, new_noise_symbols)

    def __sub__(self, other):
        """
        Subtracts one affine form from another, ensuring they belong to the same context (builder).
        
        :param other: Another AffineForm instance.
        :return: A new AffineForm with the subtracted constant and noise symbols.
        :raises ValueError: If the affine forms belong to different contexts.
        """
        if self.builder is not other.builder:
            raise ValueError("Cannot subtract affine forms from different contexts (builders).")

        new_constant = self.constant - other.constant
        new_noise_symbols = self.noise_symbols.copy()

        # Combine the noise symbols without introducing new ones
        for key, value in other.noise_symbols.items():
            if key in new_noise_symbols:
                new_noise_symbols[key] -= value
            else:
                new_noise_symbols[key] = -value

        return self.builder.create_affine_form(new_constant, new_noise_symbols)

    def __mul__(self, other):
        """
        Multiplies two affine forms or an affine form by a scalar.
        
        :param other: Either a scalar (float) or another AffineForm instance.
        :return: A new AffineForm representing the result of the multiplication.
        :raises ValueError: If affine forms from different contexts are multiplied.
        """
        # Scalar multiplication
        if isinstance(other, (int, float)):
            new_constant = self.constant * other
            new_noise_symbols = {k: v * other for k, v in self.noise_symbols.items()}
            return self.builder.create_affine_form(new_constant, new_noise_symbols)

        # Affine form multiplication
        if isinstance(other, AffineForm):
            if self.builder is not other.builder:
                raise ValueError("Cannot multiply affine forms from different contexts (builders).")

            # New constant: product of the constants
            new_constant = self.constant * other.constant

            # Cross terms between constants and noise symbols
            new_noise_symbols = {}

            # Add constant * other noise terms
            for key, value in other.noise_symbols.items():
                new_noise_symbols[key] = self.constant * value

            # Add other.constant * self noise terms
            for key, value in self.noise_symbols.items():
                if key in new_noise_symbols:
                    new_noise_symbols[key] += other.constant * value
                else:
                    new_noise_symbols[key] = other.constant * value

            # Add noise noise products, introducing new noise symbols
            for key1, value1 in self.noise_symbols.items():
                for key2, value2 in other.noise_symbols.items():
                    if key1 == key2:
                        # Handle same noise symbols (add square term, potentially tracked separately)
                        new_key = key1
                        if new_key in new_noise_symbols:
                            new_noise_symbols[new_key] += value1 * value2
                        else:
                            new_noise_symbols[new_key] = value1 * value2
                    else:
                        # Handle cross terms with new noise symbol
                        new_key = self.builder.create_noise_symbol()  # New unique noise symbol
                        new_noise_symbols[new_key] = value1 * value2

            return self.builder.create_affine_form(new_constant, new_noise_symbols)

        return NotImplemented

    

    def __repr__(self):
        return f"AffineForm({self.constant}, {self.noise_symbols}, Context: {id(self.builder)})"
