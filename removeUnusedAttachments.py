"""
removeUnusedAttachments.py goes through all .md files to make a list of attachment links.
"""

import os
import json
import csv
import logging

# Grab working directory
startDir = input('Specify FULL PATH to local content directory: ')

# Empty lists to help with parsing data
attachmentList = []