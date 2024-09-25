"""
Verify the state of the grid.
"""
import tempfile
from io import BytesIO

import cairosvg
import requests
from PIL import Image, ImageChops, ImageStat

from helpers.change.grid_row_actions import open_row_menu
from helpers.extraction import paths
from helpers.extraction.grid import find_column_contents, get_grid_metadata, get_grid_render_count_map, \
    calculate_scroll_distance, find_column_subcell_contents
from helpers.selection.column_tree import LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN
from helpers.selection.general import OPENED_MENU_ITEMS
from helpers.selection.grid import (
    GRID_COMPOUND_IMAGE_SELECTOR_, GRID_HEADER_ALIGNMENT_TEXT, GRID_FIXED_COLUMN_GROUP, GRID_ROW_CHECKBOX_INPUT,
    GRID_ROW_MENU, SELECTED_ID, ROW_INDEX, GRID_PROGRESS_NOTIFICATION, GRID_HEADER_CELL, GRID_ROWS_CONTAINER, GRID_ROW,
    GRID_ROW_CHECKBOX_, GRID_ROW_ID_HOVERED_, GRID_HEADER_TOP, GRID_TIP_NOTIFICATION, GRID_FIND_INPUT,
    GRID_FIND_MATCH_COUNT, GRID_FIND_PREV_BUTTON, GRID_FIND_NEXT_BUTTON, GRID_FIND_CLOSE_BUTTON, GRID_FIND_ORANGE_MARK,
    GRID_FIND_YELLOW_MARK, GRID_FIND_TOTAL_MATCHES, GRID_FOOTER, GRID_ERROR_NOTIFICATION, GRID_INFO_NOTIFICATION)
from helpers.selection.live_report_tab import TAB_ACTIVE
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from library import wait, dom
from library.dom import LiveDesignWebException
from library.eventually import eventually_equal, eventually
from library.scroll import wheel_element, wheel_to_bottom
from library.utils import element_is_vertically_within_parent, get_current_test_name, is_chrome, is_firefox

COMPOUND_STRUCTURE_COLUMN_NAME = 'Compound Structure'


def verify_grid_contents(driver, contents, inexact_match_columns=[COMPOUND_STRUCTURE_COLUMN_NAME]):
    """
    Verify that the contents of the grid matches what is expected. Expected
    state is passed in as a dict of lists, for example:

            verify_grid_contents(driver, {
                'Compound Structure': [smiles1, smiles2],
                column_name: ['231.5', '192.7']
            })

    or

            verify_grid_contents(driver, {
                'ID': [ 'CRA-035507', 'CRA-035508', 'CRA-035509',
                        ...<47 other values> ],
                'r_glide_XP_Sitemap (undefined)': ['-0.00246', '-0.528',
                                                   '0.386', ...<47 other values>
                                                  ],
                'Rationale': ['demo: A large Live Report based on the 100 Ideas
                               SDF.'] * 50
            })

    Note that the arrays of values must be the complete, correctly ordered list
    of items for the named column in the grid; the verification will fail if the
    number of items found differs, or if the order of items does not match. It
    is a good idea to explicitly sort the grid on a column before asserting the
    contents.

    :param driver: webdriver
    :param contents: dict of lists specifying grid contents. See examples.
    :param inexact_match_columns: List of column names to NOT test content
        equality on. For the specified columns, we only verify that the cells are
        non-empty.
        NOTE(badlato): The intended use case here is to NOT test if Compound
         structures, etc. are scientifically valid. We leave scientific testing
         to the underlying libraries, and just verify that LD is passing
         *something* along
    """
    for column_name in contents:
        expected_content = contents[column_name]
        exact_match = column_name not in inexact_match_columns
        verify_column_contents(driver, column_name, expected_content, exact_match=exact_match)


def verify_column_contains(driver, column_name, contents, negate=False):
    """
    Verify that a single named column contains all of contents

    :param driver: webdriver
    :param column_name: name of the column
    :type column_name: str
    :param contents: a set of values the column should contain
    :type contents: set
    """

    def get_actual_content(driver):
        return find_column_contents(driver, column_name, False)

    def comparator(actual_content):
        return set(contents).issubset(actual_content)

    assert eventually(driver, get_actual_content, comparator,
                      negate=negate), 'Grid column {} did not contains contents `{}`'.format(column_name, contents)


