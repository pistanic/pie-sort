#################################################################
#                                                               #
# Copyright 2019 All rights reserved.                           #
# Author: Jake Mawdsley                                         #
# Co-Authors: Nicholas Forest                                   #
#                                                               #
#################################################################

import numpy as np
import pandas as pd


# INPUT: HorizontalLocation - Horizontal Center of Search Box (Pixels)
#        VerticalLocation - Vertical Center of Search Box (Pixels)
#        Width - Total width of search box (ie: for 30 pixels it will search 30 pixels left and 30 pixels right of the center)
#        Height -Total Height of search box (ie: for 30 pixels it will search 30 pixels up and 30 pixels down of the center)
# OUTPUT: SearchBox - outputs searchbox array
# DESCRIPTION: Function defines searchbox to be used in "return_inside_search_box" function.
def define_search_box(HorinzontalLocation,VerticalLocation, Width,Height):
    # sets location to follow dataframe notation. top/left as location info
    SearchBox_Left_Location = HorinzontalLocation-Width# left bound of search box
    SearchBox_Top_Location = VerticalLocation-Height# upper bound of search box

    #Sets search to extend either side of center by X pixels
    SearchBox_Width = 2*Width
    SearchBox_Height = 2*Height

    SearchBox = np.array([SearchBox_Left_Location,SearchBox_Top_Location, SearchBox_Width,SearchBox_Height])

    return SearchBox

# INPUT: Searchbox - Numpy Array of [SearchBox_Left_Location,SearchBox_Top_Location, SearchBox_Width,SearchBox_Height]
#        df -  OCR dataframe output
# OUTPUT: SearchResults - New Dataframe of contents within search box
# DESCRIPTION: Takes in Search box which defines the top left corner of the search box and the width and height.
#              Then finds contents within the search box and returns news Dataframe with contents.
#              Note: function defines "Within search box" as the center of the text box.
def return_inside_search_box(Searchbox,df):
    SearchResults = df.copy(deep=True)

    leftBound=Searchbox[0]
    rightBound=Searchbox[0]+Searchbox[2]
    upBound=Searchbox[1]
    bottomBound=Searchbox[1]+Searchbox[3]

    #Finds datapoints that have location center within SearchBox
    SearchResults = SearchResults.loc[(SearchResults['left']+SearchResults['width']/2) > leftBound]
    SearchResults = SearchResults.loc[(SearchResults['left']+SearchResults['width']/2) < rightBound]
    SearchResults = SearchResults.loc[(SearchResults['top']+SearchResults['height']/2) > upBound]
    SearchResults = SearchResults.loc[(SearchResults['top']+SearchResults['height']/2) < bottomBound]

    return SearchResults

# INPUT: PHN - PHN that will be searched
#        df - OCR dataframe output
#        search_width - search box width (pixels)
#        search_height - search box height (pixels)
# OUTPUT: Outputs OCR dataframe
# DESCRIPTION: Finds values in searchbox centered around inputted PHN
def PHN_Document_Box_Search(PHN,df,search_width,search_height):
    #copy dataframe
    search_df = df.copy(deep=True)

    #Create PHN search dataframe (contains info related to search, location, width, height)
    PHN_df = find_in_df(search_df,'text',PHN)
    PHN_df = PHN_df.reset_index(drop=True)

    #define empty result dataframe
    complete_search_result_df = pd.DataFrame().reindex_like(df)

    for index, row in PHN_df.iterrows():
        #Define center of word box
        PHN_Horizontal_center = PHN_df.at[index,'left'] + (PHN_df.at[index,'width'])/2
        PHN_Vertical_center = PHN_df.at[index,'top'] + (PHN_df.at[index,'height'])/2

        #define searchbox and return search results
        searchbox = define_search_box(PHN_Horizontal_center,PHN_Vertical_center,search_width,search_height)
        search_result_df = return_inside_search_box(searchbox,search_df)

        #Merge new results into complete dataframe, drop duplicate rows
        complete_search_result_df = pd.concat([search_result_df,complete_search_result_df])
        complete_search_result_df = complete_search_result_df.drop_duplicates()

    #delete rows with all Nan values
    complete_search_result_df = complete_search_result_df.dropna(how='all')

    return complete_search_result_df

## AOI Masking Demo
#PHN_AOI_demo = 'Sidney'
#aoi_df = searchHelp.PHN_Document_Box_Search(PHN_AOI_demo,ocr_df,500,500)
#printf('Area of Interest Dataframe', aoi_df)


