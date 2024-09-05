import pytest
from pydd.builder import Builder

def test_addition_of_affine_forms_same_context():
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
    builder = Builder()

    affine1 = builder.create_affine_form(2.0, {'epsilon1': 1.0})
    affine2 = builder.create_affine_form(3.0, {'epsilon1': 0.5})


    result = affine2 - affine1
    assert result.constant == 1.0
    assert result.noise_symbols['epsilon1'] == -0.5

def test_addition_of_affine_forms_different_contexts_raises_error():
    builder1 = Builder()
    builder2 = Builder()

    # Create affine forms in two different contexts
    affine1 = builder1.create_affine_form(2.0, {'epsilon1': 1.0})
    affine2 = builder2.create_affine_form(3.0, {'epsilon2': 1.5})


    # Check that an error is raised when adding affine forms from different contexts
    with pytest.raises(ValueError, match="Cannot add affine forms from different contexts"):
        result = affine1 + affine2

