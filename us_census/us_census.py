import requests
import json 
import pandas as pd 
import os
import matplotlib.pyplot as plt
import numpy as np


#american community survey year data - detailed tables
def AmComSurv(year, group, key, yr): #example: year= 2019, group= B01001, key
    """
    Gets detailed tables for a year given the group number in the american community index. 

    Parameters
    ----------
    year:
        Only full 4-integer values for years where the Community Survey is available, 2009-2019
    group:
        Subgroup of population, indexed by list provided in API documentation.
    key:
        API key requested from US census.gov website
    yr:
        Only inputs are 1, 3, or 5 for 1 year, 3 year, and 5 year data. If the input is 3 or 5, then the function subtracts from the year argument. Hence, if year is 2010 and yr is 3, data returned will be from 2007-2010.
        
    Returns
    -------
    Pandas dataframe extracted with the inserted parameters from the American Community Survey.

    Examples
    --------
    >>> from us_census import us_census
    >>> AmComSurv(2019, 'B01001', MYKEY, '1')
     """

    
    assert isinstance(year, int), "Years must be specified in full integer format, e.g. 2019"
    assert isinstance(group, str), "Make sure you have input the string version of the group."
    assert isinstance(key, str), "Make sure your key input is the string version of your key."

    r= requests.get(f'https://api.census.gov/data/{year}/acs/acs{yr}?get=NAME,group({group})&for=us:1&key={key}')
    
    if r.status_code== 200: 
        try:
            df= pd.DataFrame(r.json())
            return df
        except (NameError):
            print("This group was not found, please try a valid group for the American Community Survey Year Data.")


#american community survey year data - detailed tables
def AmComSurvSubjects(year, group, key, c=""):  
        """
    Gets either comparison tables and subject tables for a year given the group number in the american community index. 

    Parameters
    ----------
    year:
        Only full 4-integer values for years where the Community Survey is available, 2009-2019
    group:
        Subgroup of population, indexed by list provided in API documentation.
    key:
        API key requested from US census.gov website
    c:
        Gets subject tables or comparison profiles for a year given the group number in the american community index
        if c=c, then comparison table returns. Otherwise subject table is returned. 
        
    Returns
    -------
    Pandas dataframe extracted with the inserted parameters from the American Community Survey.

    Examples
    --------
    >>> from us_census import us_census
    >>> AmComSurvSubjects(2019, "CP05", MYKEY, c='c')
     """
    assert isinstance(year, int), "Years must be specified in full integer format, e.g. 2019"
    assert isinstance(group, str), "Make sure you have input the string version of the group."
    assert isinstance(key, str), "Make sure your key input is the string version of your key."
    r= requests.get(f'https://api.census.gov/data/{year}/acs/acs1/{c}profile?get=group({group})&for=us:1&key={key}')
    if r.status_code== 200: 
        try:
            df= pd.DataFrame(r.json())
            return df
        except (NameError):
            print("This group was not found, please try a valid group for the American Community Survey Year Data.")


def AmComSurv_PopProfile(year, group, popgroup, key): #example: AmComSurv_PopProfile(2019, 'S0201', '001', MYKEY)
    """
    Gets selected population profiles for a year given the group number and population subgroup in the american community index. 

    Parameters
    ----------
    year:
        Only full 4-integer values for years where the Community Survey is available, 2009-2019
    group:
        Subgroup of population, indexed by list provided in API documentation.
    popgroup:
        Subgroup of the population (more specificly indexed by demographics than the group parameter)
    key:
        API key requested from US census.gov website

        
    Returns
    -------
    Pandas dataframe extracted with the inserted parameters from the American Community Survey.

    Examples
    --------
    >>> from us_census import us_census
    >>> AmComSurv_PopProfile(2009, 'S0201', '001', MYKEY)
     """

    assert isinstance(year, int), "Years must be specified in full integer format, e.g. 2019"
    assert isinstance(group, str), "Make sure you have input the string version of the group."
    assert isinstance(key, str), "Make sure your key input is the string version of your key."
    assert isinstance(popgroup, str), "Make sure your popgroup input is a string"
    r= requests.get(f'https://api.census.gov/data/{year}/acs/acs1/spp?get=NAME,group({group})&for=us:1&POPGROUP={popgroup}&key={key}')
    if r.status_code== 200: 
        try:
            df= pd.DataFrame(r.json())
            return df
        except (NameError):
            print("This group was not found, please try a valid group for the American Community Survey Year Data.")
    

