"""
removeUnusedAttachments.py goes through all .md files to make a list of attachment links.
"""

import os
import re
import logging

# Grab working directory
startDir = "C:\\Users\\Johanna.Hemminger\\docs\\content"
#startDir = input('Specify FULL PATH to local content directory: ')

# Empty lists to help with parsing data
attachmentList = [] 

# Create log file
logging.basicConfig(filename='attachmentlistlog.log', filemode='w', format='%(message)s')

# Walk through all files in directory
for dirPath, dirNames, allFiles in os.walk(startDir):
    for name in allFiles:
        # File path that includes name of file
        filePath = os.path.join(dirPath, name)
        # Relative file path that includes name of file
        relFilePath = os.path.relpath(filePath, startDir)
        # Pattern to find any /attachments/ followed by either ) or "
        fullAttachmentRefSearch = '/attachments/([-./\+\w= ]*)?(?:\)|")'
        # Checks if file is Markdown
        if name.lower().endswith('.md'):
            # Opens Markdown file
            with open(filePath, mode='r', encoding="utf-8") as file:
                for line in file:
                    fullSearch = re.findall(fullAttachmentRefSearch,line)
                    if fullSearch != []:
                        for searchitem in fullSearch:
                            # Creates a dictionary for file with aliases
                            itemDict = {"File path": relFilePath, "File name": name, "Attachment Link": searchitem}
                            # Appends each dictionary to attachmentList
                            attachmentList.append(itemDict)
logging.warning(attachmentList)

# Walk through all attachments and check that they're in the attachmentList
# Grab attachment directory
attachmentDir = "C:\\Users\\Johanna.Hemminger\\docs\\static\\attachments"
# attachmentDir = input('Specify FULL PATH to attachments directory (for example, C:\\Users\\Johanna.Hemminger\\docs\\static\\attachments): ')
for dirPath, dirNames, allFiles in os.walk(attachmentDir):
    for name in allFiles:
        # File path that includes name of file
        filePath = os.path.join(dirPath, name)
        # Relative file path that includes name of file
        relFilePath = os.path.relpath(filePath, attachmentDir)
        newFilePath = relFilePath.replace(os.sep, '/')
        deleteFlag = True
        for item in attachmentList:
            # fullSearch returns a list, so we need to pull things out of it
            inList = item["Attachment Link"]
            if name in inList:
                deleteFlag = False
                break
        if deleteFlag is True:
            os.remove(filePath)