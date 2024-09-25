"""
CSS Selectors that apply to tile view
"""
# Class of the button to switch to Tile View
TILE_ICON = '.tile-icon'
# Classes of the tile icon when it is active
TILE_ICON_ACTIVE = '.tile-icon.active'
# The tile
TILE_VIEW_TILE = '.tile-view-tile'
# The column name area in a tile
TILE_VIEW_COLUMN = '.tile-field-name'
# Configure tiles button
CONFIGURE_TILES = '.configure-tiles-button'
# Available columns list item
AVAILABLE_COLUMNS_ITEM = '.available-columns .column-selector-field-list-wrapper li'
# Available columns list item that is not in the Displayed columns
AVAILABLE_COLUMNS_ITEM_NOT_DISPLAYED = '.available-columns .column-selector-field-list-wrapper .visible-column'
# Displayed columns list item
DISPLAYED_COLUMNS_ITEM = '.displayed-columns .column-selector-field-list-wrapper li'
# Button to show the selected columns
SHOW_BUTTON = '.show-button'
# Button to hide the selected columns
HIDE_BUTTON = '.hide-button'
# Increase tile size button
INCREASE_TILE_SIZE = '.decrease-tiles-per-row'

SELECTED_TILE_HEADER = '{}.selected .tile-header'.format(TILE_VIEW_TILE)
TILE_VIEW_DIV = '.tile-view-div'
TILE_BASED_ON_ID_ = '.tile-id-{}'
TILE_VIEW_HEADER = '.tile-view-header'
TILE_VIEW_SELECTION_CHECKBOX = '{} .grid-selection-checkbox'.format(TILE_VIEW_HEADER)
TILE_VIEW_SELECTION_CHECKBOX_INPUT = '{} input'.format(TILE_VIEW_SELECTION_CHECKBOX)
TILE_FIELD_NAME_ = '{} {}'.format(TILE_BASED_ON_ID_, TILE_VIEW_COLUMN)
SELECTED_TILE_BASED_ON_ID_ = '{}.selected'.format(TILE_BASED_ON_ID_)
TILE_HEADER = '{} .tile-header'.format(TILE_VIEW_TILE)
TILE_CONTAINER = ".lm_content div[role='grid']"
FROZEN_TILE = '.tile-id-{}.frozen'
RATIONALE_CELL = ".tile-id-{} .rationale-cell"
RATIONALE_CELL_EDIT_BUTTON = "{} div[class='rationale-edit']".format(RATIONALE_CELL)
