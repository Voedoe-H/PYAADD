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

        return AffineForm(new_constant, new_noise_symbols, self.builder)

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

        return AffineForm(new_constant, new_noise_symbols, self.builder)

    def __repr__(self):
        return f"AffineForm({self.constant}, {self.noise_symbols}, Context: {id(self.builder)})"
