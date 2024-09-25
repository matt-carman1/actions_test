# ----- 'EDIT EXISTING MULTI-PARAMETER OPTIMIZATION' DIALOG -----#
##### General Settings section #####
MPO_GENERAL_SETTINGS_FORM = '#mpo-general-settings-form'
MPO_NAME_FIELD = '#mpo-name-field'
MPO_DESCRIPTION_FIELD = '#mpo-description-field'

##### Choose Properties section #####
# area to select/add a constituent
MPO_CONSTITUENT_PICKER = '#mpo-constituent-picker'
# columns/constituents in LR list
MPO_CONSTITUENT_PICKER_VALUE = '.mpo-constituent-picker-value'

# gets added constituent list
MPO_CONSTITUENT_BUTTON = '.mpo-added-constituent'
CONSTITUENT_OPTION = MPO_CONSTITUENT_BUTTON + '.menu-option[title="{}"]'

# area to set distribution and values
MPO_CONSTITUENT_FORM = '#mpo-constituent-form'
MPO_VALUE_DISTRIBUTION_DROPDOWN = '#mpo-value-distribution-dropdown'
# numeric input fields
MPO_CONSTITUENT_FIELD = 'input.mpo-constituent-field'
# text input fields
MPO_DROPDOWN_INPUT = '.dropdown-container'
# contains RPE warning message
NON_AVG_COLUMN_NOTICE = '#mpo-nonAvgColumnNotice-container'

MPO_OK_BUTTON = '#mpo-ok-button'
MPO_CANCEL_BUTTON = '[name="mpo-cancel-button"]'

# buttons that appear when hovering over MPO name in D&C Tree
MPO_EDIT = '.big-button.mpo-edit'
MPO_CLONE = '.big-button.mpo-clone'

# ---- Constituent section ----- #
MPO_PROPERTY_WEIGHTS = '.property-weights'
MPO_PROPERTY_WEIGHTS_FORM = '.property-weights-form'
MPO_CONSTITUENT_WEIGHT_EDITOR = '.constituent-weight-editor'

# ----- GRID -----#
# selector for the ! icon in grid that displays rpe message on hover
CELL_TIP_MESSAGE = '.generic-celltip.celltip'
# Shows assay data
MPO_CELLTIP = '.mpo-celltip'

# Delete a constituent
MPO_DELETE_CONSTITUENT = '.mpo-added-constituent .mpo-added-constituent-delete'

# Clone MPO
MPO_CLONE_BUTTON = '.big-button.mpo-clone'

MPO_OK_BUTTON_DISABLED_STATE = '{}.disabled'.format(MPO_OK_BUTTON)
MPO_VALIDATION_ERROR = '#mpo-validation-message'
