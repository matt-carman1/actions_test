
# This makefile should be executed from LD-WebTests directory, e.g.:
#       $ cd $SEURAT/LD-WebTests
#       $ make -f ./locustload/makefile

SHELL := /bin/bash 

SERVER = http://localhost:9080
PWD := $(shell pwd)
ANACONDA := $(PWD)/anaconda
VENV := locustenv
OUTPUT_DIR = results
OUTPUT_PREFIX = $(OUTPUT_DIR)/locust
LOCUST_OPTS = --headless --host $(SERVER) --only-summary -f ./locustload/locustfile.py
LOCUST_SWARM_OPTS = --headless --host $(SERVER) --only-summary -f ./locustload/locustfile_swarm.py
LOCUST_OPTS_CSV = $(LOCUST_OPTS) --csv-full-history
LOCUST_SWARM_OPTS_CSV = $(LOCUST_SWARM_OPTS) --csv-full-history
LOCUST_DB_PROFILE ?= starter
DEFAULT_USERS := BasicUser BasicAdvancedSearchUser AdvancedUser ServiceResponseUser CoincidentUser

# Keep this in sync with the number of users mentioned in "run-swarm" target
SWARM_USER := SwarmUser

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
	CONDA_URL := https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
else
	CONDA_URL := https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
endif

.PHONY: clean setup run

all: clean setup run

swarm: clean setup run-swarm

clean:
	- rm -rf $(ANACONDA)
	- rm -rf anaconda.sh
	- rm -rf $(OUTPUT_DIR)

setup: $(ANACONDA)

$(ANACONDA):
	# Install Anaconda
	wget $(CONDA_URL) -O anaconda.sh
	bash anaconda.sh -b -p $(ANACONDA)
	# Create Python venv
	$(eval export PATH=$(ANACONDA)/bin:$(PATH))
	@echo $(PATH)
	conda create -y --name $(VENV) python=3.8
	conda update pip
	source activate $(VENV) && \
	(\
		pip install -r requirements.txt; \
		pip install -r locustload/requirements.txt; \
		pip install $(SERVER)/livedesign/ldclient.tar.gz \
	)

run: $(ANACONDA)
	- rm -rf $(OUTPUT_DIR)
	mkdir $(OUTPUT_DIR)
	$(eval export PATH=$(ANACONDA)/bin:$(PATH))
	@echo $(PATH)
	source activate $(VENV) && \
	(\
		locust $(LOCUST_OPTS) -u 1 -r 1 WarmupUser ; \
		\
		for user in $(DEFAULT_USERS); do \
			locust $(LOCUST_OPTS_CSV) -u 1 -r 1 --csv $(OUTPUT_PREFIX)_$${user}_01_users $${user} ;  \
			python -m locustload.util.jenkins ${OUTPUT_PREFIX} _$${user}_01_users ; \
			python -m locustload.util.svg \
				${OUTPUT_PREFIX}_$${user}_01_users_all_data.csv \
				${OUTPUT_PREFIX}_$${user}_01_users_all_data.svg ; \
			sleep 20; \
								\
			locust $(LOCUST_OPTS_CSV) -u 7 -r 1 --csv $(OUTPUT_PREFIX)_$${user}_07_users $${user} ;  \
			python -m locustload.util.jenkins ${OUTPUT_PREFIX} _$${user}_07_users ; \
			python -m locustload.util.svg \
				${OUTPUT_PREFIX}_$${user}_07_users_all_data.csv \
				${OUTPUT_PREFIX}_$${user}_07_users_all_data.svg ; \
			sleep 60; \
		done; \
		locust $(LOCUST_OPTS) -u 1 -r 1 CleanupUser ; \
		\
		user=ExecutionUser; \
		LOCUST_DEFAULT_WAIT_INTERVAL=400 LOCUST_DEFAULT_RETRIES=400 locust $(LOCUST_OPTS_CSV) -u 7 -r 1 --csv $(OUTPUT_PREFIX)_$${user}_07_users $${user} ;  \
		python -m locustload.util.jenkins ${OUTPUT_PREFIX} _$${user}_07_users ; \
		python -m locustload.util.svg \
			${OUTPUT_PREFIX}_$${user}_07_users_all_data.csv \
			${OUTPUT_PREFIX}_$${user}_07_users_all_data.svg ; \
		sleep 60; \
	)

run-swarm: $(ANACONDA)
	- rm -rf $(OUTPUT_DIR)
	mkdir $(OUTPUT_DIR)
	$(eval export PATH=$(ANACONDA)/bin:$(PATH))
	@echo $(PATH)
	source activate $(VENV) && \
	(\
		locust $(LOCUST_OPTS) WarmupUser ; \
		locust $(LOCUST_SWARM_OPTS_CSV) --load_profile variable --max_user_count 7 --max_run_time 1920 --peak_run_time 900 --csv $(OUTPUT_PREFIX)_all_users_variable_load $(SWARM_USER) ; \
		python -m locustload.util.jenkins ${OUTPUT_PREFIX} _all_users_variable_load ; \
		python -m locustload.util.svg \
				${OUTPUT_PREFIX}_all_users_variable_load_all_data.csv \
				${OUTPUT_PREFIX}_all_users_variable_load_all_data.svg ; \
		sleep 60; \
		\
		locust $(LOCUST_SWARM_OPTS_CSV) --load_profile constant --max_user_count 7 --custom_spawn_rate 7 --max_run_time 900 --csv $(OUTPUT_PREFIX)_all_users_constant_load $(SWARM_USER) ; \
		python -m locustload.util.jenkins ${OUTPUT_PREFIX} _all_users_constant_load ; \
		python -m locustload.util.svg \
				${OUTPUT_PREFIX}_all_users_constant_load_all_data.csv \
				${OUTPUT_PREFIX}_all_users_constant_load_all_data.svg ; \
	)

run-custom: $(ANACONDA)
	- rm -rf $(OUTPUT_DIR)
	mkdir $(OUTPUT_DIR)
	$(eval export PATH=$(ANACONDA)/bin:$(PATH))
	@echo $(PATH)
	source activate $(VENV) && \
	(\
		export LOCUST_DB_PROFILE=$(LOCUST_DB_PROFILE) ; \
		locust $(LOCUST_OPTS) --csv $(OUTPUT_PREFIX)_custom $(LOCUST_CUSTOM_OPTS) ; \
	)
