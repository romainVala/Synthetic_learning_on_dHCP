# Synthetic_learning_on_dHCP
This repository report in a csv file, all results from the article
"Comprehensive analysis of synthetic learning applied to neonatal brain MRI segmentation"

Since we use an Open data set (the dHCP)

We also include a python script in generate_data subdir, as well as two label file examples, to show the generating process used with torchio package

Note that to make it run you need to use our torchio fork (https://github.com/romainVala/torchio)
Since we use a specific motion transform, and we also custumize the RandomLabelsToImage transform
but you can easily change the json file to rely on the core torchio package only