def YrSupplemental(year, key,state= "*"): 
 """
    Returns selected supplemental estimate data for all states in the given year. Has options for specifying a state. 

    Parameters
    ----------
    year:
        Only full 4-integer values for years where the Community Survey is available, 2009-2019
    state:
        takes state code in string format for state-wide information
    key:
        API key requested from US census.gov website

        
    Returns
    -------
    Pandas dataframe extracted with the inserted parameters from the Supplemental Year Survey 

    Examples
    --------
    >>> from us_census import us_census
    >>> YrSupplemental(2019, MYKEY)
     """
    assert isinstance(year, int),  "Years must be specified in full integer format, e.g. 2019"
    assert isinstance(state, str), "Please check the official US Census list for available state abbreviations, state must be a string"
    r= requests.get(f'https://api.census.gov/data/{year}/acs/acsse?get=NAME,K200101_001E&for=state:{state}&key={key}')
    if r.status_code== 200: 
        try:
            df= pd.DataFrame(r.json())
            return df
        except (NameError):
            print("This state, year, or key was not found, please try valid inputs for the American Community Supplemental estimates.")

def entrepreneur(year,key, state= "*", micro= False):  
    """Returns data on entrepreneurship information by state. If micro = true, then it will return micro metropolitan data by state for specified areas.

    Parameters
    ----------
    year:
        Only full 4-integer values for years where the Community Survey is available, 2009-2019
    state:
        takes state code in string format for state-wide information
    key:
        API key requested from US census.gov website, string format
    micro:
        Boolean value specifying whether or not the return dataframe should have microdata or not

        
    Returns
    -------
    Pandas dataframe extracted with the inserted parameters from the entrepreneurship survey

    Examples
    --------
    >>> from us_census import us_census
    >>> entrepreneur(2016, MYKEY)""" 
    assert isinstance(year, int),  "Years must be specified in full integer format, e.g. 2019"
    assert isinstance(state, str), "Please check the official US Census list for available state abbreviations, state must be a string"
    assert isinstance(micro, bool), "Make sure micro is set to true or false."
    if micro== False:
        r= requests.get(f'https://api.census.gov/data/{year}/ase/csa?get=VET_GROUP_LABEL&for=state:{state}&key={key}')
        if r.status_code== 200: 
            try:
                df= pd.DataFrame(r.json())
                return df
            except (NameError):
                print("This state, year, or key was not found, please try valid inputs for the American Entrepreneurship Survey.")
    elif micro== True: 
        r= requests.get(f'https://api.census.gov/data/{year}/ase/csa?get=VET_GROUP_LABEL&for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:*&key={key}')
        if r.status_code == 200: 
            try:
                df= pd.DataFrame(r.json())
                return df
            except (NameError):
                print("This state, year, or key was not found, please try valid inputs for the American Entrepreneurship Survey.")

def business(year, key, state= '*', micro= False):
    """"Gives statistics for the characteristics of a business, has option for microdata using micro=True..

    Parameters
    ----------
    year:
        Only full 4-integer values for years where the Community Survey is available, 2009-2019
    state:
        takes state code in string format for state-wide information
    key:
        API key requested from US census.gov website, string format
    micro:
        Boolean value specifying whether or not the return dataframe should have microdata or not

        
    Returns
    -------
    Pandas dataframe extracted with the inserted parameters from the entrepreneurship survey

    Examples
    --------
    >>> from us_census import us_census
    >>> business(2016, MYKEY)""" 
    assert isinstance(year, int),  "Years must be specified in full integer format, e.g. 2019"
    assert isinstance(state, str), "Please check the official US Census list for available state abbreviations, state must be a string"
    assert isinstance(micro, bool), "Make sure micro is set to true or false."
    if micro== False:
        r= requests.get(f'https://api.census.gov/data/{year}/ase/cscb?get=RCPPDEMP_F&for=state:{state}&key={key}')
        if r.status_code== 200: 
            try:
                df= pd.DataFrame(r.json())
                return df
            except (NameError):
                print("This state, year, or key was not found, please try valid inputs for the American Business Survey.")
    elif micro== True: 
        r= requests.get(f'https://api.census.gov/data/{year}/ase/cscb?get=RCPPDEMP_F&for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:*&key={key}')
        if r.status_code == 200: 
            try:
                df= pd.DataFrame(r.json())
                return df
            except (NameError):
                print("This state, year, or key was not found, please try valid inputs for the American Business Survey.")

