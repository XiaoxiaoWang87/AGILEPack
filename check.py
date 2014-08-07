#!/usr/bin/python

import sys
import os

import csv
from types import *

import time
import datetime
import random
from random import randint

import pandas as pd
import numpy as np
import ROOT

df = pd.read_csv('data.csv')

for index, row in df.iterrows():

    # clean unphysical trip duration entries
    if row['UserType'] == 0:
        print "find"
