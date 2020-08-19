## DawidSkene README

1. Download zip 
2. Unpack
3. Change permissions: `chmod 700 bin/get-another-label.sh`
4. Run get another label (using "face" dataset as an example)
    ```
    get-another-label/bin/get-another-label.sh  
        --categories ../data/categories/categories_face.txt 
        --input ../data/clean-tabbed/answer_face.csv  
        --eval ../data/clean-tabbed/truth_face.csv
    ```
5. The output files will be dumped in the `results/` directory

A few things to note
* right now, the `process_predictions` file only gives accuracy and f1, so calculating MAE, MSE, etc would take a bit of reworking
* `process_predictions` assumes the output file is called `object-probabilities.txt` and located in the same directory
* to run at a level of supervision, make sure to pass in an eval file only with the items you want scored
* the `results/DS` and `results/MV` directories have some results for the face dataset