## GPM README

Scripts to evaluate the output of GPM. [The original code](https://github.com/jingnantes/AnnotationModel) by the GPM authors is in the AnnotationModel submodule. 

The easy, but slightly hacky, way to use this module is to directly edit the `AnnotationModel/Annotation_main.py` module. You will modify three different places in the code:

1. Add your datafile below the list of existing datafiles. So comment out
    ```
    """----- FTV -------"""
    observation_file = 'FTV/data_FTV.csv'
    data_name = 'FTV'
    K = 5
    ```
    and add the path to your own data
2. `K` (as seen in the code above) is the number of possible categories. For categorical data, it will just be the number of categories. For numerical and ordinal data it will be `max(label_value) - min(label_value)`.
3. Depending on whether the underlying distribution of your task is continuous/ordinal or categorical, you have to swap out the function that estimates the ground truth. The default is `predict = Calculate_expectation(theta_s)`, which is for continuous underlying distributions and will calculate a weighted average of the available labels. For categorical tasks, swap that line out for `predict = Calculate_majority(theta_s)` which will select the most likely category.

**NOTE:** you will probably run into issues if you have negative label values

