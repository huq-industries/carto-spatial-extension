# Makefile for BigQuery modules

SED = sed
GSUTIL = gsutil
BQ = bq --location=$(BQ_REGION) --project_id=$(BQ_PROJECT)

BQ_DATASET = $(BQ_DATASET_PREFIX)$(MODULE)
BQ_PREFIX = $(BQ_PROJECT).$(BQ_DATASET_PREFIX)

ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

BQ_LIBRARY = $(ROOT_DIR)/dist/index.js
BQ_BUCKET_PATH = $(BQ_BUCKET)$(BQ_DATASET)/
BQ_LIBRARY_BUCKET = $(BQ_BUCKET_PATH)index.js

BQ_MODULE_CORE_LABEL = spatial_extension_module:core

COMMON_DIR = $(ROOT_DIR)/../../../common/bigquery
SCRIPTS_DIR = $(ROOT_DIR)/../../../scripts
SHARED_DIR = $(ROOT_DIR)/../shared/javascript

NODE_MODULES = $(ROOT_DIR)/node_modules
NODE_MODULES_DEV = $(COMMON_DIR)/node_modules
NODE_MODULES_SHARED = $(SHARED_DIR)/node_modules

REPLACEMENTS = -e 's!@@BQ_PREFIX@@!$(BQ_PREFIX)!g' -e 's!@@BQ_LIBRARY_BUCKET@@!$(BQ_LIBRARY_BUCKET)!g'

.SILENT:

.PHONY: help lint lint-fix build test-unit test-integration test-integration-full deploy clean clean-deploy serialize-module

help:
	echo "Please choose one of the following targets: lint, lint-fix, build, test-unit, test-integration, test-integration-full, deploy, clean, clean-deploy, serialize-module"

$(NODE_MODULES):
	yarn -s

$(NODE_MODULES_DEV):
	yarn -s --cwd $(COMMON_DIR)

$(NODE_MODULES_SHARED):
	yarn -s --cwd $(SHARED_DIR)

lint: $(NODE_MODULES_DEV)
	PATH=$(NODE_MODULES_DEV)/.bin/:$(PATH) \
	eslint --config ../../../.eslintrc.js .

lint-fix: $(NODE_MODULES_DEV)
	PATH=$(NODE_MODULES_DEV)/.bin/:$(PATH) \
	eslint --config ../../../.eslintrc.js . --fix

build: $(NODE_MODULES) $(NODE_MODULES_SHARED) $(NODE_MODULES_DEV)
	NAME=$(MODULE)Lib \
	PATH=$(NODE_MODULES_DEV)/.bin/:$(PATH) \
	rollup --config $(COMMON_DIR)/rollup.config.js $(BUILD_PARAMS)

test-unit:
	UNIT_TEST=1 \
	$(MAKE) build
	PATH=$(NODE_MODULES_DEV)/.bin/:$(PATH) \
	jest test/unit --testTimeout=30000

test-integration-full:
	$(MAKE) deploy
	$(MAKE) test-integration || ($(MAKE) clean-deploy && exit 1)
	$(MAKE) clean-deploy

test-integration: check $(NODE_MODULES_DEV)
	PATH=$(NODE_MODULES_DEV)/.bin/:$(PATH) \
	jest test/integration/$(TEST) --testTimeout=30000

deploy: check
	$(MAKE) storage-upload
	$(MAKE) dataset-create
	$(MAKE) dataset-deploy
ifdef BQ_PERMISSIONS
	BQ_PERMISSIONS_TARGET_DATASET=$(BQ_DATASET) $(COMMON_DIR)/set_module_permissions.sh
endif
ifdef BQ_PERMISSIONS_GROUP
	BQ_PERMISSIONS_TARGET_DATASET=$(BQ_DATASET) $(COMMON_DIR)/set_module_permissions_group.sh
endif

clean:
	rm -rf dist $(NODE_MODULES) $(NODE_MODULES_SHARED) $(NODE_MODULES_DEV)

clean-deploy: check
	$(MAKE) storage-remove
	$(MAKE) dataset-remove || ((sleep 5 && $(MAKE) dataset-remove) || exit 1)

storage-upload:
	$(MAKE) build
	$(GSUTIL) cp -r $(BQ_LIBRARY) $(BQ_BUCKET_PATH)

storage-remove:
	if [ `$(GSUTIL) ls $(BQ_BUCKET_PATH) 2>&1 | grep "$(BQ_BUCKET_PATH)"` ]; then \
		$(GSUTIL) rm -r -f $(BQ_BUCKET_PATH); \
	fi

dataset-create:
	$(BQ) show $(BQ_DATASET) 2>/dev/null 1>/dev/null || \
		$(BQ) mk -d --description "$(BQ_DATASET) module" -label $(BQ_MODULE_CORE_LABEL) $(BQ_DATASET)

dataset-remove:
	$(BQ) rm -r -f -d $(BQ_DATASET)

dataset-deploy:
	for n in `node $(SCRIPTS_DIR)/sqlsort.js`; do \
		$(SED) $(REPLACEMENTS) $$n | $(BQ) query -q --format=json --use_legacy_sql=false || exit 1; \
	done

serialize-module:
	$(MAKE) build
	rm -f dist/module.sql
	echo "CREATE SCHEMA IF NOT EXISTS \`@@BQ_PREFIX@@$(MODULE)\`;" >> dist/module.sql
	for n in `node $(SCRIPTS_DIR)/sqlsort.js`; do \
	  	cat $$n >> dist/module.sql; \
		echo "" >> dist/module.sql; \
	done

check:
ifndef BQ_REGION
	$(error BQ_REGION is undefined)
endif
ifndef BQ_PROJECT
	$(error BQ_PROJECT is undefined)
endif
ifndef BQ_BUCKET
	$(error BQ_BUCKET is undefined)
endif