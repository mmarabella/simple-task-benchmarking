## CATD README

**CrowdTI** is a submodule with the implementation of CATD used for the [Truth Inference in Crowdsourcing: Is the Problem Solved?](http://dbgroup.cs.tsinghua.edu.cn/ligl/papers/vldb17-quality.pdf) paper. This paper and repo implement many aggregation methods, and the CATD method is located in both `CrowdTI/main/methods/CATD` and `CrowdTI/truth_inference_crowd/methods/c_CATD`. These two seem to be copies of each other. 

Running the `method.py` module in either of these folders works well, but if you want logging more consistent with the other aggregation models, you can use my modification, described below.

Due to some import issues and python2/python3 conflicts, I had to copy the CATD folder and make my own modifications to the `main` method. Otherwise, I don't change anything. To run:

`cd my_CATD`
```
python method.py <path-to-answer-file>/file.csv <task-type> <path-to-truth-file>/file.csv <task-name>
```

The `task-name` is just for logging purposes. The `task-type` can be either `categorical`, `continuous`, or `ordinal`

