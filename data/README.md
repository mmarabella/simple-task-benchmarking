## Data and Scripts

The following directories contain data from the same 10ish datasets in different formats:
* **categories:** Specifically for DawidSkene. Lists the categories of each dataset
* **clean:** The main data folder. Datasets in this directory are separated into `answer` and `truth` files and can be joined on the `question` field. This data format will work with the distance-based models (in the annotationmodeling repo) and with most of the scripts in the `data/` directory.