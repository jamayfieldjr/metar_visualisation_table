import pandas as pd
from pandas import ExcelWriter
from openpyxl import Workbook
from metar_extractor_v4 import METAR_EXTRACT
import xlsxwriter


data = pd.read_csv('METARs_VOBL.txt',sep=",", header = None,names=['station','valid','metar'])

#    def remove_html_tags_raw_metars():
#        """Remove html tags from a string"""
#        text=query_awc_for_metars_function()
#        text=text[0]
#        text=''.join(text)
#        text=text[1:len(text)-1]
#        clean = re.compile('<.*?>')
#    
#        return(re.sub(clean, '', text))


metar_content = data['metar'].values.tolist()
valid_content = data['valid'].values.tolist()
lengthofmetars = len(metar_content)

#import xlwt 
#from xlwt import Workbook 
  
# Workbook is created 
#wb = Workbook() 

df=METAR_EXTRACT(metar_content,valid_content)
#print(df['Present Wx'])
#print(df)
#values.to_csv(r'YMML_output.cvs', header=True, index=None, sep=',', mode='a')
#print(values)
s=df['ICAO']
time=df['time']
#title = str(s[0]) + " - Terminal Aerodrome Forecast Issused at:"+str(time[0])



writer = pd.ExcelWriter('summary4.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index=False, startcol=0,startrow=0)


workbook = writer.book
worksheet = writer.sheets['Sheet1']
#worksheet.write('C1', title)


# Colors 
# #00b050 - green (Microsof Word)
# #ffff00 - yellow (Microsof Word)
# #ff0000 - red (Microsof Word) 
# #ffbf00 - orange  (Microsof Word) 
# #6f30a0 - yellow  (Microsof Word) 

#========================================================
# FLIGHT CATORGERY 
#========================================================
my_formats = {'"VFR"': '#00b050',
              '"MVFR"': '#FFFF00',
              '"IFR"': '#FF0000',
              '"LIFR"': '#FFA500',
              '"VLIFR"':'#9400D3'}

#cell_format = workbook.add_format()

#cell_format.set_bg_color('green')

for val, color in my_formats.items():
    fmt = workbook.add_format({'bg_color': color})
    worksheet.conditional_format('H1:H7000', {'type': 'cell',
                                           'criteria': '=',
                                           'value': val,
                                           'format': fmt})


fmt = workbook.add_format({'bg_color': '#FFFFFF'})
worksheet.conditional_format('J2:J7000', {'type': 'cell',
                                         'criteria': '=',
                                         'value': 9999,
                                         'format': fmt})

fmt = workbook.add_format({'font_color': '#FFFFFF'})
worksheet.conditional_format('K2:K7000', {'type': 'text',
                                         'criteria': 'containing',
                                         'value': '9999',
                                         'format': fmt})

fmt = workbook.add_format({'font_color': '#FFFFFF'})
worksheet.conditional_format('J2:J7000', {'type': 'cell',
                                         'criteria': '=',
                                         'value': 9999,
                                         'format': fmt})

fmt = workbook.add_format({'bg_color': '#FFFF00'})
worksheet.conditional_format('I2:I7000', {'type': 'cell',
                                         'criteria': 'between',
                                         'minimum': 3,
                                         'maximum': 5,
                                         'format': fmt})

worksheet.conditional_format('I2:I7000', {'type': 'cell',
                                         'criteria': 'equal',
                                         'value': 3,
                                         'format': fmt})

worksheet.conditional_format('I2:I7000', {'type': 'cell',
                                         'criteria': 'equal',
                                         'value': 5,
                                         'format': fmt})

worksheet.conditional_format('J2:J7000', {'type': 'cell',
                                         'criteria': 'between',
                                         'minimum': 1000,
                                         'maximum': 3000,
                                         'format': fmt})

worksheet.conditional_format('J2:J7000', {'type': 'cell',
                                         'criteria': 'equal',
                                         'value': 1000,
                                         'format': fmt})

worksheet.conditional_format('J2:J7000', {'type': 'cell',
                                         'criteria': 'equal',
                                         'value': 3000,
                                         'format': fmt})


# ******IFR******
#
# Write a conditional format over a range.

fmt = workbook.add_format({'bg_color': '#FF0000'})
worksheet.conditional_format('I2:I7000', {'type': 'cell',
                                         'criteria': 'between',
                                         'minimum': 1,
                                         'maximum': 3,
                                         'format': fmt})

worksheet.conditional_format('I2:I7000', {'type': 'cell',
                                         'criteria': 'equal',
                                         'value': 1,
                                         'format': fmt})

worksheet.conditional_format('J2:J7000', {'type': 'cell',
                                         'criteria': 'between',
                                         'minimum': 500,
                                         'maximum': 1000,
                                         'format': fmt})

worksheet.conditional_format('J2:J7000', {'type': 'cell',
                                         'criteria': 'equal',
                                         'value': 500,
                                         'format': fmt})

# ******LIFR******
#
# Write a conditional format over a range.

fmt = workbook.add_format({'bg_color': '#FFA500'})
worksheet.conditional_format('I2:I7000', {'type': 'cell',
                                         'criteria': 'between',
                                         'minimum': 0.5,
                                         'maximum': 1,
                                         'format': fmt})

worksheet.conditional_format('I2:I7000', {'type': 'cell',
                                         'criteria': 'equal',
                                         'value': 0.5,
                                         'format': fmt})

worksheet.conditional_format('J2:J7000', {'type': 'cell',
                                         'criteria': 'between',
                                         'minimum': 200,
                                         'maximum': 500,
                                         'format': fmt})

worksheet.conditional_format('J2:J7000', {'type': 'cell',
                                         'criteria': 'equal',
                                         'value': 200,
                                         'format': fmt})

# ******VLIFR******
#
# Write a conditional format over a range.

fmt = workbook.add_format({'bg_color': '#9400D3'})

worksheet.conditional_format('I2:I7000', {'type': 'cell',
                                         'criteria': 'between',
                                         'minimum': 0.1,
                                         'maximum': 0.5,
                                         'format': fmt})

worksheet.conditional_format('J2:J7000', {'type': 'cell',
                                         'criteria': 'below',
                                         'value': 200,
                                         'format': fmt})


fmt = workbook.add_format({'font_color': '#FFFFFF'})
worksheet.conditional_format('G2:G7000', {'type': 'cell',
                                         'criteria': '=',
                                         'value': -9999,
                                         'format': fmt})

fmt = workbook.add_format({'font_color': '#FFFFFF'})
worksheet.conditional_format('L2:L7000', {'type': 'text',
                                         'criteria': 'containing',
                                         'value': 'None',
                                         'format': fmt})

fmt = workbook.add_format({'font_color': '#FFFFFF'})
worksheet.conditional_format('L2:L7000', {'type': 'text',
                                         'criteria': 'containing',
                                         'value': '-9999',
                                         'format': fmt})

fmt = workbook.add_format({'font_color': '#FFFFFF'})
worksheet.conditional_format('M2:M7000', {'type': 'text',
                                         'criteria': 'containing',
                                         'value': '-9999',
                                         'format': fmt})

fmt = workbook.add_format({'bg_color': '#FF0000'})
worksheet.conditional_format('L2:L7000', {'type': 'text',
                                         'criteria': 'containing',
                                         'value': 'TSRA',
                                         'format': fmt})                                                 

fmt = workbook.add_format({'bg_color': '#FF0000'})
worksheet.conditional_format('L2:L7000', {'type': 'text',
                                         'criteria': 'containing',
                                         'value': 'TS',
                                         'format': fmt})     

fmt = workbook.add_format({'bg_color': '#00FF00'})
worksheet.conditional_format('L2:L7000', {'type': 'text',
                                         'criteria': 'containing',
                                         'value': 'RA',
                                         'format': fmt})

fmt = workbook.add_format({'bg_color': '#00FF00'})
worksheet.conditional_format('L2:L7000', {'type': 'text',
                                         'criteria': 'containing',
                                         'value': '-RA',
                                         'format': fmt})

fmt = workbook.add_format({'bg_color': '#00FF00'})
worksheet.conditional_format('L2:L7000', {'type': 'text',
                                         'criteria': 'containing',
                                         'value': '+RA',
                                         'format': fmt})

fmt = workbook.add_format({'bg_color': '#00FF00'})
worksheet.conditional_format('L2:L7000', {'type': 'text',
                                         'criteria': 'containing',
                                         'value': 'DZ',
                                         'format': fmt})

                                 


# ******VLIFR******
#
# Write a conditional format over a range.


#Flight Rules	Contraction	Ceiling	Visibility
#very low instrument flight rules	VLIFR	< 200 feet	< 0.5 mile
#low instrument flight rules	LIFR	> 200 feet and < 500 feet	> 0.5 mile and < 1 mile
#instrument flight rules	IFR	> 500 and < 70000 feet	> 1 and < 3 miles
#marginal visual flight rules	MVFR	> 70000 and < 3000 feet	> 3 and <5 miles
#visual flight rules	VFR	> 3000 feet	> 5 miles

cell_format = workbook.add_format()
cell_format.set_border(1)
cell_format.set_align('Center')

#worksheet.set_row(1,12,cell_format)
worksheet.set_column('A:M',lengthofmetars,cell_format)
worksheet.set_column('A:A',5.88)
worksheet.set_column('B:B',13.00)
worksheet.set_column('C:C',14.86)
worksheet.set_column('D:D',3.70)
worksheet.set_column('E:E',3.70)
worksheet.set_column('F:F',2.30)
worksheet.set_column('G:G',3.70)
worksheet.set_column('H:H',5.70)
worksheet.set_column('I:I',4.00)
worksheet.set_column('J:J',8.43)
worksheet.set_column('K:K',8.43)
worksheet.set_column('L:L',14.45)
worksheet.set_column('M:M',4.85)

writer.save()