def verify_column_contents(driver,
                           column_name,
                           expected_content,
                           get_info_from_cell=None,
                           match_length_to_expected=False,
                           exact_match=True):
    """
    Verify the contents of a single named column.

    :param driver: webdriver
    :param column_name: str name of column
    :param expected_content: a list of str values expected in the grid for the
                             named column
    :param get_info_from_cell: optional function that is used to extract data from a cell. If not supplied, we will get
                               the text representation. NOTE: This is ignored for Compound Structure Column.
    :param match_length_to_expected: boolean, if true will only check up to the length of the supplied expected array
    :param exact_match: True if cell contents should match exactly.
        False if cell contents only need to exist, but not match.
        NOTE(badlato): The intended use case here is to not test if SMILES
         strings, etc. are scientifically valid. We leave scientific testing
         to the underlying libraries, and just verify that LD is passing
         *something* along
    """
    if exact_match and column_name == 'Compound Structure':
        print(
            'Warning: Performing exact match on Compound Structure column.  You probably only want to do this for scientific integrity tests!'
        )
    # The following function will be called by eventually_equal many times,
    # until either 1) the return value equals the expected_content, or 2) too
    # much time has elapsed. We are using the default timeout, which is (at the
    # time of writing) 60 seconds.
    def get_actual_content(driver):
        try:
            actual_contents = find_column_contents(driver, column_name, get_info_from_cell)
        except LiveDesignWebException:
            actual_contents = []
        if match_length_to_expected:
            actual_contents = actual_contents[0:len(expected_content)]
        if not exact_match and actual_contents:
            return expected_content
        return actual_contents

    assert eventually_equal(
        driver,
        # Note that we pass get_actual_content *without parentheses*. This means
        # it's not invoked right now, but instead passed as a variable, and
        # called in core/eventually.py when needed.
        get_actual_content,
        expected_content), 'Grid column {} did not have expected contents `{}`.  Had `{}` instead.'.format(
            column_name, expected_content, get_actual_content(driver))


def verify_column_subcell_contents(driver,
                                   column_name,
                                   expected_content,
                                   get_info_from_subcell=None,
                                   match_length_to_expected=False):
    """
    Verify the contents of a single named column.

    :param driver: webdriver
    :param column_name: str name of column
    :param expected_content: a list of str values expected in the grid for the
                             named column
    :param get_info_from_subcell: optional function that is used to extract data from a subcell. If not supplied, we
                                  will get the text representation. NOTE: This is ignored for Compound Structure Column.
    :param match_length_to_expected: boolean, if true will only check up to the length of the supplied expected array
    """

    # The following function will be called by eventually_equal many times,
    # until either 1) the return value equals the expected_content, or 2) too
    # much time has elapsed. We are using the default timeout, which is (at the
    # time of writing) 60 seconds.
    def get_actual_content(driver):
        actual_contents = find_column_subcell_contents(driver, column_name, get_info_from_subcell)
        if match_length_to_expected:
            actual_contents = actual_contents[0:len(expected_content)]
        return actual_contents

    assert eventually_equal(
        driver,
        # Note that we pass get_actual_content *without parentheses*. This means
        # it's not invoked right now, but instead passed as a variable, and
        # called in core/eventually.py when needed.
        get_actual_content,
        expected_content), 'Grid column {} did not have expected subcell contents `{}`'.format(
            column_name, expected_content)


