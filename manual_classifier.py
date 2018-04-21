#!user/bin/env python

################################################################################
# File:     manual_classifier.py
# Author:   Vikram Prasad
# Date:     April 20, 2018
# Desc:     This file takes in a csv statement and has manual rules to label the
#           data. Ideally, with this fully labeled set, I can write some ML code
#           to classify unseen purchases.
################################################################################

#imports, boilerplate stuff
import time
import sys
import os
import numpy as np
import pickle

class Labeler(object):
   
    #pre-defined list of categories I am interested in
    KEYWORDS_BY_CATEGORIES = {
            "rent" : [],
            "car payment" : [],
            "transportation" : [ 'uber', 
                                 'lyft', 
                                 'caltrain', 
                                 'clipper', 
                                 'bart', 
                                 'hertz'
                                 'oil',
                                 'fuel',
                                 'gas'],
            "restaurants/bars" : ['pizza',
                                 'caffe macs'],
            "fast food" : [],
            "travel" : [],
            "entertainment" : ['museum'],
            "subscriptions" : ['spotify',
                                'storage',
                                'dropbox',
                                'hulu'],
            "insurance" : [  "lifeloc",
                             "assurant"],
            "groceries/household items" : [ 'target', 
                                             'safeway',
                                             'meijer'],
            "online shopping" : ['amazon']        
    }
    
    
    def __init__(self, filename):
        '''
        Takes in a filename for a CSV and creates a dictionary where the
        keys are the purchase descriptions and the values are the category.
        '''

        #create dictionary
        self.categorized_data = {}

        #get a list of each line item's tokens
        tokenized_input = self.tokenize_file(filename)

        for line_item in tokenized_input:
            desc = self.get_purchase_description(line_item)
            category = self.categorize(desc)
            self.categorized_data[desc] = category

    def tokenize_file(self, filename):
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
    
    def get_purchase_description(self, line_elements):
        '''
        Returns the purchase description of a lineitem.
        '''

        return line_elements[1]

    def categorize(self, description):
        '''
        Function takes in a purchase description and has manual hard-coded
        definitions of what category it belongs in
        '''

        
        description = description.lower()

        for cat, keywords in self.KEYWORDS_BY_CATEGORIES.items():
            for kw in keywords:
                if kw in description:
                    return cat

        return "MISC"
