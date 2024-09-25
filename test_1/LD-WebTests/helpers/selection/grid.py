"""
CSS Selector constants for interacting with the grid
"""
# Class of the button to switch to Grid View
GRID_ICON = '.grid-icon'
# Classes of the grid icon when it is active
GRID_ICON_ACTIVE = '.grid-icon.active'

# NOTE (pradeep): The top header or the column group header is the first row wrapper in FDT.
GRID_HEADER_TOP = ".grid-header .fixedDataTableLayout_rowsContainer > .fixedDataTableRowLayout_rowWrapper:nth-child(1) .fixedDataTableLayout_header"
GRID_HEADER_TOP_CELLS = '{} .public_fixedDataTableCell_cellContent'.format(GRID_HEADER_TOP)
# NOTE (pradeep): The bottom header or the sub-column header is the second row wrapper in FDT.
# This appears when columns are grouped. Contains sub-column header cells.
GRID_HEADER_BOTTOM = ".grid-header .fixedDataTableLayout_rowsContainer > .fixedDataTableRowLayout_rowWrapper:nth-child(2) .fixedDataTableLayout_header"
"""
Get the header cell for a particular column.

NOTE: This selector needs to be formatted with the name of the column, e.g.

    GRID_HEADER_SELECTOR_.format("I am the column name")
"""
GRID_HEADER_SELECTOR_ = '.fixedDataTableLayout_header div[data-title="{}"]'

GRID_HEADER_CELL = '.grid-header-cell'

GRID_GROUP_HEADER_CELL = '.group-header-cell'

GRID_COLUMN_HEADER_REORDER_CONTAINER = '.fixedDataTableCellLayout_columnReorderContainer'

GRID_HEADER_READ_ONLY_FFC_LOCK_ICON = 'div[data-title="{}"] i.fa-lock'

GRID_HEADER_READ_ONLY_FFC_UNLOCK_ICON = 'div[data-title="{}"] i.fa-unlock'
"""
The dropdown menu for a column of the grid. Note that a hover must be simulated
before this will match any element.
"""
GRID_HEADER_DROPDOWN_MENU = \
    '{}:hover .grid-header-cell-menu-trigger'.format(GRID_HEADER_CELL)
GRID_COLUMN_MENU_OPEN = '.grid-column-menu .bb-menu.open'

GRID_COLUMN_HEADER_SORT_ICON_ = '.grid-column-header-multi-sort-{}'

GRID_HEADER_ALIGNMENT_TEXT = '.alignment-text'

GRID_ROWS_CONTAINER = '.main-table .fixedDataTableLayout_rowsContainer'
GRID_ROW = '.grid-row'
GRID_ROW_SELECTION_CELL = '.selection-cell'
GRID_SCROLLBAR_THUMB = '.main-table .ScrollbarLayout_mainHorizontal .ScrollbarLayout_face'

GRID_ALL_ROWS_CHECKBOX = '.grid-header .grid-selection-checkbox'
GRID_TILE_ALL_ROWS_CHECKBOX = '.selection-checkbox-div input[type="checkbox"]'
GRID_ALL_ROWS_CHECKBOX_INPUT = '{} input'.format(GRID_ALL_ROWS_CHECKBOX)
GRID_ROW_ID_ = '.grid-row-id-{}'
GRID_ROW_ID_HOVERED_ = '.grid-row-id-{}:hover'
GRID_ROW_CHECKBOX_ = '.grid-row-id-{} .checkbox-container'
GRID_ROW_CHECKBOX_INPUT = '.grid-row-id-{} .checkbox-container input'

GRID_FIXED_COLUMN_GROUP = \
    '.fixedDataTableCellGroupLayout_cellGroupWrapper:first-child'

GRID_CELL_COLUMN_ID_ = '.grid-cell-column-{}'
GRID_CELL_ASSAY_SUBCELL = '.grid-cell-type-assay-subcell'
GRID_COMPOUND_ID_CELLS = ('.grid-cell-type-id ' '.public_fixedDataTableCell_cellContent')
GRID_PENDING_CELLS = '.grid-cell-wrapper .pending-cell'
GRID_PENDING_CELLS_IN_COLUMN = '{}{}'.format(GRID_CELL_COLUMN_ID_, GRID_PENDING_CELLS)
GRID_FDT_CELL_WRAPPER_1 = '.public_fixedDataTableCell_wrap1'

GRID_PROGRESS_NOTIFICATION = '.notification-area .notification-progress'
GRID_ERROR_NOTIFICATION = '.notification-area .notification-error'
GRID_NOTIFICATION_LINK = '{} a'.format(GRID_PROGRESS_NOTIFICATION)
GRID_ERROR_NOTIFICATION_LINK = '{} a'.format(GRID_ERROR_NOTIFICATION)
GRID_INFO_NOTIFICATION = '.notification-area .notification-info'
GRID_TIP_NOTIFICATION = '.notification-area .notification-tip'

GRID_FOOTER = '.grid-footer'
GRID_FOOTER_ROW_ALL_COUNT = '.grid-footer-row-metadata .all-count'
GRID_FOOTER_ROW_HIDDEN_COUNT = '.grid-footer-row-metadata .hidden-count'
GRID_FOOTER_ROW_HIDDEN_LINK = '{} a'.format(GRID_FOOTER_ROW_HIDDEN_COUNT)
GRID_FOOTER_ROW_FILTERED_COUNT = '.grid-footer-row-metadata .filtered-count'
GRID_FOOTER_ROW_SELECTED_COUNT = '.grid-footer-row-metadata .selected-count'
GRID_FOOTER_COLUMN_ALL_COUNT = '.grid-footer-column-metadata .all-count'
GRID_FOOTER_COLUMN_HIDDEN_COUNT = '.grid-footer-column-metadata .hidden-count'
GRID_FOOTER_COLUMN_HIDDEN_LINK = '{} a'.format(GRID_FOOTER_COLUMN_HIDDEN_COUNT)
GRID_FOOTER_COPYRIGHT = '.grid-footer-copyright'
GRID_FOOTER_ROW_DISPLAYED_COUNT = '.grid-footer-row-metadata .displayed-count'