def verify_footer_values(driver, expected_grid_metadata):
    # TODO: putting column count as None generally it is 6 for a new LR and
    # will never be Zero in a new LR
    """
    Function to check footer values of LR.
    :param driver: Selenium WebDriver
    :param expected_grid_metadata: Dictionary containing expected values. You
    may pass the dictionary in the following format:
        {
        'row_all_count': '10 Total Compounds',
        'row_hidden_count': '1 Hidden',
        'row_filtered_count': '2 After Filter',
        'row_selected_count': '1 Selected',
        'column_all_count': '4 Columns',
        'column_hidden_count': '2 Hidden'
        }
    Note: It not required to pass all the values in the dictionary.
    Pass only the ones that you intend to verify. This will give you an error if
    any of the key is not visible in the footer but you still pass it while
    calling this function. For e.g "After Filter" and "Hidden" doesn't show
    up in the footer unless there is a similar action performed as the name
    say.
    :return:
    """
    wait.until_visible(driver, GRID_FOOTER)

    # TODO (mulvaney) Note: This should work but is too clever:
    # def compare_metadata(actual_metadata):
    #     return all(item in actual_metadata.items() for item in
    #         expected_grid_metadata.items())
    #
    # assert eventually(driver, get_grid_metadata, compare_metadata)

    for (metadata_key, expected_value) in expected_grid_metadata.items():
        # create a variable to store actual count
        actual_count = None

        def get_count(driver_):
            nonlocal actual_count
            actual_count = get_grid_metadata(driver_).get(metadata_key, "None")
            # "None" so we can verify when values are *not* present
            return actual_count

        # TODO (mulvaney): Modify or get rid of eventually_equal
        # Generate the assertion message using 'actual_count' value rather than recalling get_count(driver)
        # because LD may update and show a different number, resulting in an unexpected error message
        assert eventually_equal(driver, get_count, expected_value), \
            "{} differs: Expected '{}' " \
            "but got '{}'".format(metadata_key,
                                  expected_value,
                                  actual_count)


def check_for_butterbar(driver, notification_text, visible=True):
    """
    Check for the butter appearance or disappearance.
    This would wait for the butter bar with a the provided notification_text
    :param driver: Selenium Webdriver
    :param notification_text: The text that appears in the butterbar
    :param visible: Default is True as we check for appearance for butterbar
                    but when we want to check if it has disappeared then
                    explicitly set it to False.
    :return:
    """
    if visible:
        wait.until_visible(driver, GRID_PROGRESS_NOTIFICATION, notification_text)
    else:
        wait.until_not_visible(driver, GRID_PROGRESS_NOTIFICATION, notification_text)


def check_for_info_butterbar(driver, notification_text, visible=True):
    """
    Check for the info butter appearance or disappearance.
    This butterbar shows up whenever comments are added or edited.
    This would wait for the butter bar with a the provided notification_text
    :param driver: Selenium Webdriver
    :param notification_text: The text that appears in the butterbar
    :param visible: Default is True as we check for appearance for butterbar
                    but when we want to check if it has disappeared then
                    explicitly set it to False.
    :return:
    """
    if visible:
        wait.until_visible(driver, GRID_INFO_NOTIFICATION, notification_text)
    else:
        wait.until_not_visible(driver, GRID_INFO_NOTIFICATION, notification_text)


def check_for_baconbar(driver, notification_text, visible=True):
    """
    Check for the bacon bar appearance or disappearance.
    This would wait for the bacon bar with the provided notification_text
    :param driver: Selenium Webdriver
    :param notification_text: The text that appears in the bacon bar
    :param visible: Default is True as we check for appearance for bacon bar
                    but when we want to check if it has disappeared then
                    explicitly set it to False.
    :return:
    """
    if visible:
        wait.until_visible(driver, GRID_ERROR_NOTIFICATION, notification_text)
    else:
        wait.until_not_visible(driver, GRID_ERROR_NOTIFICATION, notification_text)


def check_for_notification_tip(driver, tip_text, visible=True):
    """
    Check for the notification tip bar's appearance or disappearance.
    This would wait for the bar with a the provided tip_text

    :param driver: Selenium Webdriver
    :param tip_text: The text that appears in the notification tip
    :param visible: True to wait for presence of notification tip bar,
                    False to wait for the bar to disappear.
                    Default is True.
    :return:
    """
    if visible:
        wait.until_visible(driver, GRID_TIP_NOTIFICATION, tip_text)
    else:
        wait.until_not_visible(driver, GRID_TIP_NOTIFICATION, tip_text)


def verify_columns_not_visible(driver, columns):
    """
    Verify that each column is hidden.

    :param driver: webdriver
    :param columns: list of column names
    """
    for column_name in columns:
        verify_is_not_visible(driver, GRID_HEADER_CELL, column_name)


