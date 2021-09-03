"""Test Genetics IO Operations."""
import os

import numpy as np

from among_us.const import ORIGINAL_GENOME
from among_us.genetics import (
    POOR_VARIANT_FILE_NAME,
    add_poor_variants,
    get_poor_variants,
)

from . import POOR_VARIANTS


def test_save_poor_variants_append():
    """Test saving poor variants."""

    # Clear file
    test_file_name = "test.out"
    open(test_file_name, "w").close()

    # Save Multiple Rows
    test_file = open(test_file_name, "a")
    np.savetxt(test_file, POOR_VARIANTS, fmt="%.0f", delimiter=",")
    test_file.close()

    # Save single record
    test_file = open(test_file_name, "a")
    np.savetxt(test_file, [POOR_VARIANTS[0]], fmt="%.0f", delimiter=",")
    np.savetxt(test_file, [POOR_VARIANTS[0]], fmt="%.0f", delimiter=",")
    np.savetxt(test_file, [POOR_VARIANTS[0]], fmt="%.0f", delimiter=",")
    np.savetxt(test_file, [POOR_VARIANTS[0]], fmt="%.0f", delimiter=",")
    np.savetxt(test_file, [POOR_VARIANTS[0]], fmt="%.0f", delimiter=",")
    test_file.close()

    poor_variants = np.loadtxt("test.out", dtype="int64", delimiter=",")
    assert len(poor_variants) == 24

    # Cleanup
    os.remove(test_file_name)


def test_load_poor_variants():
    """Test loading poor variants."""

    # Setup test file
    test_file_name = "test.out"
    test_file = open(test_file_name, "w")
    np.savetxt(test_file, POOR_VARIANTS, fmt="%.0f", delimiter=",")
    test_file.close()

    poor_variants = np.loadtxt("test.out", dtype="int64", delimiter=",")

    assert len(poor_variants) == 19

    os.remove(test_file_name)


def test_get_poor_variants():
    """Test get poor variants."""

    # Setup test file
    test_file = open(POOR_VARIANT_FILE_NAME, "w")
    np.savetxt(test_file, POOR_VARIANTS, fmt="%.0f", delimiter=",")
    test_file.close()

    poor_variants = get_poor_variants()

    assert len(poor_variants) == 19

    # Cleanup
    os.remove(POOR_VARIANT_FILE_NAME)


def test_add_poor_variants():
    """Test adding poor variants."""

    pop_fits = np.empty((0, 44))

    test_genome = np.array(ORIGINAL_GENOME)
    pop_fit = np.append(test_genome, 0)

    pop_fits = np.vstack((pop_fits, pop_fit))

    poor_variants = add_poor_variants(POOR_VARIANTS, pop_fits)

    assert len(poor_variants) == 20

    # Cleanup
    os.remove(POOR_VARIANT_FILE_NAME)
