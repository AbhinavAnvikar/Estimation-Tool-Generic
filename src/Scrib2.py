import openpyxl as xl

wb = xl.load_workbook('C:\\Users\\aban0617\\PycharmProjects\\Estimation_Tool\\venv\\Estimation_NC\\media\\Estimation.xlsx')
sheet = wb['Estimation_Matrix']

lst=[]

for i in range(1,sheet.max_row):
    if sheet.cell(i,1).value == 'Simple':   # com 1 value passed
        lst.append(i)
        print(i,sheet.cell(i,1).value)

print(sheet.max_row)
print(sheet.max_column)
for rows in range(1, sheet.max_row + 1):
    if sheet.cell(rows,1).value == 'Complex' and sheet.cell(rows,2).value == 5:
        for headers in range(1,sheet.max_column + 1):
            if sheet.cell(1,headers).value == 'Tech_LOE':
                print(sheet.cell(rows,headers).value)
            elif sheet.cell(1,headers).value == 'Final_Tech_LOE':
                print(sheet.cell(rows,headers).value)
