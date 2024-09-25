COLUMN_TREE_PICKER = '.data-and-columns-drawer-wrapper'
COLUMN_TREE_PICKER_ADD_NODE_BUTTON = 'span.plus-button-multi-select'
COLUMN_TREE_SECTION_NODE = '.top-level-column-folder-node'
COLUMN_TREE_PICKER_CREATE_NEW_FFC_BUTTON = 'div.action.freeform'
COLUMN_TREE_PICKER_CREATE_NEW_FORMULA_BUTTON = 'div.action.formulas'
COLUMN_TREE_PICKER_NODE_TEXT_AREA = 'div.node-text-area'
COLUMN_TREE_PICKER_SEARCH = '{} .column-tree-search-field input'.format(COLUMN_TREE_PICKER)
COLUMN_TREE_PICKER_NODE_ICON_AREA = '.node-icons-area'
COLUMN_TREE_PICKER_TEXT_NODE = 'div.node-text'
COLUMN_TREE_PICKER_TEXT_NODE_HIGHLIGHTED = 'div.node-text.highlighted'
COLUMN_TREE_ADD_COLUMNS_BUTTON = '{} .add-button-multi-select'.format(COLUMN_TREE_PICKER)
COLUMN_TREE_SCROLL_CONTAINER = '.column-tree-list .ReactVirtualized__Grid__innerScrollContainer'
COLUMN_TREE_SEARCH_BOX = '{} .column-tree-search-field input'.format(COLUMN_TREE_PICKER)
COLUMN_FOLDER_MULTI_SELECT = '.column-folder-multi-select'
COLUMN_FOLDER_TEXT_AREA = '{}.inner-folder-text'.format(COLUMN_TREE_PICKER_TEXT_NODE)
COLUMN_TREE_SEARCH_HIGHLIGHTED = '.column-tree-text-highlight'

INVALID_SEARCH_RESULT = '{} .no-result'.format(COLUMN_TREE_PICKER)
PARAMETERIZED_MODEL_DIALOG = '.bb-dialog-container.parameterized-dialog'
COLUMNS_TREE_DATA_PROJECT_TAB = '#project-tab'
COLUMNS_TREE_LIVEREPORT_TAB = '#live-report-tab'

# ---- TOOLTIPS IN D&C TREE ----- #
COLUMN_TREE_PICKER_TOOLTIP = '.column-picker-tooltip'
COLUMN_TREE_PICKER_TOOLTIP_HEADER_TEXT = '{} .header-text'.format(COLUMN_TREE_PICKER_TOOLTIP)
COLUMN_TREE_PICKER_TOOLTIP_BODY_TEXT = '{} .body-text'.format(COLUMN_TREE_PICKER_TOOLTIP)
COLUMN_TREE_PICKER_TOOLTIP_ADD_FAVORITE_ICON = '.icon-favorite-add'
COLUMN_TREE_PICKER_TOOLTIP_REMOVE_FAVORITE_ICON = '.icon-favorite-remove'
ADD_TO_LIVEREPORT_TOOLTIP_BUTTON = '.big-button.live-report-add'
EDIT_TOOLTIP_BUTTON = 'button[class="big-button freeform-column-edit"] span'
COLUMN_TREE_SEARCH_INPUT_CLEAR_BUTTON = '.search-input-clear-button'

PROJECT_TAB_SEARCH_INPUT_CLEAR_BUTTON = '.column-tree-search-field button'
PROJECT_FAVORITE_COLUMN_NODE = '.project-favorite'

