#!user/bin/env python

################################################################################
# File:     statement_parser.py
# Author:   Vikram Prasad
# Date:     January 25, 2018
# Desc:     This file takes in a csv statement downloaded from my CC website and
#           parses the data.
################################################################################

#imports, boilerplate stuff
import time
import sys
import os
import numpy as np
import pickle

def tokenize_file(filename):
    '''
    Function takes in a CSV and returns a list of the lines
    '''

    tokens_by_line = []
    
    with open(filename) as f:
        for line in f:
            words = [x.strip() for x in line.split(',')]
            tokens = []
            for elem in words:
                if len(elem)>0: tokens.append(elem)
            tokens_by_line.append(tokens)

    return tokens_by_line
    
if __name__ == "__main__":

    #take in filename
    fn = sys.argv[1] #first arg is the python file being executed

    #tokenizes csv into a list of lines
    line_item_features = tokenize_file(fn)

