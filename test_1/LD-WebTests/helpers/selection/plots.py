# Info icon (on hover shows rpe related message).
# located at lower right hand corner of plot panel
INFO_CIRCLE = '.fa.fa-info-circle'
PLOT_WARNING = '.plot-warning[title="{}"]'

ADD_RADAR_AXIS_BUTTON = '#add-radar-axis-button'
ADVANCED_OPTIONS_BUTTON = '#spg-advanced-options-btn'
ADVANCED_OPTIONS_COLLAPSE = '.spg-data-options-collapse'
BIN_COUNT_BUTTON = '#spg-bin-group label.bin-count span:first-of-type'

CHART = '.chart'
CHART_AXIS_TITLE = '.highcharts-axis-title'
CHART_XAXIS_LABEL = '.highcharts-xaxis-labels'
CHART_YAXIS_LABEL = '.highcharts-yaxis-labels'
CHART_XAXIS_TITLE = '.highcharts-xaxis {}'.format(CHART_AXIS_TITLE)
CHART_YAXIS_TITLE = '.highcharts-yaxis {}'.format(CHART_AXIS_TITLE)
COLOR_BY_AXIS_SELECT = '#spg-colorby-axis-select'
COLOR_BY_COLORING_RULE = '.spg-colorby-axis-tooltip a'
GADGET_TAB_NUMBER = 'div.tab-list ul li:nth-child({}) a'
HEATMAP_COLUMN_PICKER = '#heatmap-column-picker .spg-series-header'
HEATMAP_COLUMN_PICKER_ITEM = \
    '#heatmap-column-picker .multiselect-unselected-items li:nth-child({}) .heatmap-column-picker-checkbox'
CUSTOM_BINNING_ACTIVE_RULE_TYPE_LABEL = '#spg-bin-control-column-type-toggle label.active'
CUSTOM_BINNING_BUTTON = '#spg-bin-group .spg-bin-options .spg-bin-options-item label.custom-bins'
ONE_PER_VALUE_BINNING_BUTTON = '#spg-bin-group .spg-bin-options .spg-bin-options-item label.one-per-value'
CUSTOM_BINNING_RULE_TYPE_TOGGLE = '#spg-bin-control-column-type-toggle'
CUSTOM_BINNING_RULE_TYPE_LABEL = '#spg-bin-control-column-type-toggle label[data-rule-type="{}"]'
HEATMAP_COLUMN_PICKER_UNSELECTED_ITEM_CHECKBOX = \
    '#heatmap-column-picker .multiselect-unselected-items li[data-column-name="{}"] .heatmap-column-picker-checkbox'
HEATMAP_COLUMN_PICKER_SELECTED_ITEM_COLOR_LINK = \
    '#heatmap-column-picker .multiselect-selected-items li[data-column-name="{}"] .heatmap-column-picker-link'
