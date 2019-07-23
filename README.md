# Enron Summariser

To run

```python
python summarize-enron.py <path_to_raw_csv>
```

It will save the output in two files
1. emails_activity.csv
2. activity_plot.html

It will also open up the a dialog box to save the plot as png. Plotly currently does not have a proper way to export as png, they have developed this https://plot.ly/python/static-image-export/ but it requires installing some external non python dependencies, hence I did not implement that.

Any config of paths, or run params can be changed in the run_config.py script

