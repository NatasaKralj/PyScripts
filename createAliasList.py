"""
createAliasList.py goes through all .md files to grab 'aliases' parameter in front matter
It goes through every .md file within given startDir.
It outputs a JSON list of all files containing aliases.
It outputs a CSV list of all files containing aliases.
It goes through content again to check all cross-reference links against aliases list.
It outputs the aliases in cross-references to warnings.log
"""

import frontmatter
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
import os
import json
import csv
import logging

# Grab working directory
startDir = input('Specify FULL PATH to local content directory: ')

# Empty lists to help with parsing data
aliasList = []
aliasCompare = []
linkChecked = []

# Walk through all files in directory
for dirPath, dirNames, allFiles in os.walk(startDir):
    for name in allFiles:
        # File path that includes name of file
        filePath = os.path.join(dirPath, name)
        # Relative file path that includes name of file
        relFilePath = os.path.relpath(filePath, startDir)
        # Checks if file is Markdown
        if name.lower().endswith('.md'):
            # Opens Markdown file
            with open(filePath, mode='r', encoding="utf-8") as file:
                # Loads file into frontmatter parser
                post = frontmatter.load(file)
                aliases = post.get("aliases")
                title = post.get("title")
                # If 'aliases' exists in front matter
                if aliases != None:
                    # Creates a dictionary for file with aliases
                    itemDict = {"File path": relFilePath, "title": title, "aliases": aliases}
                    # Appends each dictionary to aliasList
                    aliasList.append(itemDict)
                    # Each entry of ailas for a file gets added to aliasCompare list
                    for each in aliases:
                        aliasCompare.append(each)

# Walk through all files in directory
for dirPath, dirNames, allFiles in os.walk(startDir):
    for name in allFiles:
        # File path that includes name of file
        filePath = os.path.join(dirPath, name)
        # Relative file path that includes name of file
        relFilePath = os.path.relpath(filePath, startDir)
        # Checks if file is Markdown
        if name.lower().endswith('.md'):
            # Opens Markdown file
            with open(filePath, mode='r', encoding="utf-8") as file:
                # Loads file into frontmatter parser
                post = frontmatter.load(file)
                # Calls Markdown class and sets type to GitHub-like
                md = MarkdownIt("gfm-like")
                # Makes text parsable, won't work with feeding file
                text = post.content
                # Gives Markdown tokens
                tokens = md.parse(text)
                # Takes tokens to create a SyntaxTree
                node = SyntaxTreeNode(tokens)
                # Walks through all tree nodes
                for node in node.walk():
                    # If a node is a link type
                    if node.type == "link":
                        # Gives back the dict value of node attribute with key 'href'
                        link = node.attrs['href']
                        # Removes any anchor from link
                        cleanedLink = link.split('#', maxsplit=1)
                        # If the link contains anything before # and has not been checked previously
                        if cleanedLink[0] != '' and cleanedLink[0] not in linkChecked:
                            # Checks if the link is in the alias list
                            if cleanedLink[0] in aliasCompare:
                                # If it is an alias, adds it to log
                                logging.basicConfig(filename='warnings.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
                                logging.warning('Link %s in file %s is an alias, please replace', cleanedLink[0], relFilePath)
                            # Once link has been checked against alias list once, it's added to checked list
                            linkChecked.append(cleanedLink[0])

# Writes a list of all aliases as a JSON file (list of dicts)
with open('aliasList\\'+'aliasList.json', 'w') as logfile:
    json.dump(aliasList, logfile)

# Writes a list of all aliases as a CSV
with open('aliasList\\'+'aliasList.csv', 'w', newline='') as f:
    fieldNames = ['File path', 'title', 'aliases']
    writer = csv.DictWriter(f, fieldnames=fieldNames)
    writer.writeheader()
    writer.writerows(aliasList)

