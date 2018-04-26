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
import pandas as pd

class Labeler(object):
   
    #pre-defined list of categories I am interested in
    KEYWORDS_BY_CATEGORIES = {
        "Rent"              :   [],
        "Car Payment"       :   [],
        "Transportation"    :   ['uber', 
                                 'lyft', 
                                 'caltrain', 
                                 'clipper', 
                                 'mta',
                                 'bart', 
                                 'parking',
                                 'zipcar',
                                 'hertz',
                                 'oil',
                                 'fuel',
                                 'gas'],
        "Entertainment"      :   ['museum',
                                 'theater',
                                 'theatre',
                                 'ticket',
                                 'event',
                                 'citation',
                                 'itunes'],
        "Subscriptions"     :   ['spotify',
                                 'google storage',
                                 'netflix',
                                 'economist',
                                 'dropbox',
                                 'hulu',
                                 'league pass'],
        "Insurance/Health"  :   ["lifeloc",
                                 "assurant",
                                 "wellnes",
                                 "optimeyes",
                                 "medical",
                                 "fitness",
                                 "urgent care",
                                 "clinic",
                                 "hospital"],
        "Groceries"         :   ['meijer', 
                                 'safeway',
                                 'trader joe',
                                 'kroger'],
        "Shopping"          :   ['amazon',
                                 'target',
                                 'nike.com',
                                 'macys',
                                 'ae.com',
                                 'store'],
        "Travel"            :   ['airport',
                                 'airline',
                                 'air line']
    }
    self.CATCH_ALL_CATEGORY = "Miscellaneous"

    def __init__(self, filename):
        '''
        Takes in a filename for a CSV and creates a dictionary where the
        keys are the purchase descriptions and the values are the category.
        '''

        ##create dictionary
        #self.categorized_data = {}

        ##get a list of each line item's tokens
        #tokenized_input = self.tokenize_file(filename)

        ##categorize each line
        #for line_item in tokenized_input:
        #    desc = self.get_purchase_description(line_item)
        #    category = self.categorize(desc)
        #    self.categorized_data[desc] = category

        ##manually label the rest by prompting client
        #self.client_label()

        self.raw_df = pd.read_csv(filename)


    def clean_date(self, date):

        def unpack_date(date):
            month_idx = date.find('/')
            day_idx = date.find('/', month_idx+1)

            month = date[:month_idx]
            day = date[month_idx+1:day_idx]
            year = date[day_idx+1:]

            return month, day, year

        def dow_formula(m, d, y):

            var1 = d
            var2 = int(2.6*m - 0.2)
            var3 = 2*20 #assumes 21st century
            var4 = 2000 + y
            if m <= 2:
                var4 = var4-1
            var5 = int(var4/4)
            var6 = int(var3/4)

            dow = (var1 + var2 + var3 + var4 + var5 + var6) % 7
            return result
        
        month_idx, day, year = unpack_date(date)
        month = constants.MONTHS_BY_INDEX[month_idx]
        dow_idx = dow_formula(month_idx, day, year)
        dow = constants.DAYS_OF_WEEK_BY_INDEX[dow_idx]

        return month, dow, (2000+y)

    def clean_raw_df(self):

        #data fields we are interested in
        header = ['Date', 'Description', 'Amount', 'Category']

        abridged_data = []
        for idx, row in self.raw_df.iterrows():

            #check to make sure this purchase was made for me
                #Apple purchases bought for other people
            for_me = self.verify_purchase(row)
            if not for_me:
                continue
            date = row['Date']
            desc = row['Description']
            amt = self.clean_amount(row['Amount'])
            if amt < 0:
                cat = self.categorize_credit(row)
            else:
                cat = self.categorize_purchase(row)
           
            new_row = [date, desc, amt, cat]
            abridged_data.append(new_row)

        self.polished_df = pd.DataFrame(abridged_data, columns=header)

    def clean_amount(self, str_amt):
        '''
        Takes in an amount in string form, converts to float.
        '''

        new_amt = str_amt.replace(',', '')
        new_amt = float(new_amt)

        return new_amt

    def verify_purchase(self, row):
        '''
        Function that queries client to see if a particular purchase
        was made for someone else.
            -Usually it's an Apple purchase made for someone else
        '''

        concat_desc =   row['Description'] + " " \
                      + str(row['Doing Business As']) + " "  \
                      + str(row['Category'])
        concat_desc = concat_desc.lower()
   
        amt = self.clean_amount(row['Amount'])
        if "apple online store" in concat_desc or amt > 1000:
           
            print "Did you purchase this for yourself?"
            print str(row)
            response = raw_input('Yes or No? :'  )
            print "\n\n"
            response = response.lower()
            result = response.startswith('y')
    
        else:
            result = True

        return result

    def categorize_credit(self, row):
        '''
        Function to categorize a line item that had a negative
        amount, essentially a credit to the account. Could be a
        CC payment, return, discount, etc.
        '''

        concat_desc =   row['Description'] + " " \
                      + str(row['Doing Business As']) + " "  \
                      + str(row['Category'])
        concat_desc = concat_desc.lower()
 
        if ('online payment' in concat_desc) \
            or ('payment received' in concat_desc):
                return "CC PAYMENT"
        
        else:
            return "RETURN/CREDIT"

    def categorize_purchase(self, row):
        '''
        Function to categorize a line item that had a postiive amount,
        essentially a debit from the account. Typical line item.
        '''
        
        concat_desc =   row['Description'] + " " \
                      + str(row['Doing Business As']) + " "  \
                      + str(row['Category'])
        concat_desc = concat_desc.lower()
        
        for cat, keywords in self.KEYWORDS_BY_CATEGORIES.items():
            for kw in keywords:
                if kw in concat_desc:
                    return cat
        
        if ("restaurant" in concat_desc) or ("bar" in concat_desc):
            return "Restaurant/Bar"

        elif ("travel" in concat_desc):
            return "Travel"
       
        elif ('merchandise' in concat_desc):
            return "Shopping"

        elif ('service' in concat_desc):
            return "Services"
        
        for category in self.KEYWORDS_BY_CATEGORIES.keys():
            if category.lower() in concat_desc:
                return category

        return self.CATCH_ALL_CATEGORY 

