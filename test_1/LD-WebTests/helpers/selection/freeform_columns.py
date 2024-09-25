class FreeformColumnDialog:
    """
    This class contains selectors for the Freeform Column Dialog.
    """
    # General
    FFC_EDIT_WINDOW = '.freeform-window'
    FFC_DIALOG_CLOSE = '.close'
    FFC_WINDOW = '#freeform-window-container'
    FFC_NAME = '#freeform-name-field'
    FFC_TYPE = '#freeform-type-field'
    FFC_CONSTRAINT_ANY = '.freeform-constraint-field-any'
    FFC_DESCRIPTION = '#freeform-description-field'
    FFC_PUBLISHED_CHECKBOX = 'input[name="editedPublished"] + span'
    FFC_READ_ONLY_CHECKBOX = 'input[name="editedReadOnly"] + span'
    FFC_READ_ONLY_CHECKBOX_CHECKED = 'input[name="editedReadOnly"]:checked + span'
    FFC_READ_ONLY_ALLOWLIST_SEARCH = 'input.read-only-search-input'
    FFC_READ_ONLY_ALLOWLIST_VALUES = 'li.freeform-picklist-value'
    FFC_READ_ONLY_ALLOWLIST_FIRST_VALUE = '{} label'.format(FFC_READ_ONLY_ALLOWLIST_VALUES)
    FFC_READ_ONLY_ALLOWLIST_CHECKED_VALUE = '{} input:checked + span'.format(FFC_READ_ONLY_ALLOWLIST_VALUES)
    FFC_READ_ONLY_ALLOWLIST_DISABLED_VALUE = '{} input:disabled + span'.format(FFC_READ_ONLY_ALLOWLIST_VALUES)
    FFC_ERROR_CONTAINER = '#freeform-window-error-container'

    # Picklist Related
    FFC_PICKLIST_FIELD = '.freeform-constraint-field-picklist'
    FFC_PICKLIST_ACTION = '.freeform-picklist-action'
    FFC_PICKLIST_VALUE_SELECT = '.freeform-picklist-value'
    FFC_MULTISELECT_IN_PICKLIST = '#freeform-multiple-values-field'

    # Add Column Value Dialog Related
    FFC_PICKLIST_VALUE_PLACEHOLDER = '#cell-edit-value-field'
    FFC_CELL_EDIT_WINDOW = '.cell-edit-window'
    FFC_CALENDAR_ELEMENT = '.date-picker'
    FFC_CALENDAR_PICK = '.rc-calendar-date'


class FreeformColumnCellEdit:
    """
    This class contains selectors for the Freeform Column Cell Edit.
    """
    # General
    FFC_EDIT_ICON = '.freeform-icon'
    FFC_CELL_EDIT_SAVE = '.editable-cell-save'
    FFC_EDIT_CANCEL_BUTTON = 'button.editable-cell-cancel'

    # Picklist Cell Related
    FFC_PICKLIST_VALUES = '.edit-mode select option'

    # Attachment Cell Related
    FILE_FFC_ATTACHMENT_ICON = '.freeform-cell.attachment .attachment-icon'
    FILE_FFC_ATTACHMENT_ICON_HAS_ATTACHMENT = FILE_FFC_ATTACHMENT_ICON + '.has-attachment[title="{}"]'
    # Usage example: FILE_FFC_ATTACHMENT_ICON_HAS_ATTACHMENT.format('410.svg') #
    FILE_FFC_ATTACHMENT_ICON_HAS_ATTACHMENT_IMAGE = '.freeform-cell.attachment.grid-image-cell.has-attachment img'
    FILE_FFC_BUTTON_TRAY = '.button-tray'
    FILE_FFC_POP_OUT_ICON = '.traybutton.attachment-open.popout-icon'
    FILE_FFC_PENCIL_ICON = '.traybutton.attachment-upload.pencil-icon'
    FILE_FFC_DELETE_ICON = '.traybutton.attachment-clear.trash-icon'

    # Boolean Cell Related
    FFC_BOOLEAN_VALUE = '.freeform-cell-value'
    FFC_BOOLEAN_OPTION = '.freeform-cell-boolean-option[data-value="{}"]'


class FreeformColumnBulkEdit:
    """
    This class contains selectors for the Freeform Column Bulk Edit.
    """
    FFC_CELL_EDIT_VALUE_FIELD = '#cell-edit-value-field.freeform-field'
    COLUMN_DROPDOWN = 'select#cell-edit-copy-column-picker'
    COLUMN_DROPDOWN_OPTIONS = "{} option".format(COLUMN_DROPDOWN)
    RPE_EDIT_WARNING = '#cell-edit-rpe-source-column-warning-div.edit-warning'
    FFC_CELL_EDIT_BULK_CHECKBOX = '#cell-edit-bulk-checkbox'
    FFC_CELL_EDIT_BULK_SAVE = '#cell-edit-save-btn'
    FFC_CELL_EDIT_BULK_CANCEL = '#cell-edit-cancel-btn'


class FreeformColumnCommonErrors:
    """
    This class contains selectors for the Freeform Column Common Errors.
    """
    FFC_VALUE_VALIDATION_ERROR_MESSAGE = '#cell-edit-validation-error-message'