GRID_MENU_ITEM_DISABLED = '.bb-menu-item.disabled'
GRID_MENU_ITEM_NOT_DISABLED = '.bb-menu-item:not(.disabled)'
GRID_NOTIFICATION_AREA = '.notification-area'
FROZEN_ROWS_ = '.frozen-table {}'.format(GRID_ROW_ID_)
GRID_ROW_MENU = '.bb-menu.open'
GRID_EXPAND_BUTTON_ = '{} {} .non-aggregate-assay-split'.format(GRID_ROW_ID_, GRID_CELL_COLUMN_ID_)
GRID_ROW_COLUMN_ = '{} {}'.format(GRID_ROW_ID_, GRID_CELL_COLUMN_ID_)
GRID_COMPOUND_IMAGE_SELECTOR_ = '{} .zoom-image img'.format(GRID_ROW_ID_)
GRID_COMPOUND_STRUCTURE_SMILES = '.structure-smiles'

GRID_FIND_PANEL = '#gridFind-panel'
GRID_FIND_BUTTON = '#gridFind-button'
GRID_FIND_INPUT = '#gridFind-input'
GRID_FIND_NEXT_BUTTON = '#gridFind-next-button'
GRID_FIND_PREV_BUTTON = '#gridFind-prev-button'
GRID_FIND_CLOSE_BUTTON = '#gridFind-close-button'
GRID_FIND_MATCH_COUNT = '#gridFind-match-count'
GRID_FIND_ORANGE_MARK = '.gridFind-mark-orange'
GRID_FIND_YELLOW_MARK = '.gridFind-mark-yellow'
GRID_FIND_TOTAL_MATCHES = 'mark[class*="gridFind-mark"]'

AGGREGATE_TOOLTIP = '.aggregate-tooltip'
AGGREGATE_TOOLTIP_STRIPE = '.aggregate-celltip-stripe'
AGGREGATE_TOOLTIP_TEXT = '.aggregate-celltip-main-label .aggregate-celltip-text'
AGGREGATE_CELLTIP_TEXT = '.aggregate-celltip'

READ_ONLY_FFC_CELL_TOOLTIP = 'div.description-ffc-tooltip'

PYMOL_VIEW_TEXT = '.pymol-view-text'

ROW_SELECTION_CHECKBOX_DROPDOWN = '.selection-checkbox-div .down-arrow'
ROW_SELECTION_MENU = '.selection-menu'
SELECTED_ID = '.grid-cell-type-id .selected-cell'
ROW_SELECTION_CHECKBOX = '.grid-header-cell input'
ROW_INDEX = '.row-index'
ROW_RATIONALE_CELL = '{} .rationale-cell'.format(GRID_ROW_ID_)
ROW_RATIONALE_CELL_EDIT_BUTTON = "{} div[class='rationale-edit']".format(ROW_RATIONALE_CELL)

SELECTED_CELL = '.selected-cell'
SELECTED_CELL_LEFT_BORDER = '{}.left-border'.format(SELECTED_CELL)

GRID_LIVEREPORT_COLUMNS_IMAGE_PATH = ".fixedDataTableLayout_rowsContainer >div:nth-child(2) >div"


class ColumnMenuOptionName:
    VIEW_FORMULA = 'View Formula…'
    EDIT_FORMULA = 'Edit Formula…'
    REMOVE = 'Remove'


class Footer:
    # footer_key
    ROW_ALL_COUNT_KEY = ROW_ALL_COUNT_LOTS_KEY = ROW_ALL_COUNT_POSE_KEY = ROW_ALL_COUNT_SALTS_KEY = \
        ROW_ALL_COUNT_LOT_SALTS_KEY = 'row_all_count'
    ROW_HIDDEN_COUNT_KEY = 'row_hidden_count'
    ROW_FILTERED_COUNT_KEY = 'row_filtered_count'
    ROW_SELECTED_COUNT_KEY = 'row_selected_count'
    COLUMN_ALL_COUNT_KEY = 'column_all_count'
    COLUMN_HIDDEN_COUNT_KEY = 'column_hidden_count'
    # footer value
    ROW_ALL_COUNT_VALUE = '{} Total Compounds'
    ROW_ALL_COUNT_LOTS_VALUE = '{} Total Lots'
    ROW_ALL_COUNT_POSE_VALUE = '{} Total Poses'
    ROW_ALL_COUNT_SALTS_VALUE = '{} Total Salts'
    ROW_ALL_COUNT_LOT_SALTS_VALUE = '{} Total Lot Salts'
    ROW_HIDDEN_COUNT_VALUE = '{} Hidden'
    ROW_FILTERED_COUNT_VALUE = '{} After Filter'
    ROW_SELECTED_COUNT_VALUE = '{} Selected'
    COLUMN_ALL_COUNT_VALUE = '{} Columns'
    COLUMN_HIDDEN_COUNT_VALUE = '{} Hidden'
    # Footer value with None
    ROW_ALL_COUNT_VALUE_NONE = ROW_ALL_COUNT_LOTS_VALUE_NONE = ROW_HIDDEN_COUNT_VALUE_NONE = \
        ROW_FILTERED_COUNT_VALUE_NONE = ROW_SELECTED_COUNT_VALUE_NONE = COLUMN_ALL_COUNT_VALUE_NONE = \
        COLUMN_HIDDEN_COUNT_VALUE_NONE = 'None'