# INPUT: df - Datafame to searh
#        column - column to search
#        value - value to look up
# OUTPUT: dataframe of found values
#Finds values inside dataframe and returns dataframe
def find_in_df(df,column,value):
    SimpleDataframe = df.copy(deep=True)

    SimpleDataframe = df.loc[df[column] == value]

    return SimpleDataframe

# INPUT: df - database to search
#        phn - personal health number to look up
# OUTPUT: DOB string.
def get_dob_from_phn(db,phn):
    # INPUT: df = test database
    #        phn = personal helth number
    patient_df = find_in_df(db, 'PHN', phn)
    year = patient_df['DOB-YYYY'].values[0]
    month = patient_df['DOB-MM'].values[0]
    day = patient_df['DOB-DD'].values[0]
    return year + '-' + month + '-' + day

# INPUT: df - database to search
#        phn - personal health number to look up
# OUTPUT: first and last name string.
def get_name_from_phn(db, phn):
    # INPUT: df = test database
    #        name = 'First_name Last_Name' this could be list or string. Pick one
    #               that is easyer to impl.
    patient_df = find_in_df(db,'PHN',phn)
    first_name = patient_df['First_Name'].values[0]
    last_name = patient_df['Last_Name'].values[0]
    return first_name + ' ' +last_name

# INPUT: df - Dataframe to search
#        column - Dataframe column descriptor
#        searchValue - value to loacate in dataframe.
# OUTPUT: True if value is in dataframe
#Boolean function that determines if Searchvalue is in dataframe
def is_in_df(df, column, searchValue):
    result_df = find_in_df(df, column, searchValue)
    if(result_df.empty):
        return False
    else:
        return True

# OUTPUT: Validation database
# DESCRIPTION: Create the database used for validation of test files.
#Initialized patient dataframe for patients in given database
def init_test_db():
    # First Name/Middle Name/Middle Name/Last Name/PHN/DOB-YYYY/DOB-MM/DOB-DD/FILE PATH
    # Patients in test images
    patient_list = [
    ['Cowan', 'A', 'Wood', '1742791', '1967', '06', '13','Editted Holter 2.pdf'],
    ['Sidney', 'Nan', 'Ambrose', '7453474', '1951', '11', '14','Editted Referral 3.pdf'],
    ['Andrea', 'Nan', 'Smailys', '09392030', 'Nan', 'Nan', 'Nan','Editted - CT Chest.pdf'],
    ['Amelia', 'Nan', 'Gary', '9120707959', '1959', '12', '12', 'Editted Referral 4.pdf'],
    ['Matthew', 'Nan', 'Penard', '9059309239', '1925', '06', '19', 'Editted Referral 2.pdf'],
    ['Bobbie', 'Blake', 'Hothe', '9896898914', '1943', '07', '04', 'Editted Referral 1.pdf'],
    ['Rob', 'Nan', 'Toll', '120157576', '1933', '07', '03', 'Editted MUGA 1.pdf'],
    ['Laura', 'Nan', 'Smith', '93379933', 'Nan', 'Nan', 'Nan', 'Editted MIBI 1.pdf'],
    ['Glen', 'Nan', 'Christopher', '9795127959', '1959', '12', '31', 'Editted Holter 1.pdf'],
    ['Grace', 'Nan', 'Wood', '9895806209', '1939', '06', '19', 'Editted ECHO 2.pdf'],
    ['Blake', 'Nan', 'Todd', '9831829694', '1969', '09', '04', 'Editted ECHO 1.pdf'],
    ['Rob', 'Nan', 'Todd', '9896819634', '1963', '02', '01', 'Editted ECG 3.pdf'], # DOB unclear, name unclear
    ['Joe', 'Nan', 'House', '9020179357', '1942', '05', '04', 'Editted ECG 2.pdf'], # DOB unclear, name unclear
    ['Karen', 'Nan', 'Johnston', '002253474', '1932', '11', '09', 'Editted ECG 1.pdf'],
    ['Terry', 'Perry', 'Jerry', '111111111', '1999', '03', '02','Not Assigned'],
    ['Terry', 'Gary', 'Lary', '222222222', '1999', '04', '02','Not Assigned'],
    ['Ferry', 'Dairy', 'Kerry', '3333333333', '1999', '05', '02','Not Assigned'],
    ['VALERIE', 'NAN', 'HOLM','901928236','1956','09','22','NA']
    ] # END OF PATIENT_LIST
    df = pd.DataFrame(np.array(patient_list),columns=['First_Name', 'Middle_Name', 'Last_Name', 'PHN', 'DOB-YYYY', 'DOB-MM', 'DOB-DD','Filepath'])

    return df
