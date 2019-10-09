
# IMPORT LIBS
import re
import pytaf
from datetime import datetime
import pandas as pd
from metar import Metar
from fractions import Fraction
from speci_group import speci_group_function
from collections import OrderedDict


class METAR_EXTRACT(object)
    def __init__(self, taf):
        if isinstance(taf, TAF):
            self._taf = taf
        else:
            raise DecodeError("Argument is not a METAR parser object")
                    
                 
    def speci_group_function():
        """ 
        Function IDs SPECI and ROUTINUE METARs
        Outputs:n SPECI or ROUTINUE METARs
        """
        speci_object=re.compile(r'SPECI')
        speci_array=[]
        contents00 =[]
        for values in content01:
            speci_match =speci_object.search(values)
            if speci_match:
                speci_array.append('SPECI  ')
                values=re.sub('SPECI', '',values)
                contents00.append(values)
            else:
                speci_array.append('ROUTINE')
                contents00.append(values)
           
        return(content01,speci_array)

    #print(speci_group_function())

#    print('===========>')
#    print('=========================>METAR COMPLETED speci_group_function')

    def time_group_function(content02):
        """ 
        Function built to extract time from pytaf using any METARs  
        Extracts - 'origin_minutes',' origin_hours', 'orgin_date'
        """
        time_array = []
        for values in content02:
            #print(values)
            YYYY = values[0:4]
            MM = values[5:7]
            DD = values[8:10]
            hh = values[11:13]
            mm = values[14:16]
            #print(YYYY,MM,DD,hh,mm)
            #print(datetime(int(YYYY), int(MM), int(DD),int(hh),int(mm)).strftime('%Y-%m-%d %H:%M'))
            time_array.append(datetime(int(YYYY), int(MM), int(DD),int(hh),int(mm)).strftime('%Y-%m-%d %H:%M'))

    
        return(time_array)

#    print('===========>')
#    print('=========================>METAR COMPLETED time_group_function')

    def visibility_group_function():
        """
        Function built for extracting taf._weather_groups[X]["visibility"]
        Attribute "winds" has 2 outputs
        'visibility': None 
        or
        'visibility':{'more': P, 'range': '3', 'unit': 'SM'}
        'visibility':{'range': '10 000', 'more': True, 'unit': 'M'}
        """
        visibility_array = []
        for values in content01:
            taf = pytaf.TAF(values)
            weather_groups = taf._weather_groups
            visibilitytf = weather_groups[0]["visibility"]    
            if not visibilitytf:
                res2 = 10
                visibility_array.append(res2)
            else:
                if weather_groups[0]["visibility"]["unit"] == 'M':

                    if weather_groups[0]["visibility"]["range"] == '10 000':
                        res2 = 10 
                        visibility_array.append(res2)
                    else:    
                        if int(weather_groups[0]["visibility"]["range"])<900:
                            res2 = 0.125 
                        elif 900<=int(weather_groups[0]["visibility"]["range"])<1200:
                            res2 = 0.5 
                        elif 1200<=int(weather_groups[0]["visibility"]["range"])<1600:
                            res2 = 0.75
                        elif 1600<=int(weather_groups[0]["visibility"]["range"])<3200:
                            res2 = 1 
                        elif 3200<=int(weather_groups[0]["visibility"]["range"])<4800:
                            res2 = 2 
                        elif 4800<=int(weather_groups[0]["visibility"]["range"])<6000:
                            res2 = 3 
                        elif 6000<=int(weather_groups[0]["visibility"]["range"])<8000:
                            res2 = 4 
                        elif 8000<=int(weather_groups[0]["visibility"]["range"])<9000:
                            res2 = 5 
                        elif 9000>=int(weather_groups[0]["visibility"]["range"]):
                            res2 = 10
                        visibility_array.append(res2)
                else:
                    res2 = weather_groups[0]["visibility"]["range"]    
                    if (' ' in res2) == True:
                        res2=res2.split()
                        res3=Fraction(res2[1])
                        res2=int(res2[0])+float(res3)
                    else:
                        if ('/' in res2) == True:
                           res2=Fraction(res2)
                           res2=float(res2)
                        else: 
                            res2=float(res2)
                    visibility_array.append(res2)
                visibilitytf = []
      
        return(visibility_array)