def verify_header_has_aligned(driver):
    """
    Verify that the Compound Structure column header has the (Aligned) text

    :param driver: webdriver
    """
    verify_is_visible(driver, GRID_HEADER_CELL + '[title="Compound Structure"] ' + GRID_HEADER_ALIGNMENT_TEXT)


def verify_svg(driver, entity_id, expected_file_name):
    """
    Verify that the expected compound image svg matches the actual svg in the grid.

    :param driver: webdriver
    :param entity_id: str entity id
    :param expected_file_name: str file name of the expected compound image
    """
    if not expected_file_name.endswith('.svg'):
        assert False, 'Please provide an svg file'

    expected_path = paths.get_resource_path(expected_file_name)
    # Convert the svgs to pngs
    expected_png = cairosvg.svg2png(url=expected_path)
    actual_png = _get_actual_png(driver, entity_id)

    verify_png(driver, expected_png, actual_png, entity_id)


def verify_png(driver, expected_png, actual_png, entity_id):
    """
    Verify that the actual png's similarity to the expected png is at or below the RMS (root mean square) threshold.
    NOTE: The threshold was determined experimentally, due to the nature of image comparison (there is no catch-all
        algorithm, because the way in which images are determined to be different matters - it is subjective by nature)
        However, in this case, the threshold of 1 might make sense if you think of a compound differing only by a
        radical (a dot) as being different by 1 pixel (e.g. a pixel difference of 255). Look at the ImageStat.Stat
        code to see where 255 is used (you'll see 256 since it's used by range()), etc.

    :param driver: selenium webdriver
    :param expected_png: bytes, expected png formatted bytes string
    :param actual_png: bytes, actual png formatted bytes string
    :param entity_id: str entity id
    """
    rms_threshold = 1
    expected_im = Image.open(BytesIO(expected_png))
    actual_im = Image.open(BytesIO(actual_png))

    # The histogram is returned as a list of pixel counts, one for each pixel value in the source image. If the image
    # has more than one band, the histograms for all bands are concatenated (for example, the histogram for an “RGBA”
    # image contains 1024 values)
    # Ex: [count r == 0, count r == 1, ..., count r = 255, count g == 0, count g == 1, ...],  length 1024 (256 * 4)
    histogram = ImageChops.difference(expected_im, actual_im).histogram()

    # This gives us a list of the RMS of each band (r,g,b, and a) in the image.
    rgba_rms = ImageStat.Stat(histogram).rms
    # Check if any rgba band's RMS is above the RMS threshold (standard deviation)
    is_below_threshold = not any((band > rms_threshold for band in rgba_rms))

    if not is_below_threshold:
        test_name = get_current_test_name()
        browser = ''
        if is_chrome(driver):
            browser = 'Chrome'
        elif is_firefox(driver):
            browser = 'Firefox'
        with open("{}_expected_compound_{}_{}.png".format(test_name, entity_id, browser),
                  'wb') as expected_image, open("{}_actual_compound_{}_{}.png".format(test_name, entity_id, browser),
                                                'wb') as actual_image:
            expected_image.write(expected_png)
            actual_image.write(actual_png)

    assert is_below_threshold, 'Standard deviation {} of the images was above the threshold of {}' \
        .format(rgba_rms, rms_threshold)


def _get_actual_png(driver, entity_id):
    """
    Helper to get the actual compound image svg from the DOM and convert it to a png

    :param driver: webdriver
    :param entity_id: str entity id
    :return: bytes, png formatted bytes string
    """
    # Extract the actual src from the dom and make a GET request for it
    actual_src = dom.get_element(driver, GRID_COMPOUND_IMAGE_SELECTOR_.format(entity_id)).get_attribute('src')
    actual_svg = requests.get(actual_src, auth=('demo', 'demo')).content

    if not actual_svg.startswith(b'<!DOCTYPE svg'):
        assert False, 'Actual image is not an svg'

    # Create a tempfile to create a png bytes string for the actual svg
    with tempfile.NamedTemporaryFile(dir='.', suffix='.svg') as f:
        f.write(actual_svg)
        actual_path = f.name
        actual_png = cairosvg.svg2png(url=actual_path)

    return actual_png


