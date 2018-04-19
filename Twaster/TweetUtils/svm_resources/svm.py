import pandas as pd
import numpy as np
from sklearn import svm
import math
import pathlib

this_dir = pathlib.Path().resolve() / "svm_resources" / "collection.xlsx"

def index_containing_substring(the_list, substring):
    the_list = [item.lower() for item in the_list]
    for i, s in enumerate(the_list):
        if substring in s:
            return i
    return -1

try:
    earthquakes = pd.read_excel(this_dir)
except FileNotFoundError:
    this_dir = pathlib.Path().resolve() / "TweetUtils" / "svm_resources" / "collection.xlsx"
    earthquakes = pd.read_excel(this_dir)

length_position = earthquakes[['httpsOrAtSy','length','position']].as_matrix()
type_label = earthquakes['eq'].values

model = svm.SVC(kernel='linear', C=2**-5)
model.fit(length_position, type_label)

def eq_or_not(text):
    splited = text.split()
    position = index_containing_substring(splited, "earthquake")
    length = len(splited)
    httpsOrAtSy = 0
    if(index_containing_substring(splited, "@") >= 0 or index_containing_substring(splited, "http") >= 0 or index_containing_substring(splited, "twitter.com") >= 0):
        httpsOrAtSy = 1

    if(model.predict([[httpsOrAtSy,length,position]]) ==1):
        return "It is eq"
    else:
        return "Not eq"