def manufacturing(year,manu, key): 
    """"Returns information on a given manufacturing sector in a given year's survey across the US.

    Parameters
    ----------
    year:
        Only full 4-integer values for years where the Community Survey is available, 2009-2019
    manu:
        string for a manufacturing sector code
    key:
        API key requested from US census.gov website, string format

        
    Returns
    -------
    Pandas dataframe extracted with the inserted parameters from the entrepreneurship survey

    Examples
    --------
    >>> from us_census import us_census
    >>> manufacturing(2017, '31-33', MYKEY)""" 
    assert isinstance(year, int),  "Years must be specified in full integer format, e.g. 2019"
    assert isinstance(manu, str), "Please check the official US Census list for available manufacturing sector abbreviations, must be a string"
    r= requests.get(f'https://api.census.gov/data/timeseries/asm/area{year}?get=NAICS{year}_LABEL,NAICS{year},EMP&for=us:*&YEAR={year+1}&NAICS{year}={manu}&key={key}')
    if r.status_code== 200: 
        try:
            df= pd.DataFrame(r.json())
            return df
        except (NameError):
            print("This state, year, survey number, or manufacturing sector code was not found. Please try valid inputs for the American Manufacturing survey .")

def state_manufacturing(key, year,manu, crosssection, state='*'): #cross-section can equal state or industry only
    """"Getting state manunfacturing data for a certain sector, can provide nation-wide or specific state data.

    Parameters
    ----------
    year:
        Only full 4-integer values for years where the Community Survey is available, 2009-2019
    manu:
        string for a manufacturing sector code
    key:
        API key requested from US census.gov website, string format

    crosssection:
        only takes the string arguments 'state' or 'industry' to return a dataframe across the specified cross-section.
    state:
        string argument for state code 

    Returns
    -------
    Pandas dataframe extracted with the inserted parameters from the census manufacturing survey

    Examples
    --------
    >>> from us_census import us_census
    >>> state_manufacturing(MYKEY, 2016, '31-33', 'state')""" 
    assert isinstance(state, str), "Please check the official US Census list for available state abbreviations, state must be a string"
    assert isinstance(year, int), "Please only ask for available years and ensure the year entry is an integer"
    assert isinstance(manu, str), "Ensure the manufacturing sector is viable"
    r= requests.get(f'https://api.census.gov/data/timeseries/asm/{crosssection}?get=NAICS_TTL,EMP,GEO_TTL&for=state:{state}&YEAR={year}&NAICS={manu}&key={key}')
    if r.status_code== 200: 
        try:
            df= pd.DataFrame(r.json())
            return df
        except (NameError):
            print("This state, year, or manufacturing sector code was not found. Please try valid inputs for the American Manufacturing survey .")
    else:
        print("An error occured with your get request. Please check your inputs again.")


def unemployed(year,manu, key,state='*'): #ex manu= 54 is professional, scientific, and technical service industries, year= 2017
    """"Yearly data on self-employed manufacturing sectors for all counties. Returns all receipts in thousands of dollars for all counties for the specified state for certain industries.

    Parameters
    ----------
    year:
        Only full 4-integer values for years where the Community Survey is available, 2009-2019
    manu:
        string for a manufacturing sector code
    key:
        API key requested from US census.gov website, string format

    state:
        string argument for state code 

    Returns
    -------
    Pandas dataframe extracted with the inserted parameters from the census manufacturing survey

    Examples
    --------
    >>> from us_census import us_census
    >>> unemployed(2002, '54', MYKEY, '02')""" 
    assert isinstance(year, int), "Please only ask for available years and ensure the year entry is an integer"
    assert isinstance(manu, str), "Ensure the manufacturing sector is viable and a string."
    assert isinstance(state, str)
    r= requests.get(f'http://api.census.gov/data/{year}/nonemp?get=NRCPTOT,NAME&for=county:*&in=state:{state}&NAICS{year}={manu}&key={key}')
    if r.status_code== 200: 
        try:
            df= pd.DataFrame(r.json())
            return df
        except (NameError):
            print("This state, year, or manufacturing sector code was not found. Please try valid inputs for the American Manufacturing survey .")