def verify_row_hovered(driver, entity_id):
    """
    Verify that row is hovered.

    :param driver: webdriver
    :param entity_id: str, Compound ID from ID column
    """
    verify_is_visible(driver,
                      GRID_ROW_ID_HOVERED_.format(entity_id),
                      message="The row for compound {} is not hovered".format(entity_id))


def verify_row_selected(driver, entity_id):
    """
    Verify that row is selected.

    :param driver: webdriver
    :param entity_id: str, Compound ID from ID column
    """
    row = dom.get_element(driver, GRID_ROW_CHECKBOX_.format(entity_id))
    assert row.is_selected(), "The checkbox with selector {} for compound {} is not selected" \
        .format(GRID_ROW_CHECKBOX_.format(entity_id), entity_id)


def verify_reasonable_initial_render_count(driver):
    """
    Verify that on first load of the LR, a "reasonable" number of rows render,
    and that the cells in those rows render a "reasonable" number of times.

    :param driver: webdriver
    """
    render_count_map = get_grid_render_count_map(driver)
    total_rows_rendered = len(render_count_map)
    row_container = dom.get_element(driver, GRID_ROWS_CONTAINER)

    rows = dom.get_elements(row_container, GRID_ROW)
    visible_rows = [row for row in rows if element_is_vertically_within_parent(row_container, row)]
    total_visible_rows = len(visible_rows)

    # allow a small buffer for rendering off-screen rows
    assert total_rows_rendered <= total_visible_rows + 4, \
        "The initial render involved rendering {} rows when only {} are visible".format(total_rows_rendered,
                                                                                        total_visible_rows)

    max_allowed_renders = 3
    excessive_renderers = []
    for row, col_map in render_count_map.items():
        for col, render_count in col_map.items():
            # cap frivolous renders
            if render_count > max_allowed_renders:
                excessive_renderers.append((row, col, render_count))

    if excessive_renderers:
        error_message = "In the initial grid render, cells should render no more than {} times." \
                        "\nThe following cells exceeded this:".format(max_allowed_renders)
        for row, col, render_count in excessive_renderers:
            error_message += "\nRow {} Column {} ({} renders)".format(row, col, render_count)
        assert False, error_message


def verify_render_count(driver, entity_id, count, baseline_counts=None):
    """
    Verify the maximum render count of GridCells in a given row.

    :param driver: webdriver
    :param entity_id: id of row whose renders to count
    :param count: maximum allowed render count for cells in the row (or maximum
                  *increase* from the baseline if baseline_counts is provided)
    :param baseline_counts: optional initial render counts *for this entity*
                            (dict mapping columnId -> render count of that cell)
    """
    render_count_map = get_grid_render_count_map(driver)

    excessive_renderers = []
    for col, render_count in render_count_map[entity_id].items():
        max_allowed_renders = count + (0 if not baseline_counts else baseline_counts[col])
        if render_count > max_allowed_renders:
            excessive_renderers.append((col, render_count, max_allowed_renders))

    if excessive_renderers:
        error_message = "The following cells in row {} rendered excessively:".format(entity_id)
        for col, render_count, max_allowed_renders in excessive_renderers:
            error_message += "\nColumn {}: {} renders (max {})".format(col, render_count, max_allowed_renders)
        assert False, error_message


def verify_frozen_columns_in_grid(driver, frozen_column_names):
    """
    Verify frozen columns in the grid.
    :param driver: Selenium Webdriver
    :param frozen_column_names: list, Representing the expected frozen columns in the grid. The order of column names
                                is from left of the grid to the right and is important.
    """
    expected_frozen_columns = '\n'.join(frozen_column_names)

    def get_frozen_columns(driver_):
        fixed_cell_group_wrapper = dom.get_elements(driver_, GRID_FIXED_COLUMN_GROUP)
        frozen_columns_in_grid = fixed_cell_group_wrapper[0].text
        return frozen_columns_in_grid

    assert eventually_equal(driver, get_frozen_columns, expected_frozen_columns), \
        'Expected following columns to be frozen {}.  Got {}'.format(expected_frozen_columns, get_frozen_columns(driver))


