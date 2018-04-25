#!user/bin/env python

################################################################################
# File:     constants.py
# Author:   Vikram Prasad
# Date:     April 24, 2018
# Desc:     This flie houses constants, essentially pound defines.
#           Utilized by other modules in the spending-tracker to consolidate
#           all relatively-static information.
################################################################################

#note the first element is a NULL to match one-indexing of months
MONTHS_BY_INDEX = ["",  "January",   "February", "March",    "April", 
                        "May",       "June",     "July",     "August",
                        "September", "October",  "November", "December"]

DAYS_OF_WEEK_BY_INDEX = ["Sunday",      "Monday",   "Tuesday",  "Wednesday",
                         "Thursday",    "Friday",   "Saturday"]
