import pytest
from pydd.builder import Builder


@pytest.fixture
def setup_affine_forms():
    """
    Simple test to check if affine forms are being created
    """
    builder = Builder()

    af1 = builder.create_affine_form(2, {1: 3.0, 2: -1.5})
    af2 = builder.create_affine_form(1.5, {2: 2.5, 3: -4.0})

    builder_other = Builder()
    af_other = builder_other.create_affine_form(1, {1: 2.0})

    return af1, af2, af_other, builder

def test_addition_of_affine_forms_same_context():
    """
    Test to make sure that the addition of affine forms works as expected
    """
    builder = Builder()

    # Create two affine forms in the same context (builder)
    affine1 = builder.create_affine_form(2.0, {'epsilon1': 1.0})
    affine2 = builder.create_affine_form(3.0, {'epsilon1': 0.5})

    # Perform the addition
    result = affine1 + affine2

    # Assert the expected result
    assert result.constant == 5.0
    assert result.noise_symbols['epsilon1'] == 1.5

def test_subtraction_of_affine_forms_same_context():
    """
    Test to make sure that the subtraction works as expected
    """
    builder = Builder()

    affine1 = builder.create_affine_form(2.0, {'epsilon1': 1.0})
    affine2 = builder.create_affine_form(3.0, {'epsilon1': 0.5})


    result = affine2 - affine1
    assert result.constant == 1.0
    assert result.noise_symbols['epsilon1'] == -0.5

def test_addition_of_affine_forms_different_contexts_raises_error():
    """
    Test to make sure that two affine forms of different context to not add with each other
    """
    builder1 = Builder()
    builder2 = Builder()

    # Create affine forms in two different contexts
    affine1 = builder1.create_affine_form(2.0, {'epsilon1': 1.0})
    affine2 = builder2.create_affine_form(3.0, {'epsilon2': 1.5})


    # Check that an error is raised when adding affine forms from different contexts
    with pytest.raises(ValueError, match="Cannot add affine forms from different contexts"):
        result = affine1 + affine2

def test_scalar_multiplication(setup_affine_forms):
    """
    Test multiplying an affine form by a scalar.
    """
    af1, _, _, _ = setup_affine_forms
    result = af1 * 2.0

    expected_constant = 4  # 2 * 2.0
    expected_noise_symbols = {1: 6.0, 2: -3.0}  # All noise coefficients scaled by 2.0

    assert result.constant == expected_constant
    assert result.noise_symbols == expected_noise_symbols

def test_affine_multiplication_same_context(setup_affine_forms):
    """
    Test multiplying two affine forms from the same context.
    """
    af1, af2, _, _ = setup_affine_forms
    result = af1 * af2

    expected_constant = 3.0  # 2 * 1.5

    # Expected noise symbols from constant * noise terms:
    expected_noise_symbols = {
        1: 3.0,   # af1.constant * af2.noise_symbol(1)
        2: 2.75,  # Combination of both af1 and af2 noise symbols: 3.0 * 2.5 + (-1.5) * 2.0
        3: -8.0   # af1.noise_symbol(3) = 0, af2.noise_symbol(3) = -4.0 -> 2 * -4.0
    }

    assert result.constant == expected_constant
    assert result.noise_symbols == expected_noise_symbols

def test_affine_multiplication_different_context(setup_affine_forms):
    """
    Test multiplying two affine forms from different contexts.
    Expect a ValueError to be raised.
    """
    af1, _, af_other, _ = setup_affine_forms
    with pytest.raises(ValueError, match="Cannot multiply affine forms from different contexts"):
        _ = af1 * af_other