def county_business_patterns(year, manu, state='*'):
    """Function that returns dataframe on county business patterns across different manufacturing industries, states, and years.

    Parameters
    ----------
    year:
        Only full 4-integer values for years where the Community Survey is available, 2009-2019
    manu:
        string for a manufacturing sector code

    state:
        string argument for state code 

    Returns
    -------
    Pandas dataframe extracted with the inserted parameters from the census manufacturing survey. No key necessary for this API.

    Examples
    --------
    >>> from us_census import us_census
    >>> county_business_patterns(2018, '72', state='06')""" 
    assert isinstance(year, int), "Please only ask for available years and ensure the year entry is an integer"
    assert isinstance(manu, str), "Ensure the manufacturing sector is viable and a string."
    r= requests.get(f'https://api.census.gov/data/{year}/cbp?get=ESTAB,LFO,NAICS{year-1}_LABEL,NAME&for=state:{state}&NAICS{year-1}={manu}')
    if r.status_code==200:
        try:
            df= pd.DataFrame(r.json())
            return df
        except(NameError):
            print('This state, year, or manufacturing sector code was not found. Please try valid inputs for the American Manufacturing survey .')

def get_econ(year1,subset, betweentime= False, year2='', m1= '', m2= ''): #subset=hv is housing, resconst is new residential reconstruction info
""" Function that extracts economic time-series data.
    Parameters
    ----------
    year1:
        Only full 4-integer values for years where the Community Survey is available, 2009-2019
    subset:
        string argument, can equal either 'hv' or 'resconst', 'hv' for current housing, 'resconcst' for new residential construction.

    betweentime:
        boolean for whether function will return time series or cross-section, across various years or one year only.
    year2:
        string for the end year of the time series if betweentime= True
    m1:
        optional argument for specific month of the beginning year of time series
    m2:
        optional argument for the end month of the end year of time series, year2. 

    Returns
    -------
    Pandas dataframe extracted with economic indicators across time or in a cross-section about housing and new constructions. 

    Examples
    --------
    >>> from us_census import us_census
    >>> get_econ(2018, 'hv')""" 
    assert isinstance(year1, int), "Year must be an integer"
    assert isinstance(subset, str), "Subset can be strings hv or resconst"
    if betweentime== False:
        r= requests.get(f'https://api.census.gov/data/timeseries/eits/{subset}?get=cell_value,data_type_code,time_slot_id,category_code,seasonally_adj&time={year1}')
        if r.status_code==200: 
            try:
                df= pd.DataFrame(r.json())
                return df
            except(NameError):
                print("This subset, year, or key was not found, please try valid inputs for the Economic Indicators survey.")
    elif betweentime==True:
        r2=requests.get(f'https://api.census.gov/data/timeseries/eits/{subset}?get=cell_value,data_type_code,time_slot_id,category_code,seasonally_adj&time=from+{year1}-{m1}+to+{year2}-{m2}')
        if r2.status_code==200:
            try:
                df= pd.DataFrame
                return df
            except(NameError):
                print("This subset, year, or key was not found, please try valid inputs for the Economic Indicators survey.")

  
def health(year, state='*', county='*'):
    """ Gets percentages of people insured and not insured in county, state, and year specified. If county and state are not specified, will get
    nationwide data for all states and counties. May have to make search parameters smaller.
    Parameters
    ----------
    year:
        Only full 4-integer values for years where the Community Survey is available, 2009-2019
    state:
        string argument for state code.
    county:
        string argument for county code.


    Returns
    -------
    Pandas dataframe extracted with information about state and county insured versus uninsured populations, and a quickdescription of the dataframe
    

    Examples
    --------
    >>> from us_census import us_census
    >>> health(2018, '02')"""
    r= requests.get(f'http://api.census.gov/data/timeseries/healthins/sahie?get=NIC_PT,NUI_PT&for=county:{county}&in=state:{state}&time={year}')
    if r.status_code==200: 
            try:
                df= pd.DataFrame(r.json())
                return df
                return df.describe()
            except(NameError):
                print("This subset, year, or key was not found, please try valid inputs for the Economic Indicators survey.")
    
