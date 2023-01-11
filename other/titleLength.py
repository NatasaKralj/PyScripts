# -*- coding: UTF-8 -*-
"""
Usage: 
Input a directory to work from, specify which filetype to search through,
type in the regex expression to match.
The script walks through all files within the top directory. 
Each line in each file is searched for the regex query. 
The title parameter gets grabbed from the directory path, and if longer than X characters, put into a json list.
"""

import os           # Using os.walkk(), os.path.join()
import re           # Using re.search()
import fileinput
import json
import csv

# grab working directory
startDir = input('Specify FULL PATH to local content directory: ')

# The extension to search through
fileExtension = '.md'

# Search for title
titleMatch = '(?<=^title: )("?.*"?)'

# Name of log for recordkeeping
logName = 'titleLength.json'
titleList = []

# Walk through all files in directory
for dirPath, dirNames, allFiles in os.walk(startDir):
    for name in allFiles:
        filePath = os.path.join(dirPath, name)
        if name.lower().endswith(fileExtension):
            with fileinput.input(filePath, inplace=True, backup='', encoding="utf-8") as file:
                lineNum = 0
                frontMatterEnd = True
                for line in file:
                    if '---\n' == line:
                        frontMatterEnd = not frontMatterEnd
                    elif lineNum > 0 and frontMatterEnd == False:
                        searchTitle = re.search(titleMatch,line)
                        if searchTitle != None:
                            title = searchTitle.group()
                            titleLength = len(title)
                            if titleLength > 40:
                                # creates a dictionary for every title, loggin the directory, title characters and title length
                                itemDict = {"Dir": filePath, "title": title, "length": titleLength, "linktitle": ""}
                                # appends each dictionary to titleList
                                titleList.append(itemDict)
                                line = line + "linktitle: \n"
                    lineNum += 1
                    print(line, end='')

# Write grabbed titles to logfile
with open(logName, 'w') as logfile:
    # Writes all of titleList as a json file (list of dicts)
    json.dump(titleList, logfile)

with open('titleLengthList.csv', 'w', newline='') as f:
    fieldNames = ['Dir', 'title', 'length', 'linktitle']
    writer = csv.DictWriter(f, fieldnames=fieldNames)
    writer.writeheader()
    writer.writerows(titleList)