def verify_frozen_columns_in_column_mgmt_ui(driver, expected_frozen_columns):
    """
    Verify the frozen column names in the Columns Management UI (LiveReport Tab under D*C Tree).
    :param driver: Selenium Webdriver
    :param expected_frozen_columns: list, expected column names to be frozen in the Column Management UI from
                                    the top to bottom. Order of the column names is important too.
    """

    def get_frozen_columns_from_column_mgmt_ui(driver_):
        frozen_column_element = dom.get_elements(driver_, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN)
        observed_frozen_columns_in_tree_ui = [element.text for element in frozen_column_element]
        return observed_frozen_columns_in_tree_ui

    assert eventually_equal(driver, get_frozen_columns_from_column_mgmt_ui, expected_frozen_columns), \
        "Expected following column names to be frozen {}".format(expected_frozen_columns)


def verify_visible_columns_in_live_report(driver, expected_column_list):
    """
    Just to verify the visible columns in LiveReport by name.
    :param driver: Selenium Webdriver
    :param expected_column_list: list, list of columns expected to be in the LiveReport.
    """

    lr_column_names = dom.get_element(driver, GRID_HEADER_TOP).text
    observed_lr_column_names = lr_column_names.split("\n")

    if len(expected_column_list) == len(observed_lr_column_names):
        for expected, observed in zip(expected_column_list, observed_lr_column_names):
            assert expected == observed, "Column {} is expected to be in the LiveReport".format(expected)
    else:
        raise dom.LiveDesignWebException("Missing columns. Expected the following columns {} but got following "
                                         "{} columns".format(expected_column_list, observed_lr_column_names))


def verify_selected_row_ids(driver, *expected_selected_ids):
    """
    Verify selected row Ids.

    :param driver: selenium webdriver
    :param expected_selected_ids: set, list of compound ids which are expected
    """
    row_container = dom.get_element(driver, GRID_ROWS_CONTAINER)

    wheel_to_bottom(driver, row_container)
    selected_ids = []

    while True:
        rows = dom.get_elements(row_container, GRID_ROW)
        visible_rows = [row for row in rows if element_is_vertically_within_parent(row_container, row)]

        for row in visible_rows:
            elem = dom.get_element(row, SELECTED_ID, dont_raise=True, timeout=2)
            if elem is not None:
                selected_ids.append(elem.text)

        # getting first visible row element row index to ensure scrolling reached top
        first_visible_row_index = dom.get_element(visible_rows[0], ROW_INDEX).text
        if first_visible_row_index == '1' or len(selected_ids) > len(expected_selected_ids):
            break

        scroll_distance = calculate_scroll_distance(visible_rows)

        # NOTE: Scrolls vertically from bottom to top(- is added for scrolling bottom to top)
        wheel_element(driver, row_container, -scroll_distance)

    assert set(selected_ids) == set(expected_selected_ids), 'expected ids:{}, actual ids:{}'.format(
        set(expected_selected_ids), set(selected_ids))


def verify_row_menu_items(driver, row_id, *row_menu_items):
    """
    Verify row menu items

    :param driver: selenium webdriver
    :param row_id: str, ID of the compound
    :param row_menu_items: str, menu item name(s)
    """
    # open row menu
    open_row_menu(driver, row_id)
    # verifying menu items
    for menu_item in row_menu_items:
        verify_is_visible(driver, selector=OPENED_MENU_ITEMS, selector_text=menu_item)

    # closing row menu by clicking on active Livereport tab
    dom.click_element(driver, TAB_ACTIVE)
    # waiting until row menu is not visible
    wait.until_not_visible(driver, GRID_ROW_MENU)


def verify_rows_selected(driver, selected_entity_ids, check_selection=True):
    """
    Verify whether given rows checkbox is selected or deselected based on check_selection

    :param driver: selenium webdriver
    :param selected_entity_ids: list, list of entity ids which needs to be verified
    :param check_selection: boolean, True if you want to verify rows are selected, False to verify rows are deselected
    """
    for entity_id in selected_entity_ids:
        selector = GRID_ROW_CHECKBOX_INPUT.format(entity_id)

        message = "The checkbox with selector {} for compound {} is not selected".format(selector, entity_id)
        if check_selection:
            assert dom.get_element(driver, selector, must_be_visible=False).is_selected(), message
        else:
            assert not dom.get_element(driver, selector, must_be_visible=False).is_selected(), message


