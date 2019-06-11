import pandas as pd
import numpy as np

class patient(object):
    def __init__(self):
        self.FirstName = 'Nan'
        self.MiddleName = 'Nan'
        self.LastName = 'Nan'
        self.PHN = 'Nan'
        self.DOB_YYYY = 'Nan'
        self.DOB_MM = 'Nan'
        self.DOB_DD = 'Nan'

    def assign_First_Name(First):
        self.FirstName = First

    def assign_Middle_Name(Middle):
        self.MiddleName = Middle

    def assign_Last_Name(Last):
        self.LastName = Last

    def assign_PHN(PHN):
        self.PHN = PHN

    def assign_DOB_YYYY(YYYY):
        self.DOB_YYYY = YYYY

    def assign_DOB_MM(MM):
        self.DOB_MM = MM

    def assign_DOB_DD(DD):
        self.DOB_DD = DD

    def returnInfo(self):
        array = [self.FirstName,self.MiddleName,self.LastName,self.PHN,self.DOB_YYYY,self.DOB_MM, self.DOB_DD]
        return array

#Input Column to search and value to find
def findInDataframe(df,column,value):
    SimpleDataframe = df.copy(deep=True)

    SimpleDataframe = df.loc[df[column] == value]

    return SimpleDataframe


def init_TestPatientsDataFrame()
    # First Name/Middle Name/Middle Name/Last Name/PHN/DOB-YYYY/DOB-MM/DOB-DD
    # Patients in test images
    patient1 = ['Cowan', 'A', 'Wood', '1742791', '1967', '06', '13']
    patient2 = ['Sidney', 'Nan', 'Ambrose', '7453474', '1951', '11', '14']
    patient3 = ['Andrea', 'Nan', 'Smailys', '09392030', 'Nan', 'Nan', 'Nan']
    # Test patients
    patient4 = ['Terry', 'Perry', 'Jerry', '111111111', '1999', '03', '02']
    patient5 = ['Terry', 'Gary', 'Lary', '222222222', '1999', '04', '02']
    patient6 = ['Ferry', 'Dairy', 'Kerry', '3333333333', '1999', '05', '02']
    df = pd.DataFrame(np.array([patient1, patient2, patient3, patient4, patient5, patient6]),columns=['First_Name', 'Middle_Name', 'Last_Name', 'PHN', 'DOB-YYY', 'DOB-MM', 'DOB-DD'])

    return df