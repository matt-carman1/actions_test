BOX_WIDGET = '.box-widget'
BOX_WIDGET_BODY_CATEGORY = '.box-widget-body.category'
BOX_WIDGET_BODY_QUICK_FILTER = '.box-widget-body.quick-filter'
BOX_WIDGET_BODY_RANGE = '.box-widget-body.range'

COMPOUND_TYPE_CHECKBOX = '.quick-checkbox'

FILTERS_PANELS = '#filters-panels'
FILTERS_BOX_WIDGET = '{} .box-widget'.format(FILTERS_PANELS)
FILTERS_BOX_WIDGET_HEADER_NAME = '{} .header-name'.format(FILTERS_BOX_WIDGET)

FILTERS_OPTIONS = '#filters-options'

FILTERS_HEADER_RIGHT_BUTTON_CONTAINER = '.filters-header-right-button-container'
FILTERS_HEADER_MENU_ITEM = '.filters-header-menu .bb-menu-item'

FILTER_INVERT_BUTTON = 'div.invert-toggle'
FILTER_INVERT_BUTTON_INVERTED = '{}.inverted'.format(FILTER_INVERT_BUTTON)
FILTER_ENABLE_BUTTON = 'input.enable-toggle'

TOGGLE_ALL_FILTERS_BUTTON = '.filters-header-menu-checkbox-container'
TOGGLE_ALL_FILTERS_CONTAINER_ACTIVE = '.filters-header-menu-checkbox-container.active'

FILTER_COLUMN_PICKER = '#filter-column-picker ul'
FILTER_COLUMN_PICKER_DROPDOWN_LIST = '.filter-column-picker-dropdown ul'

# This selector below could be used for both filters and advanced search tests
SELECTED_CONTAINER = '.selected-bubble-container'

FILTER_TYPE_CATEGORY = '.category'
FILTER_TYPE_RANGE = '.range'

# This selector below could be used for both filters and advanced search tests
HEADER_TITLE = '{} .header-name'.format(BOX_WIDGET)
FILTER_HEADER_RIGHT_BUTTON = '.header-right-button'
FILTER_HEADER_RIGHT_MENU_OPEN = 'div.header-right-menu .open'

FILTER_RANGE_SLIDER_INVERTED = '.rc-slider.inverted'
FILTER_RANGE_SLIDER_DISABLED = '.rc-slider.rc-slider-disabled'

FILTER_RANGE_LOWER_AUTO_BUTTON = \
    '.rc-slider-handle-1 ~ .rc-slider-input-buttons a'
FILTER_RANGE_LOWER_VALUE_INPUT = \
    '.rc-slider-handle-1 ~ input.rc-slider-input'
FILTER_RANGE_UPPER_AUTO_BUTTON = \
    '.rc-slider-handle-2 ~ .rc-slider-input-buttons a'
FILTER_RANGE_UPPER_VALUE_INPUT = \
    '.rc-slider-handle-2 ~ input.rc-slider-input'
FILTER_RANGE_LOWER_SLIDER = 'div.rc-slider-handle-1'
FILTER_RANGE_UPPER_SLIDER = 'div.rc-slider-handle-2'

# filter gear menu items
FILTER_GEAR_MENU_ITEM_SHOW_AS_TEXT = 'Show as text'
FILTER_GEAR_MENU_ITEM_SHOW_AS_RANGE = 'Show as range'