def verify_grid_find_panel(driver, match_count):
    """
    Verify Grid panel input and buttons.

    :param driver: Selenium webdriver
    :param match_count: str, grid find match count text which appear beside grid find input text box
    """
    verify_is_visible(driver, GRID_FIND_INPUT)
    verify_is_visible(driver, GRID_FIND_MATCH_COUNT, match_count)
    verify_is_visible(driver, GRID_FIND_PREV_BUTTON, '<')
    verify_is_visible(driver, GRID_FIND_NEXT_BUTTON, '>')
    verify_is_visible(driver, GRID_FIND_CLOSE_BUTTON, 'X')


def verify_grid_matching_elements(driver, expected_total_matches, expected_matching_text=None, at_least=False):
    """
    Verifies grid matching element count which includes verify yellow matches and orange matches and verifies grid
    matching text after grid find. Text verification is done only if expected_matching_text is provided.

    :param driver: selenium webdriver
    :param expected_total_matches: int, total expected matching items count
    :param expected_matching_text: str, expected matching text
    :param at_least: If True, will verify there are *at least* that many matching elements.
        If False, will verify there are *exactly* that many matching elements
    """
    if expected_total_matches == 0:
        # verify total matching elements
        total_matching_elements = dom.get_elements(driver, GRID_FIND_TOTAL_MATCHES, dont_raise=True, timeout=2)
        assert len(total_matching_elements) == 0, \
            "Expected total matching elements: {}, " \
            "Actual total matching elements : {}".format(0, len(total_matching_elements))
    else:
        # verify orange matching count
        current_matching_elements = dom.get_elements(driver, GRID_FIND_ORANGE_MARK, dont_raise=True, timeout=2)
        assert len(current_matching_elements) == 1, \
            'Expected orange matching element count: 1, ' \
            'Actual orange matching element count: {}'.format(len(current_matching_elements))

        # verify yellow matching count
        other_matching_elements = dom.get_elements(driver, GRID_FIND_YELLOW_MARK, dont_raise=True, timeout=2)
        if at_least:
            assert len(other_matching_elements) >= expected_total_matches - 1, \
                'Expected at least matching yellow element count: {}, ' \
                'Actual matching yellow element count:{}'.format(expected_total_matches - 1, len(other_matching_elements))
        else:
            assert len(other_matching_elements) == expected_total_matches - 1, \
                'Expected matching yellow element count: {}, ' \
                'Actual matching yellow element count:{}'.format(expected_total_matches - 1, len(other_matching_elements))

        # verify all matching text in grid
        if not expected_matching_text:
            return
        all_matches = current_matching_elements + other_matching_elements
        for matching_element in all_matches:
            assert matching_element.text == expected_matching_text, \
                "Expected matching text:{}, " \
                "Actual matching text:{}".format(expected_matching_text, matching_element.text)


def verify_column_group_contents(expected_column_group_content, actual_column_group_content):
    """
    Verifies the column group contents which is received in the form of ColumnGroup objects

    :param expected_column_group_content: ColumnGroup object to be matched
    :param actual_column_group_content: ColumnGroup object to match with
    (e.g. [ColumnGroup(id=2812375, name=None, frozen=True, columns_order=['6'], limiting_condition=None), ...]
    """
    for actual_column_group_obj, expected_column_group_obj in zip(actual_column_group_content,
                                                                  expected_column_group_content):
        assert actual_column_group_obj.name == expected_column_group_obj.name, 'Expected name {} but got {} instead'.format(
            expected_column_group_obj.name, actual_column_group_obj.name)
        assert actual_column_group_obj.columns_order == expected_column_group_obj.columns_order, 'Expected columns order {} but got {} instead'.format(
            expected_column_group_obj.columns_order, actual_column_group_obj.columns_order)
