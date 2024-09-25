CANCEL_BUTTON = '.cancel-button'
MODAL_WINDOW = '.bb-window'
LOADING_MASK = '.small-dialog.loading-mask::after'
LR_LOADING_MASK = '.pending.loading-mask'
EXTJS_LOADING_MASK = '.x-mask'

MODAL_DIALOG = '.bb-dialog'
MODAL_DIALOG_HEADER = '.bb-dialog-header'
MODAL_DIALOG_HEADER_LABEL = '.bb-dialog-header span'
MODAL_DIALOG_BODY = '.bb-dialog-body'
MODAL_DIALOG_BOTTOM = '.bb-dialog-bottom'
MODAL_DIALOG_BODY_LABEL = '.bb-dialog-body label'
MODAL_DIALOG_CONTAINER = '.bb-dialog-container-modal'
MODAL_DIALOG_BODY_INPUT = '{} input'.format(MODAL_DIALOG_BODY)
OK_BUTTON = ".ok-button:not([class*='disabled'])"
MODAL_DIALOG_BUTTON = '.bb-dialog-button'
WINDOW_HEADER_TEXT = '.x-window-header-text'
WINDOW_HEADER_TEXT_DEFAULT = '.x-window-header-text-default'
WINDOW_BODY = '.x-window-body'
BOUND_LIST_ITEM = '.x-list-plain li.x-boundlist-item'

LR_RENAME_DIALOG_INPUT = '#rename-spreadsheet-dialog-input'

CLOSE_BUTTON = '.layout-picker-dialog .bb-dialog-header .close button'
CUSTOM_LAYOUT_DIV = '.layout.layout-custom'
DIV_LM_HEADER = 'div.lm_header'
DIV_LM_STACK = 'div.lm_stack'
GOLDEN_LAYOUT_GEAR_MENU_BUTTON = '.golden-layout-gear-menu-button'
NEW_LAYOUT_TITLE_INPUT = 'label.new-layout-dialog-label + input.new-layout-dialog-input'
NEW_PLOT_WIDGET_ICON = '.widget-icon-new-plot'
PLOT_OPTIONS_BB_MENU_ITEM = '.golden-layout-gear-menu.plot .bb-menu.open .bb-menu-item'
SCATTER_PLOT_ICON = '.plot-mode.plot-mode-scatter'

COPY_LR_TO_PROJECT_PREVIEW_TEXT = '.copy-live-report-preview-div'
COPY_LR_TO_PROJECT_LIST = '#copy-live-report-project-list'

OK_CANCEL_DIALOG_WINDOW = '.ok-cancel-dialog-window'
OK_CANCEL_DIALOG_WINDOW_HEADER_TEXT = '{} .x-header-text'.format(OK_CANCEL_DIALOG_WINDOW)
OK_CANCEL_DIALOG_WINDOW_BODY = '{} .x-window-body'.format(OK_CANCEL_DIALOG_WINDOW)
OK_CANCEL_DIALOG_WINDOW_OK_BUTTON = '{} {}'.format(OK_CANCEL_DIALOG_WINDOW, OK_BUTTON)
OK_CANCEL_DIALOG_WINDOW_CANCEL_BUTTON = '{} {}'.format(OK_CANCEL_DIALOG_WINDOW, CANCEL_BUTTON)

# selector for input related fields in Modal
MODAL_DIALOG_LABEL_INPUT = ".bb-dialog label[title='{}'] ~ input"
# selector for textarea related fields in Modal
MODAL_DIALOG_LABEL_TEXTAREA = ".bb-dialog label[title='{}'] ~ textarea"
# selector for upload related fields in Modal
MODAL_DIALOG_LABEL_DIV = ".bb-dialog label[title='{}'] ~ div"

PARAM_MODEL_DIALOG = '.parameterized-dialog'
PARAM_MODEL_DIALOG_CANCEL_BUTTON = '{} .link-button'.format(PARAM_MODEL_DIALOG)
PARAM_MODEL_DIALOG_OK_BUTTON = '{} .ok-button'.format(PARAM_MODEL_DIALOG)
PARAM_MODEL_DIALOG_OK_BUTTON_DISABLED = '{}.disabled'.format(PARAM_MODEL_DIALOG_OK_BUTTON)
PARAM_MODEL_VALIDATION_ERROR = '{} #error-message-container'.format(PARAM_MODEL_DIALOG)

