# Note this Makefile is only for running API tests!!!
# Selenium tests need additional dependencies that are not covered here

ENV=venv
export LD_SERVER=http://localhost/livedesign

$(ENV):
	virtualenv -p python3 $(ENV)
	touch $@

build: install-deps $(ENV)
	$(ENV)/bin/pip install -r requirements.txt
	$(ENV)/bin/pip install -e ../LD-WebServicesClient

#I did not test the Darwin case, so it might not work
install-deps:
ifeq ($(shell uname), Darwin)
	brew install cairo libffi
	touch $@
else ifeq ($(shell uname), Linux)
	sudo apt-get install -y libffi-dev python3-cffi
	touch $@
else
	@echo "Unsupported operating system!"
endif

test: $(ENV)
	LD_SERVER=http://localhost/livedesign $(ENV)/bin/pytest tests/api -k "test_"

clean:
	rm -rf $(ENV)