#    print('===========>')
#    print('=========================>METAR COMPLETED visibility_group_function')

    def time_range_function(): 
        time_array=time_group_function(content02)     
        time_array = time_array[0:len(time_array)-1] 
        res =[]
        ds = []
        index_starttime = [i for i in range(len(time_array)-1)]
        index_starttime  = [i+1 for i in index_starttime]
        index_endtime = [i for i in range(len(time_array)-1)]
        for values01,values02,values03 in zip(time_array,index_starttime,index_endtime):
            startime=datetime.strptime(time_array[values02],'%Y-%m-%d %H:%M')
            endtime=datetime.strptime(time_array[values03],'%Y-%m-%d %H:%M')
  
            res= startime - endtime  
            res=(':'.join(str(res).split(':')[:2]))
            ds.append(res)

        return(ds)

#    print('===========>')
#    print('=========================>METAR COMPLETED time_range_function')


    def clouds_group_function():
        """
        Function built for extracting taf._weather_groups[X]["clouds"]
        Attribute "Clouds" has 2 outputs
        'clouds': None 
        or 
        'clouds': [{'layer': 'XXX', 'ceiling': 'XXX', 'type': XXX}] 
        """
        layer_val = []
        ceiling_val =[]
        clouds_array = [layer_val, ceiling_val]
        for values in content01:
            #print(values)
            res1 = []
            res2 = []
            taf = pytaf.TAF(values)
            weather_groups = taf._weather_groups  
            cloudstf = weather_groups[0]["clouds"]
            vvtf = weather_groups[0]["vertical_visibility"]
            results3 =[]
            results4 =[] 
            if not cloudstf and not vvtf:
                res1 = ["-9999"]
                res2 = ["-9999"]
                layer_val.append(res1)
                ceiling_val.append(res2)
            elif vvtf:
                res1 = ["VV"]
                res2 = [weather_groups[0]["vertical_visibility"]]
                layer_val.append(res1)
                ceiling_val.append(res2)
            elif cloudstf and not vvtf: 
                if weather_groups[0]["clouds"][0]["layer"] == 'CLR' or weather_groups[0]["clouds"][0]["layer"] == 'CAVOK' or weather_groups[0]["clouds"][0]["layer"] == 'NSC' or weather_groups[0]["clouds"][0]["layer"] == 'SKC'or weather_groups[0]["clouds"][0]["layer"] == 'NCD':
                    res1 = ["CLR"]
                    res2 = ["9999"]
                    layer_val.append(res1)
                    ceiling_val.append(res2)
                else:
                    for k in range(0,len(weather_groups[0]["clouds"])): 
                        #print(weather_groups[0]["clouds"])
                        res1 = weather_groups[0]["clouds"][k]["layer"]
                        res2 = weather_groups[0]["clouds"][k]["ceiling"]
                        results3.append(res1)
                        results4.append(res2)
                    layer_val.append(results3)
                    ceiling_val.append(results4)
            cloudstf = []

        return(clouds_array)

#    print('===========>')
#    print('=========================>METAR COMPLETED clouds_group_function')

    def present_wx_group_function():
        """
        Function built for extracting taf._weather_groups[X]["weather"]
        Attribute "Weather" has 3 outputs
        'weather': None 
        or 
        'weather': [{'intensity': XXX, 'modifier': XXX, 'phenomenon': XXX}] 
        """
        present_wx=[]
        for values in content01:
            res1 = []
            res2 = []
            #print(values)
            taf = pytaf.TAF(values)
            weather_groups = taf._weather_groups  
            weathertf = weather_groups[0]["weather"]
            res1 = []
            res2 = []
            res3 = []
            res4 = []
            results1=[]

            if not weathertf:

                res1 = "None"              
                present_wx.append(res1)

            elif weathertf: 
                if len(weather_groups[0]["weather"]) == 1:
                    res1 = weather_groups[0]["weather"][0]["intensity"]
                    res2 = weather_groups[0]["weather"][0]["modifier"]
                    res3 = weather_groups[0]["weather"][0]["phenomenon"]
                    res4=res1+res2+res3
                    res4="".join(res4)
                    res4 = "".join(OrderedDict.fromkeys(res4))
                    present_wx.append(res4)
                else:
                    for k in range(0,len(weather_groups[0]["weather"])): 
                        res1 = weather_groups[0]["weather"][k]["intensity"]
                        res2 = weather_groups[0]["weather"][k]["modifier"]
                        res3 = weather_groups[0]["weather"][k]["phenomenon"]
                        res4=res1+res2+res3
                        res4="".join(res4)
                        results1.append(res4)
                    results1=" ".join(results1)
                    print(results1)
                    results1 = "".join(OrderedDict.fromkeys(results1))
                    present_wx.append(results1)
            weathertf = []

        return(present_wx)
    
