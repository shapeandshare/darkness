
setup:
	resources/setup.sh

prepare:
	resources/prepare.sh

clean:
	rm -rf ./build ./dist ./src/shapeandshare.darkness.egg-info

nuke:
	rm -rf ./build ./dist ./src/shapeandshare.darkness.egg-info ./venv

build:
	python3 -m build

#conda:
#	conda build conda-recipe --no-anaconda-upload --no-include-recipe --no-test --output-folder ./build
#

