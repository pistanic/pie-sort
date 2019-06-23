import numpy as np
import pandas as pd


#Defines Search box area
def define_search_box(VerticalLocation, HorinzontalLocation, Width,Height):
    SearchWidth = 50 #searches this width on either side
    SearchHeight = 50#searches this height on either side


    #Checks to ensure box isnt out of bounds, sets box location to
    if((VerticalLocation-SearchHeight)<0):
        SearchBox_Vertical_Location = 0
    else:
        SearchBox_Vertical_Location = VerticalLocation - SearchHeight

    if ((HorinzontalLocation - SearchWidth) < 0):
        SearchBox_Horizontal_Location = 0
    else:
        SearchBox_Horizontal_Location = VerticalLocation - SearchWidth

    #Sets search to extend either side of origial box by X pixels
    SearchBox_Width = Width + SearchWidth*2
    SearchBox_Height = Height +SearchHeight*2

    SearchBox = np.array([SearchBox_Vertical_Location,SearchBox_Horizontal_Location, SearchBox_Width,SearchBox_Height])

    return SearchBox

#Returns New Dataframe with
def return_inside_search_box(Searchbox,df):
    SearchResults = df.copy(deep=True)


    leftBound=Searchbox[0]
    rightBound=Searchbox[0]+Searchbox[2]
    upBound=Searchbox[1]
    bottomBound=Searchbox[1]+Searchbox[3]

    #Finds datapoints that have location origin within SearchBox
    SearchResults = SearchResults.loc[SearchResults['left'] > leftBound]
    SearchResults = SearchResults.loc[SearchResults['left'] < rightBound]
    SearchResults = SearchResults.loc[SearchResults['top'] > upBound]
    SearchResults = SearchResults.loc[SearchResults['top'] < bottomBound]

    return SearchResults


#Finds values inside dataframe and returns dataframe
def find_in_df(df,column,value):
    SimpleDataframe = df.copy(deep=True)

    SimpleDataframe = df.loc[df[column] == value]

    return SimpleDataframe

def get_dob_from_phn(df,phn:
    # This function should return the DOB as a string that can be searched
    # in the ocr output.
    # INPUT: df = test database
    #        phn = personal helth number
    return 'void'


def get_name_from_phn(df,name):
    # This function should return the DOB as a string that can be searched
    # in the ocr output.
    # INPUT: df = test database
    #        name = 'First_name Last_Name' this could be list or string. Pick one
    #               that is easyer to impl.

    return 'void'


#Boolean function that determines if Searchvalue is in dataframe
def is_in_df(df,column,Searchvalue):

    if(Searchvalue in df[column]):
        return True

    else:
        return False

#Initialized patient dataframe for patients in given database
def init_test_db():
    # First Name/Middle Name/Middle Name/Last Name/PHN/DOB-YYYY/DOB-MM/DOB-DD/FILE PATH
    # Patients in test images
    patient1 = ['Cowan', 'A', 'Wood', '1742791', '1967', '06', '13','Editted Holter 2.pdf']
    patient2 = ['Sidney', 'Nan', 'Ambrose', '7453474', '1951', '11', '14','Editted Referral 3.pdf']
    patient3 = ['Andrea', 'Nan', 'Smailys', '09392030', 'Nan', 'Nan', 'Nan','Editted - CT Chest.pdf']
    patient4 = ['Amelia', 'Nan', 'Gary', '9120707959', '1959', '12', '12', 'Editted Referral 4.pdf']
    patient5 = ['Matthew', 'Nan', 'Penard', '9059309239', '1925', '06', '19', 'Editted Referral 2.pdf']
    patient6 = ['Bobbie', 'Blake', 'Hothe', '9896898914', '1943', '07', '04', 'Editted Referral 1.pdf']
    patient7 = ['Rob', 'Nan', 'Toll', '120157576', '1933', '07', '03', 'Editted MUGA 1.pdf']
    patient8 = ['Laura', 'Nan', 'Smith', '93379933', 'Nan', 'Nan', 'Nan', 'Editted MIBI 1.pdf']
    patient9 = ['Glen', 'Nan', 'Christopher', '9795127959', '1959', '12', '31', 'Editted Holter 1.pdf']
    patient10 = ['Grace', 'Nan', 'Wood', '9895806209', '1939', '06', '19', 'Editted ECHO 2.pdf']
    patient11 = ['Blake', 'Nan', 'Todd', '9831829694', '1969', '09', '04', 'Editted ECHO 1.pdf']
    patient12 = ['Rob', 'Nan', 'Todd', '9896819634', '1963', '02', '01', 'Editted ECG 3.pdf'] # DOB unclear, name unclear
    patient13 = ['Joe', 'Nan', 'House', '9020179357', '1942', '05', '04', 'Editted ECG 2.pdf']# DOB unclear, name unclear
    patient14 = ['Karen', 'Nan', 'Johnston', '002253474', '1932', '11', '09', 'Editted ECG 1.pdf']

    # Test patients
    patient15 = ['Terry', 'Perry', 'Jerry', '111111111', '1999', '03', '02','Not Assigned']
    patient16 = ['Terry', 'Gary', 'Lary', '222222222', '1999', '04', '02','Not Assigned']
    patient17 = ['Ferry', 'Dairy', 'Kerry', '3333333333', '1999', '05', '02','Not Assigned']
    df = pd.DataFrame(np.array([patient1, patient2, patient3, patient4, patient5, patient6,patient7,patient8,patient9,patient10,patient11,patient12,patient13,patient14,patient15,patient16,patient17]),columns=['First_Name', 'Middle_Name', 'Last_Name', 'PHN', 'DOB-YYY', 'DOB-MM', 'DOB-DD','Filepath'])

    return df
