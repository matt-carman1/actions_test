# Forms View dropdown
FORMS_ICON = '.view-mode-button.forms-icon'
# Forms dropdown menu
FORMS_MENU = '.forms-layouts-menu'
SELECTED_FORMS_LAYOUT = '{} .checked'.format(FORMS_MENU)

# Forms container
FORMS_CONTAINER = '.primary-livereport-gadget'

# Forms toolbar
ADD_WIDGET_TOOLBAR_BUTTON = '.big-button.add-widget'
FORMS_TOOLBAR = '#forms-toolbar'
SAVE_LAYOUT_TOOLBAR_BUTTON = '.big-button.save-layout'

# to cancel use library.base.click_cancel

# Add a Layout dialog options
COMPOUND_DETAIL = '.layout.layout-compound-detail'
ASSAY_VIEWER = '.layout.layout-assay-viewer'
PLOT_VIEW = '.layout.layout-plot'
CUSTOM_LAYOUT_DIV = '.layout.layout-custom'

# 'Add a widget' dialog options
SPREADSHEET_WIDGET_ICON = '.widget-icon.widget-icon-grid'
VISUALIZER_WIDGET_ICON = '.widget-icon.widget-icon-viz'
NEW_PLOT_WIDGET_ICON = '.widget-icon-new-plot'

# Configure Visualizer Widget dialog
VISUALIZER_WIDGET_NAME_INPUT = '.selection-sync-picker-layout-name-input input'

#----- Widget elements and buttons -----#
# General
ADD_WIDGET_BUTTON = '.forms-empty-gadget .button'
CLOSE_TAB = '.lm_close_tab'
TAB_TITLE = '.lm_title'

FORM_STACK = '.lm_stack'
FORM_COLUMN = '.lm_column'
FORMS_CLOSE_TAB = '.lm_close_tab'

# Spreadsheet Widget
SPREADSHEET_WIDGET = '.grid.fixed-data-table'

# Compound Image Widget
FORMS_STRUCTURE_GADGET = '.forms-structure-gadget'
BOTTOM_TOOLBAR = '.bottom-tools'
ID_INFO = '{} .id-div .compound-id-input input:not([readonly])'.format(BOTTOM_TOOLBAR)
DECREASE_ROW_SELECTION = 'button.decrease-row-selection'

# List Widget
LIST_GADGET = '.property-list-gadget'
FIELD_LIST = '.field-list-item'
COLUMN_NAME = '.tile-field-name-wrapper'
COLUMN_VALUE = '.tile-cell-wrapper'

# Plots Widget
SCATTER_WIDGET = '.plots-widget.plot-mode-scatter'
HISTOGRAM_WIDGET = '.plots-widget.plot-mode-histogram'
