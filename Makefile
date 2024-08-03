

clean:
	rm -rf ./build ./dist ./src/shapeandshare.darkness.egg-info

build:
	python3 -m build

#setup:
#	mkdir ./build
#
#conda:
#	conda build conda-recipe --no-anaconda-upload --no-include-recipe --no-test --output-folder ./build
#

