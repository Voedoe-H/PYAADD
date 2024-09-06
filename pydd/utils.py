from pydd.affine_form import *
from pydd.decisiondiagram import *

def multiply_aadd_bdda(aadd, bdda):
    """
    Multiply an AADD with a BDDA using the generalized apply function.
    
    :param aadd: An instance of AADD.
    :param bdda: An instance of BDDA.
    :return: A new AADD resulting from the multiplication.
    """
    def multiply_affine_with_boolean(affine_form, boolean_value):
        if boolean_value:
            return affine_form
        else:
            return AffineForm(constant=0, noise_coeffs={})

    return DecisionTree.apply(aadd, bdda, multiply_affine_with_boolean)
