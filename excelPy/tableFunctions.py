import openpyxl

# Creates the excel table for storing aliases and mapped URLs from .md files

workbook = openpyxl.load_workbook(filename="C:\\Users\\Natasa.Kralj\\Documents\\pyScripts\\PyScripts\\mapping-example-table.xlsx")

sheet = workbook.active

for row in sheet.iter_rows(min_row=2, max_col=14, max_row=50):
    for cell in row:
        print("Cell row: " + str(cell.row) + " column: " + str(cell.column) + "  value: " + cell.value)