HEATMAP_CELL = '.highcharts-series-group path'
HEATMAP_SELECTED_CELL = '.highcharts-series-group path.highcharts-point-select'
HISTOGRAM_BAR = '.highcharts-series-0:not(.highcharts-legend-item) rect'
HISTOGRAM_BARS = 'g.highcharts-series rect'
HISTOGRAM_BAR_BY_ID = '.highcharts-point[id*="{}"]'
HIST_BAR_01 = '.highcharts-series-0:not(.highcharts-legend-item) rect:nth-child(1)'
HIST_BAR_02 = '.highcharts-series-0:not(.highcharts-legend-item) rect:nth-child(2)'
HIST_BAR_03 = '.highcharts-series-0:not(.highcharts-legend-item) rect:nth-child(3)'
OPTIONS_MODE_ADVANCED = '.options-mode-advanced'
OPTIONS_MODE_BASIC = '.options-mode-basic'
PIE_SLICE = '.highcharts-series-0 > .highcharts-point'
PIE_SLICE_BY_ID = '.highcharts-series-0 > .highcharts-point[id*="{}"]'
PIE_DISPLAY_RANGES = '.highcharts-data-label'
PLOT_OPTIONS_DIALOG_CLOSE_BUTTON = '.plot-options-dialog .ok-button'
PLOT_OPTIONS_PANEL = '.plot-options-panel'
RADAR_AXIS = '.highcharts-xaxis-grid > path'
RADAR_AXIS_LABEL = '.highcharts-axis-labels.highcharts-xaxis-labels > text'
RADAR_AXIS_SELECT = '#axis-row-{} .axis-column-select'
RADAR_LEGEND_ITEM = 'g.highcharts-legend .highcharts-legend-item text'
RADAR_LINE = '.highcharts-series-group > .highcharts-line-series:not(.highcharts-tracker)'
RADAR_LINE_TRACKER = '.highcharts-series-group > .highcharts-line-series.highcharts-tracker'
VISUALIZATION_BOX = '.visualization-box'
VISUALIZATION_HEATMAP = '.visualization-heatmap'
VISUALIZATION_HISTOGRAM = '.visualization-histogram'
VISUALIZATION_PIE = '.visualization-pie'
VISUALIZATION_RADAR = '.visualization-radar'
VISUALIZATION_SCATTER = '.visualization-scatter'
ERROR_BANDS = '.highcharts-series-group > .highcharts-arearange-series  > path.highcharts-area'
ERROR_BANDS_CHECKBOX = '.error-bands'
ERROR_BANDS_CHECKBOX_DISABLED = '.error-bands > .disabled'
ERROR_BANDS_SIZE = '.overlay .details-row div:nth-child(2) input'
LEGEND = '.spg-legend'
LEGEND_SELECT = '#legend-mode-select'
NUMERIC_RULE_MIN_BOX = '.spg-rule:nth-child({}) .numeric-range-input-minimum input'
NUMERIC_RULE_MAX_BOX = '.spg-rule:nth-child({}) .numeric-range-input-maximum input'
SAVED_VISUALIZATIONS = '.load-saved .gadget-list .gadget-item .gadget-title'
REGRESSION_LINE_CHECKBOX = '.regression-line'
REGRESSION_LINE_INFO = '.highcharts-label text'
REGRESSION_LINE = '.highcharts-series-group > .highcharts-spline-series > path[stroke="#FF0000"]'
RULE_NAME = 'div.spg-rule:nth-child({}) a.bin-name'
RULE_NAME_INPUT = 'div.spg-rule:nth-child({}) input.rename-input'
SCATTER_POINTS = '.highcharts-markers path.highcharts-point'
# keep stroke-width in sync with plotConsts.SELECTED_POINT_BORDER_WIDTH
SCATTER_SELECTED_POINTS = '.highcharts-markers path.highcharts-point[stroke-width="2"]'
HEATMAP_POINT = '.highcharts-heatmap-series > .highcharts-point'
SPG_ADD_BIN_RULE = 'div.spg-bin-options button.spg-add-rule'
SPG_BIN_HEADER = '.spg-bin-header'
SPG_BIN_OPTIONS = '.spg-bin-options'
SPG_PLOT_AREA = '#spg-plot-area'
SPREADSHEET_HEADER = '#spreadsheet-header'
# tooltip section
TOOLTIP_BIN_COUNT = '.plot-tooltip .bin-count'
TOOLTIP_COMPOUND_ID = '.plot-tooltip .corporate-id'
TOOLTIP_FIELD_LIST = '.field-list'
TOOLTIP_MODE_RADIO = '#tooltip-options-radio-container input[value="{}"] + span'
PLOT_TOOLTIP = '.plot-tooltip'
X_AXIS_SELECT = '#spg-x-axis-select'
Y_AXIS_SELECT = '#spg-y-axis-select'
PLOT_OPTIONS_TAB = '{} .tab-link'.format(PLOT_OPTIONS_PANEL)
PLOT_OPTIONS_TAB_ACTIVE = '{} .active-tab-link'.format(PLOT_OPTIONS_PANEL)
# keep the tab names in sync with bb.app.plots.enums.DialogOptionsTab
PLOT_OPTIONS_TAB_NAME_DATA = 'Data'
PLOT_OPTIONS_TAB_NAME_STYLE = 'Style'
PLOT_OPTIONS_TAB_NAME_TOOLTIP = 'Tooltip'
PLOT_OPTIONS_TAB_NAME_BIN = 'Bin'
PLOT_OPTIONS_TAB_NAME_REFERENCE_AREA = 'Reference Area'
EQUAL_BINNING_BUTTON = '.spg-bin-options-item:first-of-type .dark-control-indicator'
EQUAL_BINNING_INPUT = '.spg-bin-count'

# Selector related to plot options
SHAPE_BY = '#spg-shapeby-axis-select'
SELECT_SHAPE_BY = 'div[id="spg-rule-shape-selector"] button[data-shape="{}"]'
PLOT_OPTIONS_SHAPE_SELECTION_BUTTON = '//div[text()="Default"]//preceding::div[@class="spg-rule-shape"]'
SELECT_BY_RADIO = '//span[text()="{}"]/preceding-sibling::span'
PLOT_OPTIONS_ADD_RULE = 'button[id="shapeby-add-rule"]'
PLOT_OPTION_SHAPE_LAST_CHILD_MIN = ".spg-rule:last-child .numeric-range-input-minimum input"
PLOT_OPTION_SHAPE_LAST_CHILD_MAX = ".spg-rule:last-child .numeric-range-input-maximum input"
SCATTER_PATHS = '.highcharts-series-group path'
PLOT_OPTIONS_STYLE_NTH_CHILD_SHAPE = '.spg-rule:last-child  path'

BOX_PLOT_BOX_POINT = 'g[id^="plots"][id$="{}"]'
BOX_PLOT_POINT = 'path.highcharts-point[id*={}]'

# advanced options panel - Style tab
ADD_OVERLAY_BUTTON = 'button[name="add-overlay-button"]'
OVERLAY_OPTION = '.add-overlay-button-container .bb-menu-item:nth-child({})'
TRASH_BUTTON = '.overlay .trash-button:nth-child(1)'

# advanced options panel - Data tab
DATA_TAB_X_AXIS_SELECT = '.active-tab-content select#spg-x-axis-select'

FIRST_TAB_TITLE = '.tab-title:nth-child(1)'
