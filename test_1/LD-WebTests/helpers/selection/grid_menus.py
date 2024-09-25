MENU_ITEM_WITH_SUB_MENU = '.bb-sub-menu-item'

MENU_CHECKBOX_ITEM = '.bb-menu-item.checkbox'
MENU_CHECKBOX_ITEM_CHECKED = '.bb-menu-item.checkbox.checked'

FIRST_SUB_MENU_ITEM = '.bb-sub-menu-item .open > div:nth-child(1)'
LAST_SUB_MENU_ITEM = '.bb-sub-menu-item .open > div:nth-last-child(1)'
SUB_MENU_ITEM = '.bb-sub-menu-item .bb-menu-item'
DEFAULT_AGGREGATION_MENU_ITEM = '.bb-sub-menu .bb-menu-item.default-aggregation-type'

MENU_COLUMN = '.bb-menu-item.columns-vis.bb-sub-menu-item'
MENU_COLUMN_CHECKBOX_MENU_ITEM = '{} {}'.format(MENU_COLUMN, MENU_CHECKBOX_ITEM)
MENU_COLUMN_CHECKBOX_MENU_ITEM_CHECKED = '{} {}'.format(MENU_COLUMN, MENU_CHECKBOX_ITEM_CHECKED)

LIMITING_ASSAY_COLUMN_DIALOG_BOTTOM_ACTION_BUTTONS = '.bb-dialog-bottom ' \
                                                     '.link-button.bb-dialog-button'

REORDER_COLUMNS_ACTION_BUTTONS = '.column-selector-window-bottom .link-button.cancel-button'
