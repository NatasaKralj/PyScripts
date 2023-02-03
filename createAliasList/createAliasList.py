"""
createAliasList.py goes through all .md files to grab 'aliases' parameter in front matter
It goes through every .md file within given startDir.
It outputs a JSON list of all files containing aliases.
It outputs a CSV list of all files containing aliases.
It goes through content again to check all cross-reference links against aliases list.
It outputs the aliases in cross-references to warnings.log
"""
#import jsondiff
import tableFunctions
import frontmatter
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
import json
import logging
import pathlib

# Walk through all directories and files of given directory
# globPattern can be used to specify file type, defualts to all directories and files
# Returns a list of path objects
def dirWalk(start, globPattern="**/*"):
    dirList = list(start.glob(globPattern))
    return dirList

# Add front matter to list of dict entries
# TO DO - split this function into one that adds to itemDict and one that just parses front matter
def addItem(post):
    aliases = post.get("aliases")
    title = post.get("title")
    url = post.get("url")
    map = post.get("mapped")
    # Creates a dictionary entry for file with aliases
    itemDict = {"Title": title, "URL": "docs.mendix.com" + url, "Front matter": "", "aliases": aliases}

    # If 'aliases' exists in front matter
    if aliases != None:
        # Appends dictionary to aliasList
        aliasList.append(itemDict)
        # Each entry of alias in a file gets added to aliasCompare list
        for each in aliases:
            aliasCompare.append(each)

    if map is True:
        # Appends dictionary to aliasList if doc is mapped
        itemDict["Front matter"] = "mapped"
        aliasList.append(itemDict)

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
    logging.basicConfig(filename='aliasLinkWarnings.log', filemode='w', format='%(message)s')
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
                    logging.warning('%d. Link %s in file %s is an alias, please replace', 1, cleanedLink[0], relDir)

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
            addItem(post)
        # Flag for going through content body to check for aliases used in cross references
        if checkAlias == True:
            # Calls function that checks aliases in cross references
            aliasCheck(post, relDir)

# Compare two lists and log the difference
def compareLists(list1: list, list2: list):
    diff = [i for i in list1 + list2 if i not in list1 or i not in list2]
    result = len(diff) == 0
    # Adds differences into warning log
    logging.basicConfig(filename='compareDocsToExcelWarnings.log', filemode='w', format='%(message)s')
    if not result:
        logging.warning('The lists do not match! There are %d differences:',len(diff))
        for line in diff:
            logging.warning('%d. %s', (diff.index(line)+1), line)

# Grab working directory
# TO DO - the hardcoded link will need changing
startDir = "C:\\Users\\Natasa.Kralj\\Documents\\docs\\local-development\\content\\en\\docs\\"
#input('Specify FULL PATH to local content directory: ')
start = pathlib.Path(startDir)

# Empty lists to help with parsing data
aliasList = []
aliasCompare = []

# Walk through all directories and files to find .md files
dirList = dirWalk(start, "**/*.md")

# For all .md files in dirList parse their front matter
for path in dirList:
    parseMdFile(path, frontMatterGrab=True, checkAlias=False)

# Parse excel file into managable list
# TO DO - the hardcoded link will need changing
myNewList = tableFunctions.createListFromExcel("C:\\Users\\Natasa.Kralj\\Documents\\pyScripts\\PyScripts\\test.xlsx")

# Store all docs grabbed and all excel entries into sorted lists
# This is just for testing
docsList = sorted(aliasList, key=lambda x: x['Title'], reverse=False)
excelList = sorted(myNewList, key=lambda x: x['Title'], reverse=False)

# Prints differences between lists, if any
compareLists(docsList, excelList)

# Writes a list of all aliases as a JSON file (list of dicts)
with open('listFromExcel.json', 'w') as logfile:
    json.dump(myNewList, logfile)

# For all .md files in dirList check their text body for aliases in cross references
# This can be done later, after the table has been checked/updated
# for path in dirList:
#     parseMdFile(path, frontMatterGrab=False, checkAlias=True)

## Test for JSON comparison
# obj1 = ""
# obj2 = ""

## Loads the saved JSON files for comparison
# with open('listFromExcel.json', 'r') as logfile:
#     obj1 = json.load(logfile)

# with open('aliasList.json', 'r') as logfile:
#     obj2 = json.load(logfile)

# res = jsondiff.diff(obj1, obj2)
# print(res)

## Uncomment and run lines below only if table doesn't exist
# createTablePrompt = input("Do you want to create the mapping table? (Y/n)")

# if createTablePrompt.lower() == "y":
#     tableName = input("What is the new table name?") + ".xlsx"
#     tableFunctions.createExcelFromList(aliasList, tableName)
# else:
#     pass
