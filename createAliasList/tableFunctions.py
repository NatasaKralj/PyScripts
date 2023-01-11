import openpyxl
import logging

# Creates the excel table for storing aliases and mapped URLs from .md files
# Should only be run once, after table exists is not needed
def createExcelFromList(list, table):
    # Open excel file
    workbook = openpyxl.load_workbook(filename=table)

    sheet = workbook.active
    aliasNumber = 0
    rowNum = 0

    # Go through list
    for item in list:
        # Sets special row number for first list item
        # TO DO - see if there's a better way to set this
        if list.index(item) == 0:
            rowNumber = 2
        # For every subsequent list item calculate the row number
        else:
            rowNumber = rowNum + 1
        # Put in values from list to cells
        sheet.cell(row=rowNumber, column=1, value=item["Title"])
        sheet.cell(row=rowNumber, column=2, value=item["URL"])
        sheet.cell(row=rowNumber, column=3, value=item["Front matter"])
        sheet.cell(row=rowNumber, column=4, value="")
        # Aliases jump to a new blank row
        # There can be more than one
        for alias in item["aliases"]:
            aliasNumber = item["aliases"].index(alias) + 1
            rowNum = rowNumber + aliasNumber
            sheet.cell(row=rowNum, column=4, value=alias)
        # Save the excel file
        workbook.save(filename=table)

# Creates a list for comparison from excel table
# The list matches the format of initial .md file parsing
# which enables comparison of this and the initial list
def createListFromExcel(table):
    # Open excel file
    workbook = openpyxl.load_workbook(filename=table)

    sheet = workbook.active
    startRow = 2
    listFromTable = []

    # Loop to keep going through rows until the last one is reached
    while startRow < sheet.max_row:

        aliases = []
        nextRow = startRow + 1
        # Grab values from cells
        title = sheet.cell(row=startRow, column=1).value
        url = sheet.cell(row=startRow, column=2).value
        mapped = sheet.cell(row=startRow, column=3).value
        if mapped == None:
            mapped = ""
        # Aliases jump to a new blank row
        # There can be more than one
        checkNext = sheet.cell(row=nextRow, column=1).value
        alias = sheet.cell(row=nextRow, column=4).value
        while (checkNext == None) and (alias != None):
            aliases.append(alias)
            nextRow = nextRow + 1
            alias = sheet.cell(row=nextRow, column=4).value
            checkNext = sheet.cell(row=nextRow, column=1).value
        # Dump all grabbed values into dict for list
        itemDict = {"Title": title, "URL": url, "Front matter": mapped, "aliases": aliases}
        listFromTable.append(itemDict)
        startRow = nextRow
    # Save the excel file
    workbook.save(filename=table)
    # Return the new list
    return listFromTable

# # Compares each list item with 
# def compareItem(listItem, tableRow, sheet):
#     tabItem = tableItem(tableRow, sheet)
#     if listItem["Title"] == tabItem.title & listItem["URL"] == tabItem.url:
#         if listItem["Front matter"] != tabItem.mapped:
#             # If it is an alias, adds it to log
#             logging.basicConfig(filename='warnings.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
#             logging.warning('Mapping mismatch between file %s and table row %s', listItem["File path"], tableRow)
#         if tabItem.aliasList != []:
#             l1 = tabItem.aliasList.sort()
#             l2 = [4]["aliases"].sort()
#             if l1 != l2: 
#                 logging.basicConfig(filename='warnings.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
#                 logging.warning('Alias entries are not the same in file %s and table row %s', listItem["File path"], tableRow)
#         if tabItem.prodList != None:
#             if tabItem.mapped == None:
#                 logging.basicConfig(filename='warnings.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
#                 logging.warning('Table row %s entry is mapped to product(s), but missing "mapped" parameter. ', tableRow)
#     else:
#         logging.basicConfig(filename='warnings.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
#         logging.warning('File %s and table row %s are not same item!', listItem["File path"], tableRow)
#     return tabItem.nextRow

# def tableItem(startRow, sheet):
#     aliasList = []
#     prodList = []
#     nextRow = startRow + 1
#     title = sheet.cell(row=startRow, column=1).value
#     url = sheet.cell(row=startRow, column=2).value
#     mapped = sheet.cell(row=startRow, column=3).value
#     checkNext = sheet.cell(row=nextRow, column=1).value
#     alias = sheet.cell(row=nextRow, column=4).value
#     product = sheet.cell(row=startRow, column=5).value
#     if product != None:
#         prodList.append(product)
#     while (checkNext == None) and (alias != None):
#         product = sheet.cell(row=nextRow, column=5).value
#         if product != None:
#             prodList.append(product)
#         aliasList.append(alias)
#         nextRow = nextRow + 1
#         alias = sheet.cell(row=nextRow, column=4).value
#         checkNext = sheet.cell(row=nextRow, column=1).value


#     return title, url, mapped, aliasList, prodList, nextRow
