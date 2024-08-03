
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
	twine upload dist/*



