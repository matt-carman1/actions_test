from helpers.selection.grid import GRID_LIVEREPORT_COLUMNS_IMAGE_PATH
from library import dom
from library.eventually import eventually_equal


def verify_compound_structure_image_count_on_formula_column(driver, expected_compounds):
    """
    Verifies the count of compound_structure image tags on a grid in a web page.

    :param driver: The web driver instance
    :type driver: WebDriver
    :param expected_compounds: The expected count of image tags.
    :type expected_compounds:
    :return: None
    :rtype: None

    """

    def get_compounds_structure_image_tags(driver):
        """
        Retrieves the count of image tags on the grid.
        :param driver: The web driver instance.
        :type driver: WebDriver
        :return: The count of image tags on the grid.
        :rtype: int
        """
        images_element = dom.get_elements(driver, GRID_LIVEREPORT_COLUMNS_IMAGE_PATH)
        image = [dom.get_element(element, selector="[class='structure-image']") for element in images_element]
        return len(image)

    assert eventually_equal(driver, get_compounds_structure_image_tags, expected_compounds), \
        "Expected {} compound images on the grid, but found {}.".format(expected_compounds,
                                                                        get_compounds_structure_image_tags(driver))
