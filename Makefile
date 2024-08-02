

clean:
	rm -rf ./build

setup:
	mkdir ./build

conda:
	conda build conda-recipe --no-anaconda-upload --no-include-recipe --no-test --output-folder ./build


