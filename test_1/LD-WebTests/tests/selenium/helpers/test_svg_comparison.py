import cairosvg
import pytest

from helpers.extraction import paths
from helpers.verification.grid import verify_png


def test_svg_comparison(selenium):
    """
    Testing the verify_png function to check if it actually works.
    Tests for anti-aliasing handling image similarity checks.
    :param selenium: selenium webdriver
    """
    # Same compound pairs
    exact1_png = _get_png_from_svg('CustomAlignment1.svg')
    # This svg is not an exact copy of the previous svg; it instead should produce an exact
    # pixel to pixel match when converted to png formatted bytes and extracting the pixel data
    exact2_png = _get_png_from_svg('CustomAlignment1_helper_test.svg')
    similar1_png = _get_png_from_svg('CustomAlignment2.svg')
    # The derived pixel data of this svg is only similar to the previous svg's, rather than exact,
    # though the images should still appear identical to the human eye. This is due to anti-aliasing.
    similar2_png = _get_png_from_svg('CustomAlignment2_helper_test.svg')

    # Different compound pairs
    # Will be compared with similar1_png above
    different_png = _get_png_from_svg('CustomAlignment3.svg')
    # These are two different compounds, differing only by a single bond, and aligned exactly the same.
    single_bond_png = _get_png_from_svg('single_bond_helper_test.svg')
    double_bond_png = _get_png_from_svg('double_bond_helper_test.svg')
    # These small compounds differ only by a single point: the presence of a radical.
    small_non_radical_png = _get_png_from_svg('small_non_radical_helper_test.svg')
    small_radical_png = _get_png_from_svg('small_radical_helper_test.svg')
    # These large compounds differ only by a single point: the presence of a radical.
    non_radical_png = _get_png_from_svg('non_radical_helper_test.svg')
    radical_png = _get_png_from_svg('radical_helper_test.svg')
    # These two only differ by color. The differently colored compound was generated using a SAR scaffold.
    color_png = _get_png_from_svg('color_helper_test.svg')
    no_color_png = _get_png_from_svg('no_color_helper_test.svg')

    # Testing verify_png helper for exact similarity, anti-aliasing accounted for
    # There is no entity_id available, so we pass random strings as the entity_id argument
    verify_png(selenium, exact1_png, exact2_png, 'exact_pngs')
    verify_png(selenium, similar1_png, similar2_png, 'similar_pngs')

    ###### Testing verify_png helper to ensure that very similar but still different compounds are rejected ######
    with pytest.raises(AssertionError):
        # NOTE These compound images are very similar but still different (one has an -OH, the other a =O),
        # yet they produce a low similarity. This is because the compounds are slightly translated.
        verify_png(selenium, similar1_png, different_png, 'similar_and_different_pngs')

    with pytest.raises(AssertionError):
        # NOTE These compound images are identical except that one has a double bond instead of a single in one place
        verify_png(selenium, single_bond_png, double_bond_png, 'single_and_double_bond_pngs')

    with pytest.raises(AssertionError):
        # NOTE These compounds are identical except for color. One is a regular compound, the other a SAR scaffold.
        verify_png(selenium, color_png, no_color_png, 'color_and_no_color_pngs')

    with pytest.raises(AssertionError):
        # NOTE These small compounds are identical except for the presence or lack of a single radical.
        # This is a hard test to pass
        verify_png(selenium, small_non_radical_png, small_radical_png, 'small_non_radical_and_small_radical_pngs')

    with pytest.raises(AssertionError):
        # NOTE These large compounds are identical except for the presence or lack of a single radical.
        # This is the toughest test to pass
        verify_png(selenium, non_radical_png, radical_png, 'non_radical_and_radical_pngs')


def _get_png_from_svg(filename):
    full_file_path = paths.get_resource_path(filename)
    return cairosvg.svg2png(url=full_file_path)
