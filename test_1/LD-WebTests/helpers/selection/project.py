"""
Selections in the project modal.
"""
from library import dom
"""
List available project elements. Note that there is not a class on the
"Project name" column to distinguish from therapeutic area, so we are using
an nth-child selector for now.

TODO: Add classes to the project picker.
"""
PROJECT_LIST_ITEMS = '.project-picker-search-column:nth-child(2) li'
"""
Modal that appears when a user attempts to open a project to which they do not
have access.
"""
INVALID_PROJECT_MODAL = '.invalidText'
"""
Element at the top of LiveDesign that displays the project name.
"""
PROJECT_TITLE = '#project-title'
"""
Icon with ellipses that you click to change the project
"""
CHANGE_PROJECT_ICON = '.change-project-icon'
"""
Search input that filters the project list
"""
PROJECT_SEARCH_INPUT = '#project-search .components-text-input-wrapper input'

PROJECT_COPYRIGHT_NOTICE = '.copyright-notice'

THERAPEUTIC_AREA_SEARCH_INPUT = '#therapeutic-search .components-text-input-wrapper input'

PROJECT_DETAILS_CONTENT = '.project-picker-details div'
