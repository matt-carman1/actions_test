"""
Buttons in Advanced Search Panel
"""

# ADVANCED SEARCH FOR COMPOUNDS #
# Textbox to query models
ADVANCED_SEARCH_TEXTBOX = 'input[placeholder="Add Query on..."]'
# Indicator on body element (adds animation to left action button)
ADVANCED_SEARCH_ACTIVE_CLASS = '.live-report-query-active'

# ----- QUERY SELECTORS ----- #
# All Advanced Query headers (Contains the name)
QUERY_HEADERS = '#adv-query-panels .box-widget .header-name'
ADVANCED_SEARCH_ADD_COLUMNS_BUTTON = '.adv-query-drawer .add-button-multi-select'
ADVANCED_QUERY_COLUMN_SELECTOR = '#adv-query-column-selector'

# ----- BOTTOM OPTIONS AND ADVANCED SEARCH QUERY LINKS (All IDs, Compound Structure, Project...etc) ----- #
BOTTOM_OPTIONS_LINKS = '.adv-query-drawer .bottom-options > *'
ALL_IDS_LINK = 'All IDs'
COMPOUND_STRUCTURE_LINK = 'Compound Structure'
PROJECT_LINK = 'Project'
DATABASE_LINK = 'Database/Dataset'
PRESENCE_IN_LIVE_REPORT_LINK = 'Presence in Live Report'

# ----- Advanced Query Panels ----- #
ADV_QUERY_PANEL = '#adv-query-panels'
ADV_QUERY_BOX_WIDGET = '{} .box-widget'.format(ADV_QUERY_PANEL)
ADV_QUERY_PANEL_HEADER = '{} .header-name'.format(ADV_QUERY_BOX_WIDGET)
# ADV_QUERY_PANEL_GEAR_BUTTON = '.header-right-button.adv-query-panel-gear-btn'
ADV_QUERY_PANEL_GEAR_BUTTON_MENU = '.header-right-menu.adv-query-panel-right-menu'
ADV_QUERY_PANEL_GEAR_BUTTON_MENU_OPEN = '.header-right-menu.adv-query-panel-right-menu .open'
ADV_QUERY_INVERT = '.invert-toggle'

# ----- COMPOUND STRUCTURE QUERY MODES & RELATED ----- #
INACTIVE_MODE_BUTTON = 'div.adv-query-structure-valuetype:not(.active)'
SUBSTRUCTURE = '.adv-query-structure-valuetype[data-valuetype="substructure"]'
SIMILARITY = '.adv-query-structure-valuetype[data-valuetype="similarity"]'
SIMILARITY_VALUE_INPUT = 'input.similarity-value'
ADV_SEARCH_SKETCHER = '.draggable-compound-panel'

# ----- "PRESENCE IN LIVE REPORT" QUERY SELECTORS ----- #
PRESENCE_IN_LR_DROPDOWN = '.adv-query-dropdown'
PRESENCE_IN_LR_DROPDOWN_ACTIVE = '{}.active'.format(PRESENCE_IN_LR_DROPDOWN)
PRESENCE_IN_LR_DROPDOWN_OPTIONS = '.adv-query-livereport-choose'
PRESENCE_IN_LR_DROPDOWN_TITLE = '.dropdown-title'

# ----- Advanced Search bottom right drawer ----- #
# Search for Compounds button (adds to LR)
SEARCH_AND_ADD_COMPOUNDS_BUTTON = '.big-button.start.tooltip-target:not(.disabled)'
DISABLED_SEARCH_AND_ADD_COMPOUNDS_BUTTON = '.big-button.start.tooltip-target.disabled'
ADV_QUERY_WARNING = "#adv-query-drawer-tooltip-warning-only-not-lr-presence"

# Stop Search for compounds
ADV_QUERY_STOP_SEARCH = '.big-button.stop.tooltip-target'
# Auto-update Results checkbox
AUTO_UPDATE_CHECKBOX = '.adv-query-auto-update-checkbox'
AUTO_UPDATE_CHECKED = '.adv-query-auto-update-checkbox input:checked + span'
AUTO_UPDATE_NOT_CHECKED = '.adv-query-auto-update-checkbox input:not(:checked) + span'

CLEAR_REPORT_CHECKBOX = '.adv-query-clear-lr-checkbox'
CLEAR_REPORT_NOT_CHECKED = '.adv-query-clear-lr-checkbox input:not(:checked) + span'
CLEAR_REPORT_CHECKED = '.adv-query-clear-lr-checkbox input:checked + span'

# ----- Advanced Search Clear Button ----- #
CLEAR_ADVANCED_QUERY_BUTTON = '#adv-query-remove-all-button'
CLEAR_ADVANCED_QUERY_DIALOG_TITLE = 'Delete All Search Conditions'
CLEAR_ADVANCED_QUERY_SEARCH = '.column-tree-input-button'

# ----- Range Slider in Query Panel ----- #
QUERY_RANGE_LOWER_BOX = '.range-widget .low-value'
QUERY_RANGE_LOWER_AUTO_BUTTON = '.range-widget .adv-query-low-infinity-button'
QUERY_RANGE_LOWER_VALUE_INPUT = '.range-widget .low-value input'
QUERY_RANGE_UPPER_BOX = '.range-widget .high-value'
QUERY_RANGE_UPPER_AUTO_BUTTON = '.range-widget .adv-query-high-infinity-button'
QUERY_RANGE_UPPER_VALUE_INPUT = '.range-widget .high-value input'

# ------ Advanced Search query cog menu  ------ #
ADV_QUERY_COG_ICON = '.adv-query-panel-gear-btn'

ADV_PROJECT_QUERY_DROPDOWN = '.dropdown-header'
ADV_PROJECT_QUERY_DROPDOWN_ELEMS = '.adv-query-project-multiselect-li'

AUTOSUGGEST_ITEMS_DELETE = '.selected-bubble-container span'

ADVANCED_SEARCH_TYPE = '#adv-query-view-type'
ADVANCED_SEARCH_VIEW_MENU = 'ul.view-mode'

# ------- Complex Advanced Search ------ #
COMPLEX_ADV_QUERY_PANEL = '.adv-query-panel-list-complex'
COMPLEX_ADV_SEARCH_TEXT_NODE = '.adv-query-text-node:nth-of-type(2)'
COMPLEX_ADV_QUERY_RANGE_1 = '.adv-query-panel[data-id=observation_numeric_range__1]'
COMPLEX_ADV_QUERY_RANGE_2 = '.adv-query-panel[data-id=observation_numeric_range__2]'
COMPLEX_ADV_QUERY_DATABASE_DATASET = '.adv-query-panel[data-id=dataset]'
COMPLEX_ADV_SEARCH_FOCUSED_QUERY = '#adv-query-focused-panel .adv-query-panel[data-id=observation_numeric_range__1]'
