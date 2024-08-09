
setup:
	resources/setup.sh

prepare:
	resources/prepare.sh

clean:
	rm -rf ./build ./dist ./src/shapeandshare.darkness.egg-info

nuke:
	rm -rf ./build ./dist ./src/shapeandshare.darkness.egg-info ./venv ./data

build:
	resources/build.sh

publish:
	resources/publish.sh

# In CI:
#	TWINE_USERNAME=joshburt
#	TWINE_PASSWORD=token
#	TWINE_NON_INTERACTIVE
# locally: ~/.pypirc

lint:
	resources/lint.sh

lint-fix:
	resources/lint-fix.sh

docs-quickstart:
	sphinx-quickstart docs --sep --project darknesss

docs-api:
	sphinx-apidoc -f -o docs/source/api src/shapeandshare/darkness

docs-build:
	rm -rf docs/build && cd docs && make clean && make html
