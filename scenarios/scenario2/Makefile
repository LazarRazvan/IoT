NOHUP = nohup
PY = python3
PYFLAGS = -u	# prevent buffering
KILL = kill
KILLFLAGS = -9

SRC = scenario2.py
PID_FILE = .pidfile
TUYA_LOGS = tuya.log
NOHUP_LOGS = nohup.out

.PHONY: all
all: run_nohup

.PHONY: run
run:
	$(PY) $(PYFLAGS) $(SRC) & echo $$! > $(PID_FILE)

.PHONY: run_nohup
run_nohup:
	$(NOHUP) $(PY) $(PYFLAGS) $(SRC) & echo $$! > $(PID_FILE)

.PHONY: stop
stop:
	$(KILL) $(KILLFLAGS) `cat $(PID_FILE)`

.PHONY: clean
clean:
	rm $(TUYA_LOGS) $(NOHUP_LOGS) $(PID_FILE)
