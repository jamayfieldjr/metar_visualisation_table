""" Libaries and Modules """
import re
from datetime import datetime,timedelta
from urllib.request import urlopen
from bs4 import BeautifulSoup
from TAF_range_time import TAF_time_range_function

def metar_collector(ICAO,hours):

    """ICAO == KMEM, EHAM, etc. 
    HH = hours you want to look at """

    def remove_html_tags(text):
        """Remove html tags from a string"""
        import re
        clean = re.compile('<.*?>')
        return(re.sub(clean, '', text))

    def query_awc_for_metars_function(): 
        url='https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString='+ICAO+'&hoursBeforeNow='+hours 
        html = urlopen(url)
        soup = BeautifulSoup(html,"html.parser")
        text = str(soup.find_all('raw_text'))
        metartype = str(soup.find_all('metar_type'))
        lines=text.splitlines()
        line_type=metartype.splitlines()
        return(lines,line_type)

    def remove_html_tags_raw_metars():
        """Remove html tags from a string"""
        text=query_awc_for_metars_function()
        text=text[0]
        text=''.join(text)
        text=text[1:len(text)-1]
        clean = re.compile('<.*?>')
    
        return(re.sub(clean, '', text))
  
    def remove_html_tags_type():
        """Remove html tags from a string"""
        text=query_awc_for_metars_function()
        text=text[1]
        text=''.join(text)
        text=text[1:len(text)-1]
        clean = re.compile('<.*?>')
    
        return(re.sub(clean, '', text))


    def adding_final_touchs():

        text=remove_html_tags_raw_metars() 
        line_type=remove_html_tags_type()
        text=re.split(",",text)
        line_type=re.split(",",line_type)
        reference_index = [i for i in range(len(text))]

        for values00,values01 in zip(text,reference_index):
            text[values01] = values00 + ' ='      
        
        line_type = list(reversed(line_type))
        text = list(reversed(text))
        return(text,line_type)

    text = adding_final_touchs()
    return(text)
