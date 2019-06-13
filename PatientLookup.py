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
        self.FilePath = 'Nan'


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

    def assign_FilePath(FP):
        self.FilePath = FP

    def returnInfo(self):
        array = [self.FirstName,self.MiddleName,self.LastName,self.PHN,self.DOB_YYYY,self.DOB_MM, self.DOB_DD]
        return array


#Input Column to search and value to find
def findInDataframe(df,column,value):
    SimpleDataframe = df.copy(deep=True)

    SimpleDataframe = df.loc[df[column] == value]

    return SimpleDataframe


def init_TestPatientsDataFrame()
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