# Selectors common to both Duplicate and Export LR Dialog
MODAL_TITLE_FIELD_CONTAINER = '.bb-dialog .title-input-container'
MODAL_TITLE_FIELD_LABEL = '{} .export-dialog-label'.format(MODAL_TITLE_FIELD_CONTAINER)
MODAL_TITLE_FIELD_INPUT = '{} ~ div input'.format(MODAL_TITLE_FIELD_LABEL)
MODAL_TITLE_FIELD_RESET = '{} span'.format(MODAL_TITLE_FIELD_CONTAINER)
MODAL_LR_COLUMN_SEARCH_BOX = '.search-filter'
MODAL_LR_COLUMN_SEARCH_BOX_INPUT = '{} input'.format(MODAL_LR_COLUMN_SEARCH_BOX)
MODAL_LR_COLUMN_SEARCH_BOX_SEARCH_ICON = '{} .fa-search'.format(MODAL_LR_COLUMN_SEARCH_BOX)
MODAL_LR_COLUMN_SEARCH_BOX_CLEAR_BUTTON = '{} .fa-close'.format(MODAL_LR_COLUMN_SEARCH_BOX)
MODAL_LR_COLUMNS_LIST = '.export-dialog-columns-list'
MODAL_LR_COLUMN_LABEL = '{} .column-label'.format(MODAL_LR_COLUMNS_LIST)
MODAL_LR_SELECTED_COLUMN_LABEL = '{}.selected'.format(MODAL_LR_COLUMN_LABEL)
MODAL_LR_NOT_SELECTED_COLUMN_LABEL = '{}:not(.selected)'.format(MODAL_LR_COLUMN_LABEL)
MODAL_LR_COLUMN_SELECTION_LINKS_WRAPPER = '.column-selection-links-wrapper'
MODAL_LR_COLUMN_SELECTION_OPTIONS = '{} div'.format(MODAL_LR_COLUMN_SELECTION_LINKS_WRAPPER)
MODAL_LR_COLUMN_SELECTION_LINK = '.export-dialog-link'
MODAL_OK_BUTTON = '{} button.ok-button'.format(MODAL_DIALOG_BOTTOM)
MODAL_OK_BUTTON_DISABLED = '{}.disabled'.format(MODAL_OK_BUTTON)
MODAL_CANCEL_BUTTON = '{} button.link-button'.format(MODAL_DIALOG_BOTTOM)

# Selectors specific to Export LR Dialog
EXPORT_DIALOG_COMPOUNDS = '.bb-dialog-body .radio-group:nth-child(2)'
EXPORT_DIALOG_COMPOUNDS_LABEL = '{} .radio-group-label'.format(EXPORT_DIALOG_COMPOUNDS)
EXPORT_DIALOG_COMPOUNDS_ALL = '{} .radio-button:first-child'.format(EXPORT_DIALOG_COMPOUNDS)
EXPORT_DIALOG_COMPOUNDS_ALL_UNCHECKED = '{} input[value="All"] + span'.format(EXPORT_DIALOG_COMPOUNDS_ALL)
EXPORT_DIALOG_COMPOUNDS_ALL_CHECKED = '{} input[value="All"]:checked + span'.format(EXPORT_DIALOG_COMPOUNDS_ALL)

EXPORT_DIALOG_COMPOUNDS_CURRENTLY_SELECTED = '{} .radio-button:last-child'.format(EXPORT_DIALOG_COMPOUNDS)
EXPORT_DIALOG_COMPOUNDS_CURRENTLY_SELECTED_UNCHECKED = '{} input[value^="Currently Selected"] + span'\
    .format(EXPORT_DIALOG_COMPOUNDS_CURRENTLY_SELECTED)
EXPORT_DIALOG_COMPOUNDS_CURRENTLY_SELECTED_CHECKED = '{} input[value^="Currently Selected"]:checked + span'\
    .format(EXPORT_DIALOG_COMPOUNDS_CURRENTLY_SELECTED)

EXPORT_DIALOG_COLUMNS = '.bb-dialog-body .radio-group:nth-child(3)'
EXPORT_DIALOG_COLUMNS_LABEL = '{} .radio-group-label'.format(EXPORT_DIALOG_COLUMNS)
EXPORT_DIALOG_COLUMNS_ALL = '{} .radio-button:first-child'.format(EXPORT_DIALOG_COLUMNS)
EXPORT_DIALOG_COLUMNS_ALL_UNCHECKED = '{} input[value="All"] + span'.format(EXPORT_DIALOG_COLUMNS_ALL)
EXPORT_DIALOG_COLUMNS_ALL_CHECKED = '{} input[value="All"]:checked + span'.format(EXPORT_DIALOG_COLUMNS_ALL)

EXPORT_DIALOG_COLUMNS_CHOOSE_SUBSET = '{} .radio-button:last-child'.format(EXPORT_DIALOG_COLUMNS)
EXPORT_DIALOG_COLUMNS_CHOOSE_SUBSET_UNCHECKED = '{} input[value^="Choose Subset"] + span'\
    .format(EXPORT_DIALOG_COLUMNS_CHOOSE_SUBSET)

EXPORT_DIALOG_DISABLED_CHECKED_COLUMN = '{} .disabled .selected'.format(MODAL_LR_COLUMNS_LIST)

# Selectors specific to Duplicate LR Dialog
DUPLICATE_LR_FOLDER_DROPDOWN = '.export-dialog-dropdown'
DUPLICATE_LR_RADIO_GROUP_LABEL = '.radio-group .radio-group-label'
DUPLICATE_LR_RADIO_BUTTON_LABEL = 'label.radio-button'
DUPLICATE_LR_COLUMN_SELECTION_WARNING_MSG = '.column-selection-warning'
DUPLICATE_LR_COLUMN_SELECTION_WARNING_MSG_UNDO_LINK = '{} .undo-link'.format(DUPLICATE_LR_COLUMN_SELECTION_WARNING_MSG)
