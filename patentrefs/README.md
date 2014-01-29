# ReffedBy
Code for doing a simple comparison between USPTO data and data from Berkeley Fung Institute

### How to Use

1. Download Fung data
    - [__200 random patents__: clean_200_random.csv](https://github.com/funginstitute/referencedby/blob/master/data/counts/clean_200_random.csv)
    - [__Fung Institute data__: reffedby.csv](https://s3-us-west-1.amazonaws.com/fidownloads/reffedby.csv.zip)

2. Make sure the downloads are in the root directory of the repository.

3. Run `python reffedby.py` and `ruby uspto_reffedby.rb` to get the results.

### Using the Results

Following the instructions above results in two files, `uspto_ref_hash.json`, and `ref_hash.json`, corresponding to data from the USPTO and Fung Institute, respectively.

(It may be easier to analyze the two side by side if you use a [JSON formatter](http://jsonformat.com/) after obtaining the results.)

Each hash's keys are the 200 random patents selected from the [Fung repository](https://github.com/funginstitute/referencedby). The corresponding values list the patents that reference each key.

A side-by-side comparison of the two has sufficed so far, but later `diff.py` may be used to analyze the discrepancies between Fung and USPTO data. `count.py` is a simple way to verify that the computer is reading in all 67 million lines from `reffedby.csv`.

__Note__: Processing takes several minutes, so the script will not run through all the code again if resulting files already exist. To run through the entire process, make sure to delete `reffedby_sample.csv`, `ref_hash.json`, `uspto_ref_hash.json`, and the `uspto_refs` folder from the directory first.

### Credit

The `uspto_reffedby.rb` script is a slightly modified version of the [one on the Fung repository](https://github.com/funginstitute/referencedby/blob/master/referencedby.rb).