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
import json
import csv
import logging
import pathlib

# Walk through all directories and files of given directory
# globPattern can be used to specify file type, defualts to all directories and files
# Returns a list of path objects
def dirWalk(start, globPattern="**/*"):
    dirList = list(start.glob(globPattern))
    return dirList

# Go through .md file types
# Can toggle parsing of front matter
# Can toggle finding aliases in .md body content
def parseMdFile(filePath, frontMatterGrab=True, checkAlias=False):
    # creates a relative path from starting directory
    # used in logs
    relDir = filePath.relative_to(start)
    # Opens Markdown file
    with open(filePath, mode='r', encoding="utf-8") as file:
        # Loads .md file into post via frontmatter module
        post = frontmatter.load(file)
        # Flag for going through functions that parse front matter
        if frontMatterGrab == True:
            # Calls function that grabs any aliases in front matter
            aliasGrab(post, relDir)
            # Calls function that checks for "mapped" flag
            mapGrab(post)
        # Flag for going through content body to check for aliases used in cross references
        if checkAlias == True:
            # Calls function that checks aliases in cross references
            aliasCheck(post, relDir)

# Grab aliases from front matter
def aliasGrab(post, relDir):
    aliases = post.get("aliases")
    title = post.get("title")
    # If 'aliases' exists in front matter
    if aliases != None:
        # Creates a dictionary entry for file with aliases
        itemDict = {"File path": str(relDir), "title": title, "isMapped": "", "aliases": aliases}
        # Appends each dictionary to aliasList
        aliasList.append(itemDict)
        # Each entry of alias in a file gets added to aliasCompare list
        for each in aliases:
            aliasCompare.append(each)

# Checks for "mapped" flag in front matter
def mapGrab(post):
    map = post.get("mapped")
    if map is True:
        # Adds if doc is mapped or not
        aliasList[0]["isMapped"] = "mapped"

# Checks for the use of aliases in cross reference links
def aliasCheck(post, relDir):
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
            # If the link contains anything before #
            if cleanedLink[0] != '':
                # Checks if the link is in the alias list
                if cleanedLink[0] in aliasCompare:
                    # If it is an alias, adds it to log
                    logging.basicConfig(filename='warnings.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
                    logging.warning('Link %s in file %s is an alias, please replace', cleanedLink[0], relDir)

# Grab working directory
startDir = input('Specify FULL PATH to local content directory: ')
start = pathlib.Path(startDir)

# Empty lists to help with parsing data
aliasList = []
aliasCompare = []

# Walk through all directories and files to find .md files
dirList = dirWalk(start, "**/*.md")

# For all .md files in dirList parse their front matter
for path in dirList:
    parseMdFile(path, frontMatterGrab=True, checkAlias=False)

# For all .md files in dirList check their text body for aliases in cross references
for path in dirList:
    parseMdFile(path, frontMatterGrab=False, checkAlias=True)

# File output for testing, (un)comment below

# Writes a list of all aliases as a JSON file (list of dicts)
with open('aliasList.json', 'w') as logfile:
    json.dump(aliasList, logfile)

# Writes a list of all aliases as a CSV
with open('aliasList.csv', 'w', newline='') as f:
    fieldNames = ['File path', 'title', 'isMapped', 'aliases']
    writer = csv.DictWriter(f, fieldnames=fieldNames)
    writer.writeheader()
    writer.writerows(aliasList)
