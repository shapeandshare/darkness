
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
