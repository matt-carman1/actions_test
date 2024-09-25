from ldclient.api import paths

BASE = "/livedesign/api"

COLUMN_DESCRIPTORS = BASE + paths.COLUMN_DESCRIPTORS_PATH + "/{column_descriptor_id}"
COMPOUNDS = BASE + paths.COMPOUNDS_PATH
COMPOUND_SEARCH = BASE + paths.COMPOUNDS_PATH + "/search/async"
LIVE_REPORTS_RESULTS = BASE + paths.LIVE_REPORTS_PATH + "/results"
LOGIN = BASE + paths.AUTH_PATH + "/login"
SCAFFOLDS = BASE + "/scaffolds"
IMPORT_ASYNC = BASE + paths.IMPORT_PATH + "/async_task"
ASYNC_TASK_SEARCH = BASE + paths.ASYNC_PATH + "/search"
CREATE_PLOT = BASE + "/plot"
UPDATE_PLOT = CREATE_PLOT + "/{plot_id}"
LIVE_REPORTS_QUERIES = BASE + paths.LIVE_REPORTS_PATH + "/{live_report_id}/query"
OBSERVATION_SEARCH = BASE + paths.OBSERVATION_PATH + "/search"
RATIONALES_SEARCH = BASE + "/rationales/search"
ACTIVE_USERS_SEARCH = BASE + "/active_users/search"
PLOT_SEARCH = BASE + "/plot/search"
COLUMN_FOLDER_SEARCH = BASE + paths.COLUMN_FOLDER_PATH + "/search"
