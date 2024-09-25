"""
Button for adding idea to live report, found under the sketcher

From FE JS CompoundPanelSelectors.ADD_IDEA_TO_LIVE_REPORT_BUTTON
"""
# ----- COMMON SECTION ----- #
COMPOUNDS_PANE_TAB_PICKER = '#compounds-pane-container .tab-picker'
COMPOUNDS_PANE_TAB = '{} .tab-link .tab-link-content'.format(COMPOUNDS_PANE_TAB_PICKER)
COMPOUNDS_PANE_ACTIVE_TAB = '{} .active-tab-link .tab-link-content'.format(COMPOUNDS_PANE_TAB_PICKER)

### DRAW & SEARCH BY STRUCTURE SECTION ###
# Realtime properties pane
REALTIME_PROPERTIES_PANE = '.realtime-pane'
REALTIME_PROPERTY_ = '.realtime-pane .realtime-property[data-property-name="{}"]'
REALTIME_EMPTY_MESSAGE = '.realtime-pane span'

# ----- Add sketched compound to LR buttons ----- #
# Basic Search Add Idea Button
ADD_IDEA_TO_LIVE_REPORT_BUTTON = 'button.add-compound'
# Substructure, Similarity, and Exact Search Add Compounds Button
SEARCH_AND_ADD_COMPOUNDS_BUTTON = 'button.search-compounds'

# ----- Sketcher Mode CSS selectors ----- #
ACTIVE_MODE = '.x-form-cb-checked'
ADD_IDEA_TAB = '.sketcher-mode-idea'
BASIC_SEARCH_SIMILARITY_SEARCH_SLIDER = '.similarity-slider .rc-slider .rc-slider-handle'
BASIC_SEARCH_SIMILARITY_SEARCH_SLIDER_THRESHOLD_LABEL = '.search-threshold'
EXACT_TAB = '.sketcher-mode-exact'
MAX_COMPOUNDS = '.x-form-field.x-form-text[name=\"max-compounds\"]'
SUBSTRUCTURE_TAB = '.sketcher-mode-substructure'
SIMILARITY_TAB = '.sketcher-mode-similarity'

# Compounds found (shown after doing a substructure, similarity, and exact search)
COMPOUNDS_FOUND = '.search-result-count'

# ----- SEARCH BY ID SECTION ----- #
SEARCH_BY_ID_BUTTON = '.search-compounds'
SEARCH_BY_ID_TEXTAREA = '.search-textarea'

COMPOUND_SEARCH_SUB_TAB = '.tab-content-list .active-tab-content .compounds-design-pane-row .sub-tab'
COMPOUND_SEARCH_SUB_TAB_ACTIVE = '.tab-content-list .active-tab-content .compounds-design-pane-row .sub-tab.active'
COMPOUND_SEARCH_BY_ID_TEXTAREA = '.search-textarea'
COMPOUND_SEARCH_BUTTON = '.search-compounds'

# ----- IMPORT FROM FILE SECTION ----- #
IMPORT_FILE_BUTTON = '.import-pane .big-button.import-file'
IMPORT_FILE_BUTTON_DISABLED_STATE = '{}.disabled'.format(IMPORT_FILE_BUTTON)
IMPORT_FILE_BUTTON_ENABLED_STATE = '{}:not(.disabled)'.format(IMPORT_FILE_BUTTON)
IMPORT_FROM_FILE_PLACEHOLDER_TITLE = '.import-pane .import-file-field input[placeholder="Select an SDF, CSV, Excel or Maestro file"]'
IMPORT_FROM_FILE_INPUT_ELEMENT = '.import-pane .import-file-field input[type="file"].import-file-helper'
IMPORT_FROM_FILE_COLUMN_SELECTION_LIST_DROPDOWN = '.import-file-field select'
IMPORT_FROM_FILE_COLUMN_SELECTION_LIST_DROPDOWN_OPTION = '.import-file-field select option'
IMPORT_FROM_FILE_INVALID_MESSAGE_SELECTOR = '.import-controller-header .form-error-state-invalid'
IMPORT_FROM_FILE_CHECKBOX = '.import-pane label'
IMPORT_FROM_FILE_VALID_MESSAGE_SELECTOR = '.import-controller-header .form-error-state-valid'
ERROR_DIALOG_TEXT = '.bb-dialog-container .bb-dialog-body'
ERROR_DIALOG_OK_BUTTON = '.bb-dialog-container .ok-button'

# Search toggle options
GEAR_BUTTON_DOWN = '.gear-button .fa-caret-down'
GEAR_BUTTON_UP = '.gear-button .fa-caret-up'
MAX_RESULTS_DIALOG = '.structure-search-fields .open'
MAX_RESULTS_INPUT = '.bb-menu-item .field-input'
