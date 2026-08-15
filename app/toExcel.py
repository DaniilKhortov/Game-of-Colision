import xlsxwriter
from .globalVars import damage



def saveRecord():

    recordTable = xlsxwriter.Workbook('Record.xlsx')
    worksheet = recordTable.add_worksheet()
    
    headerColor = recordTable.add_format({'bg_color': '#FF5733'})
    awariaColor = recordTable.add_format({'bg_color': '#DAA520'})
    
    worksheet.write(0, 0, "Accident Number", headerColor )
    worksheet.set_column(0, 0, 18)
    worksheet.write(0, 1, "Damage (J)", headerColor)
    worksheet.set_column(1, 1, 17)
    
    row = 1


    for case in damage:
        worksheet.write(row, 0, f"Accident#{damage.index(case)}", awariaColor)
        worksheet.write(row, 1, case)
        row +=1

    recordTable.close()    