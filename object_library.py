#!user/bin/env python

################################################################################
# File:     object_library.py
# Author:   Vikram Prasad
# Date:     January 25, 2018
# Desc:     This file defines all the class objects needed for the spending
#           tracker.
################################################################################

#imports, boilerplate stuff
import time
import sys
import os
import numpy as np
import pickle

class LineItem(object):

    #object attributes
    def __init__(self, line_item_keywords):
        '''
        Takes in a line with comma-seperated elements pulled from a spreadsheet
        downloaded from a credit card statement. Each of these lines describes a
        particular purchase (line item) and has features associated with it.
        This object consolidates all that information in an accessible class.
        '''

        #unpack csv_line
        date, description, amount = line_item_keywords

        #cleanup date
        month, day, year = self.unpack_date(date)
        
        #classify
        category = self.categorize(establishment)

        #save attributes
        self.month = month
        self.day = day
        self.year = year

        self.amount = amount
        self.establishment = establishment
        self.category = category

    def categorize(self, establishment):
        '''
        Based on the establishment and exogenously defined rules, this function
        will return the cateogry.
        '''
 
        pass

    def unpack_date(self, date):
        '''
        Takes a string form of a full date and returns the month, day, and year.
        '''
        
        pass