#    print('===========>')
#    print('=========================>METAR COMPLETED present_wx_function')
    #print(present_wx_group_function())

   # Obscuration
    def present_wx_group_function_2():
        dumby01=[]
        dumby02=[]
        present_wx = present_wx_group_function()
        for value in present_wx:
            value=value.replace('BR', '').replace('HZ', '').replace('FU', '').replace('DU', '').replace('BLSN', '').replace('BLDU', '').replace('FG', '').replace('FZFG', '').replace('MIFG', '').replace('PRFG','')
            dumby01.append(value)
        

        for value in dumby01:
            if value=='':
               dumby02.append('-9999')
            else:
               dumby02.append(value)

        return(dumby02)

#    print('===========>')
#    print('=========================>METAR COMPLETED present_wx_function')
    #print(present_wx_group_function_2())

    def visibility_obscuration_function():
        dumby01 =[]
        present_wx = present_wx_group_function()
        for value in present_wx:   
            obscuration_object=re.compile(r'(BLSN\sFZFG)|(BLSN\sFG)|(BR)|(HZ)|(FU)|(DU)|(BLSN)|(BLDU)|(FG)|(FZFG)|(MIFG)|(PRFG)')
            obscuration_match = obscuration_object.search(value)
            if obscuration_match:
                obscuration_string = obscuration_match.group()
                dumby01.append(obscuration_string)
            else:
                obscuration_string = '-9999'
                dumby01.append(obscuration_string)
    
        return(dumby01)

#    print('===========>')
#    print('=========================>METAR COMPLETED visibility_obscuration_function')
    #print(visibility_obscuration_function())

    def lowest_cloud_group_function():
        clouds=clouds_group_function()
        cloudx_layers = clouds[0]
        cloudx_heights =clouds[1]
        cloud_layer=[]
        cloud_height=[]
        for values00,values01 in zip(cloudx_layers,cloudx_heights):
            results1 = []
            results2 = []
            res1 = []
            res2 = [] 
            for values02,values03 in zip(values00,values01):
                if values02=='BKN' or values02=='OVC' or values02=='VV':
                    res1 = values02
                    res2 = int(values03) * 100   
                    results1.append(res1)
                    results2.append(res2)
                elif values02=='CLR' or values02=='FEW' or values02=='SCT':
                    res1 = '9999'
                    res2 = 9999   
                    results1.append(res1)
                    results2.append(res2)
                elif values02=='-9999':
                    res1 = '-9999'
                    res2 = -9999
                    results1.append(res1)
                    results2.append(res2)
            cloud_layer.append(results1)
            cloud_height.append(results2)
            
            lowest_cloud_height=[]
            lowest_cloud_layer=[]
            lowest=[]

            for zabby1,zabby2 in zip(cloud_height,cloud_layer):
                res3 = min(zabby1)
                index_cloud = zabby1.index(min(zabby1))
                res4 = zabby2[index_cloud]
                lowest_cloud_height.append(res3)
                lowest_cloud_layer.append(res4)

            lowest = [lowest_cloud_height, lowest_cloud_layer] 

        return(lowest)