# ----- LIVEREPORT TAB IN D&C TREE ----- #
LIVEREPORT_TAB_SEARCH_INPUT_CLEAR_BUTTON = '.search-input-clear-button'
LIVEREPORT_COLUMNS_WRAPPER = '.live-report-columns-wrapper'
LIVEREPORT_COLUMN_CONTAINER_ID_ = ".column-checkbox-container[data-addable-column-id*='{}']"
LIVEREPORT_COLUMN_LABEL_ID_ = ".column-checkbox-container[data-addable-column-id='{}'] label"
LIVEREPORT_COLUMN_CHECKBOX_LABEL = ".columns-list .column-checkbox-label"
LIVEREPORT_HIDDEN_COLUMN_LABEL = "{}.is-hidden".format(LIVEREPORT_COLUMN_CHECKBOX_LABEL)
LIVEREPORT_VISIBLE_COLUMN_LABEL = "{}:not(.is-hidden)".format(LIVEREPORT_COLUMN_CHECKBOX_LABEL)
LIVEREPORT_COLUMN_CHECKBOX_LABEL_SELECTED = '{}.selected'.format(LIVEREPORT_COLUMN_CHECKBOX_LABEL)
LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN = '{}.frozen'.format(LIVEREPORT_COLUMN_CHECKBOX_LABEL)
LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN_GROUP = '.frozen.group'
LIVEREPORT_COLUMN_LIST_FREEZE_LINE = '.columns-list .freeze-line'
LIVEREPORT_COLUMN_MANAGER_BUTTON = ".live-report-column-manager-button"
LIVEREPORT_COLUMN_MANAGER_BUTTON_DISABLED = '.live-report-column-manager-button.disabled'
LIVEREPORT_CHECKED_COLUMNS = '.columns-list .selected + span'
LIVEREPORT_COLUMN_CHECKBOX_LABEL_GROUPED_COLUMNS = '.column-checkbox-label.group'
LIVEREPORT_COLUMN_SEARCH_BOX = '{} .search-input input'.format(LIVEREPORT_COLUMNS_WRAPPER)
LIVEREPORT_COLUMN_LABEL_HIGHLIGHT = '{} mark'.format(LIVEREPORT_COLUMN_CHECKBOX_LABEL)

PARTIALLY_SELECTED_COLUMN_NODE = '.partially-selected'
SELECTED_COLUMN_NODE = '.selected'

LIVEREPORT_NOTIFICATION_MESSAGE = '.view-mode-notification'


class ColumnTreeSectionTooltip:
    """
    This class contains the selectors for section tooltip header & description in D&C Tree
    """
    # header selectors
    PROJECTS_FAVORITE_HEADER = 'Project Favorites'
    COMPUTED_PROPERTIES_HEADER = 'Computed Properties'
    COMPUTATIONAL_MODELS_HEADER = 'Computational Models'
    ASSAYS_HEADER = 'Experimental Assays'
    OTHER_COLUMNS_HEADER = 'Other Columns'
    FORMULAS_HEADER = 'Formulas'
    MPO_HEADER = 'Multi-Parameter Optimization'
    FFC_HEADER = 'Freeform Columns'
    # description selectors
    PROJECTS_FAVORITE_DESC = 'Favorite Computational Models and Experimental Assays. ' \
                            'Add to this list by clicking the star icon next to any model or assay below.'
    COMPUTED_PROPERTIES_DESC = 'Computed Properties are simple properties like molecular weight. ' \
                              'To add custom properties to this list contact your system administrator.'
    COMPUTATIONAL_MODELS_DESC = 'Computational Models include complex simulations and 3D docking models. ' \
                               'Any 3D docking models include the term (Complex) in their name. ' \
                               'To add custom models to this list contact your system administrator.'
    ASSAYS_DESC = 'Experimental Assays represent data obtained in a laboratory. ' \
                  'To add additional assays to this list contact your system administrator.'
    OTHER_COLUMNS_DESC = 'Other Columns are assorted columns from any database or data source. ' \
                        'They can any hold information on a lot or compound-wide level ranging from vendor names, ' \
                        'to pre-computed property values.'
    FORMULAS_DESC = 'Formula Columns allow you to translate or combine the values of one or more columns in a ' \
                    'LiveReport using standard arithmetical operators, built-in functions, and logical conditions.'
    MPO_DESC = 'Multi-Parameter Optimization columns allow you to combine several experimental and computational ' \
               'properties into one color-coded, aggregate measure of compound quality that can be used across ' \
               'LiveReports and projects.'
    FFC_DESC = (
        "Freeform columns allow you to enter custom data for any compound by typing directly into a spreadsheet cell."
        "\nThe column can optionally be 'published' to make it available and editable across many LiveReports."
        "\nUse these to to track compound state for workflows, bin compounds into groups, collect structured comments, "
        "and more.")
