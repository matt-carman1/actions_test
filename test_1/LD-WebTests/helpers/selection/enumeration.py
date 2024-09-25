from helpers.selection.general import MENU_ITEM

OLD_ENUMERATION_ICON = '#enumeration-runner-panel_header-iconEl'
X_BTN_INNER = '.x-btn-inner'

EXIT_ENUMERATION_BUTTON = '.exit-enumeration-button'
NEW_ENUMERATION_ICON = '.select-enumeration-type'
NEW_ENUMERATION_WIZARD_WINDOW = ".enumeration-wizard:not([class*='hidden'])"
ENUMERATION_HEADER = ".enumeration-header"

ENUMERATION_PROCEED_BUTTON = "{} .enumeration-button-bar .enumeration-proceed".format(NEW_ENUMERATION_WIZARD_WINDOW)
ENUMERATION_PROCEED_BUTTON_DISABLED = '{} .enumeration-button-bar .enumeration-proceed.big-button.bb-dialog-button.disabled'.format(
    NEW_ENUMERATION_WIZARD_WINDOW)
ENUMERATION_ACTIVE_TAB = "{} .enumeration-tab.active".format(NEW_ENUMERATION_WIZARD_WINDOW)
ENUMERATION_TAB = "{} .enumeration-tab".format(NEW_ENUMERATION_WIZARD_WINDOW)
ENUMERATION_STRUCTURE_COUNT = ".enumeration-wizard:not([class*='hidden']) .structures-pane-body " \
                                       ".compound-list-container:{} .enumeration-emphasize+span"
ENUMERATION_STATUS = '.enumeration-status div'
ENUMERATION_SOURCE_PICKER_LIST_LABEL = "{} .source-picker-list li label".format(NEW_ENUMERATION_WIZARD_WINDOW)
REACTION_PICKER_LIST = ".reaction-picker-list .reaction-title em"
REACTION_FILTER_INPUT = '.reaction-picker-filter .reaction-filter-input-wrapper input'
REACTION_EDIT_PICKER = '.reaction-picker-preview .edit-button'
ENUMERATION_BACK_BUTTON = '.enumeration-back'

ENUMERATION_SIDEBAR_TAB = "{} .sidebar .enumeration-tab".format(NEW_ENUMERATION_WIZARD_WINDOW)
ENUMERATION_CHOOSE_LIVE_REPORT_LINK = "{} .choose-live-reports .enumeration-link".format(NEW_ENUMERATION_WIZARD_WINDOW)
ENUMERATION_SCAFFOLD_SKETCHER = '#enumeration-scaffold-sketcher'
ENUMERATION_RGROUP_SKETCHER = '#enumeration-rgroup-sketcher'
ENUMERATION_REACTANT_SKETCHER = '#enumeration-reactant-sketcher'
CLOSE_SKETCHER_DIALOG = '.bb-dialog .link-button'
ENUMERATION_SOURCE_PICKER = '.choose-live-reports .enumeration-link'
ENUMERATION_NEW_SKETCH_BUTTON = '.source-picker-list input[value="sketched"]:checked'
REACTION_ENUM_IMPORT_FROM_FILE = '.source-picker-list input[accept=".csv,.sdf,.sd"].file-picker'

ENUMERATION_REACTANT_COLUMNS_DIALOG = '.reactant-columns-dialog'
ENUMERATION_CLOSE_BUTTON = '.enumeration-close'

ENUMERATION_REACTION_SKETCHER = '#enumeration-reaction-sketcher'
ENUMERATION_LINKS = '.enumeration-link'
SAVE_REACTION_NAME_INPUT = '.form-row-input input[name="name"]'
SAVE_REACTION_DESCRIPTION_INPUT = '.form-row-input input[name="description"]'
SAVE_REACTANT_A_NAME_INPUT = '.form-row-input input[name="namedClasses[0]"]'
SAVE_REACTANT_B_NAME_INPUT = '.form-row-input input[name="namedClasses[1]"]'
REACTION_PREVIEW = '.reaction-picker-preview'
REACTANT_NAME_INFO = '.compound-list-container .enumeration-emphasize'
SAVE_REACTION_CANCEL_LINK = '.bb-dialog-bottom .link-button'
CREATE_NEW_OVERWRITE_OK = ".ok-button"
DELETE_REACTION = ".reaction-delete-button"

# Reaction Enumeration extra columns dialog
EXTRA_COLUMNS_LINKS = '.links-container a.link'
EXTRA_COLUMNS_REACTANT_SELECTION = '.reactant-columns-buttons .enumeration-tab'
EXTRA_COLUMNS_CHECKBOXES = '.reactant-extra-column'
EXTRA_COLUMNS_CHECKBOX_CHECKED = '.checkbox-list input:checked + span'
ENUMERATION_EXTRA_COLUMN_CHECKED = '.checkbox-list input:checked ~ span .reactant-extra-column'
ENUMERATION_EXTRA_COLUMN_APPLY_ALL = '.reactant-columns-buttons label'
ENUM_EXTRA_COLUMN_APPLY_ALL_CHECKED = '.reactant-columns-buttons label input:checked + span'

ENUMERATION_CSV_DIALOG_ID_DROPDOWN = '.bb-dialog-body .form-row:nth-child(4) select'

RGROUP_ENUM_ACTIVE_LR_RADIO = '.source-picker-list input[value="active-live-report"]'
RGROUP_ENUM_ACTIVE_LR_DROPDOWN = '.source-picker select'
RGROUP_ENUM_ACTIVE_LR_COMPOUND_ID = RGROUP_ENUM_ACTIVE_LR_DROPDOWN + " option[value={}]"
RGROUP_ENUM_TARGET_LR_DROPDOWN = '.enumeration-wizard .wizard-body .structures-pane .footer .live-report-target-area .target-lr-picker'
RGROUP_ENUM_SELECT_TARGET_LR = '.bb-menu.open .bb-menu-item'
RGROUP_COMPOUND_CONTAINER_STRUCTURES = '.compound-list-container:{} .compound-list div[role="rowgroup"] .structure:{} img'
RGROUP_ENUM_ADD_BUTTON = '.ok-button.big-button.bb-dialog-button'
RGROUP_ENUM_CANCEL_BUTTON = '.link-button.big-button.bb-dialog-button'
RGROUP_CONTAINERS = '.compound-list-container'
RGROUP_CONTAINER_TAG = REACTANT_NAME_INFO
R_GROUPS = '.compound-list div[role="rowgroup"] .structure img'
