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
