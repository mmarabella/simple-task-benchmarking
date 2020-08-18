## MACE README

**MACE_external_lib** is the submodule with the original MACE code. There is [yet another README](MACE_external_lib/README.md) in that submodule with an explanation of how to run the script using Java or a shell script

**evaluate.py** takes the output of running the MACE program and calculates the accuracy, f1, mae, mse, etc. depending on the task type. The output of `--help`:

```
    positional arguments:
      task                  task/dataset name
      task_type             task type (e.g. categorical, ordinal, numerical...)
      predictions_file      location of file with answer/labels
      eval_file             location of file with truths

    optional arguments:
      -h, --help            show this help message and exit
      --log-results RESULTS_DIR
                            write results to user-specified directory
      --semi-supervised PCT_TRAINING_SET
                            amount of supervision. Does not affect how program
                            runs and is just for logging
      --fold FOLD           which fold? Does not affect how program runs and is
                            just for logging
      --noise NOISE         noise level. Does not affect how program runs 
                            and is just for logging
```

**RUN_SEMISUPERVISED.sh** and **RUN_NOISE.sh** are scripts I made to repeatedly run the MACE program and `evaluate.py` on multiple levels of supervision and noise.

**results/** is where the output of `evaluate.py`, `RUN_NOISE.sh` and `RUN_SUPERVISED.sh` will go, unless otherwise specified