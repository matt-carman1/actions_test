COLOR_RULES_DIALOG = '.color-rules-dialog'
ADD_COLORING_RULE = '{} .buttons .ok-button'.format(COLOR_RULES_DIALOG)
BLUE = '.color-palate-item:nth-child(48)'
GREEN = '.color-palate-item:nth-child(56)'
CELL_SELECTOR_LABEL = '.dropdown-list-item'
# the parameter represents the row of the coloring rows in the dialog
COLOR_SELECTOR = '{} .value-rule:nth-child({{}}) .value-rule-colorpicker .color-swab'.format(COLOR_RULES_DIALOG)
COLOR_WINDOW_OK_BUTTON = '{} .bb-dialog-button.ok-button:not(.disabled)'.format(COLOR_RULES_DIALOG)
COLOR_WINDOW_CANCEL_BUTTON = '{} .bb-dialog-button'.format(COLOR_RULES_DIALOG)
COLOR_RULE = '{} .value-rule:nth-child({{}}) .dropdown-header'.format(COLOR_RULES_DIALOG)
COLOR_RULE_INPUT = '{} .value-rule:nth-child({{}}) .dropdown-header .dropdown-query-input'.format(COLOR_RULES_DIALOG)
SLIDER_MIN = '.range-rule .low-inputs input[type="text"]'
SLIDER_MAX = '.range-rule .high-inputs input[type="text"]'
CONVERT_GEAR_ICON = '.convert-rule-container .gear-icon'
CONVERT_COLOR_RULES_WINDOW = '.bb-dialog-container:not({})'.format(COLOR_RULES_DIALOG)
CONVERT_COLOR_RULES_WINDOW_HEADER = '{} .bb-dialog-header span'.format(CONVERT_COLOR_RULES_WINDOW)
CONVERT_COLOR_RULES_WINDOW_BODY = '{} .bb-dialog-body'.format(CONVERT_COLOR_RULES_WINDOW)
CONVERT_DIALOG_WINDOW_CANCEL_BUTTON = '{} .bb-dialog-bottom .link-button'.format(CONVERT_COLOR_RULES_WINDOW)
CONVERT_DIALOG_WINDOW_OK_BUTTON = '{} .bb-dialog-bottom .ok-button'.format(CONVERT_COLOR_RULES_WINDOW)
CLEAR_RULES = '{} .clear-rules'.format(COLOR_RULES_DIALOG)
COLOR_RULES_MENU_CONTAINER = '.color-rules-menu-container'
COLOR_RULES_MENU_ITEM = '.menu-list-container .bb-menu .bb-menu-item:nth-child({})'
PALATE_SELECTOR = ".color-palate div[data-value='{}']"
RANGE_COLOR_SELECTOR_LEFT = '.low-inputs .color-swab'
RANGE_COLOR_SELECTOR_RIGHT = '.high-inputs .color-swab'