#    print('===========>')
#    print('=========================>METAR COMPLETED lowest_cloud_group_function')

    def wind_group_function():
        """
        Function built for extracting taf._weather_groups[X]["winds"]
        Attribute "Clouds" has 2 outputs
        'wind': None 
        or 
        wind': {'direction': '210', 'speed': '06', 'gust': None, 'unit': 'KT'}
        """
        direction_val =[]
        speed_val =[]
        gust_val =[]
        unit_val = []
        wind_array = [direction_val,speed_val,gust_val,unit_val]
        for values in content01:
            #print(values)
            taf = pytaf.TAF(values)
            weather_groups = taf._weather_groups  
            windtf = weather_groups[0]["wind"]
            #print(windtf)
            if not windtf:
                res1 = -9999
                res2 = -9999
                res3 = -9999
                res4 = -9999
                direction_val.append(res1)
                speed_val.append(res2)
                gust_val.append(res3)
                unit_val.append(res4)
            else:
                if weather_groups[0]["wind"]["direction"] == 'VRB':
                    res1 = 777
                    res2 = int(weather_groups[0]["wind"]["speed"])
                    res4 = weather_groups[0]["wind"]["unit"]
                    direction_val.append(res1)
                    speed_val.append(res2)
                    unit_val.append(res4)
                else: 
                    res1 = int(weather_groups[0]["wind"]["direction"])
                    res2 = int(weather_groups[0]["wind"]["speed"])
                    res4 = weather_groups[0]["wind"]["unit"]
                    direction_val.append(res1)
                    speed_val.append(res2)
                    unit_val.append(res4)
            if not weather_groups[0]["wind"]["gust"]:
                res3 = -9999 
                gust_val.append(res3)
            else:
                res3 = weather_groups[0]["wind"]["gust"]
                gust_val.append(res3)
            windtf = []
        
        return(wind_array)

    #p = wind_group_function()
    #print(p[2])
#    print('===========>')
#    print('=========================>METAR COMPLETED wind_group_function')


    def flight_cat_function():
        cloud_array = lowest_cloud_group_function()
        cloud_array = cloud_array[0]
        visibility_array = visibility_group_function()    
        flt_cat = []
        for val01,val02 in zip(visibility_array,cloud_array): 
            res=[]
            if (val01<0.5 and val02<200) or (val01<0.5 and not val02<200) or (val02<200 and not val02<1/2): 
                res='VLIFR'
            elif (0.5<=val01<1 and 200<=val02<500) or (0.5<=val01<1 and not 200<=val02<500) or (200<=val02<500 and not 0.5<=val01<1):
                res='LIFR'
            elif (1<=val01<3 and 500<=val02<1000) or (1<=val01<3 and not 500<=val02<1000) or (500<=val02<1000 and not 1<=val01<3):
                res='IFR'
            elif (3<=val01<=5 and 1000<=val02<=3000) or (3<=val01<=5 and not 1000<=val02<=3000) or (1000<=val02<=3000 and not 3<=val01<=5):
                res='MVFR' 
            elif val01>5 and val02>3000:
                res='VFR' 
            flt_cat.append(res)
        return(flt_cat)    

#    print('===========>')
#    print('=========================>METAR COMPLETED flight_cat_function')

    def icao_get_function():
        icao = []
        for values in content01:
            taf = pytaf.TAF(values)
            icao.append(taf._taf_header["icao_code"])
        return(icao)

#    print('===========>')
#    print('=========================>METAR COMPLETED icao_get_function')

    def build_table():
        wind_array = wind_group_function()
        visibility_array = visibility_group_function()
        time_array = time_group_function(content02)
        delta = time_range_function()
        speci=speci_group_function()
        flt_cat=flight_cat_function()
        icao = icao_get_function()
        present_wx_array=present_wx_group_function_2()
        vis_obscur_wx_array=visibility_obscuration_function()
        dmicao = pd.DataFrame({'ICAO' : icao})
        lowest_clouds = lowest_cloud_group_function()
        dmtime = pd.DataFrame({'time': time_array})
        dmvis = pd.DataFrame({'vis': visibility_array})
        dmdt = pd.DataFrame({'dt': delta})
        dms = pd.DataFrame({'Message Type': speci[1]})
        dmwx = pd.DataFrame({'Present Wx':present_wx_array})
        dmch = pd.DataFrame({'Cld Hgt': lowest_clouds[0]})
        dmcl = pd.DataFrame({'Cld Type': lowest_clouds[1]})
        dmwd = pd.DataFrame({'ddd': wind_array[0]})
        dmws = pd.DataFrame({'ff': wind_array[1]})
        dmwg = pd.DataFrame({'gg': wind_array[2]})
        dmfc = pd.DataFrame({'Flt Cat' : flt_cat})
        dmov = pd.DataFrame({'Vis Obc':vis_obscur_wx_array})
        result = pd.concat([dmicao,dms,dmtime,dmdt,dmwd,dmws,dmwg,dmfc,dmvis,dmch,dmcl,dmwx,dmov], axis=1, sort=False)
        return(result)

#    print('===========>')
#    print('=========================>METAR COMPLETED build_table')

    print('METAR JOB METAR COMPLETED')

    return(build_table())
