
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

#conda:
#	conda build conda-recipe --no-anaconda-upload --no-include-recipe --no-test --output-folder ./build
#

