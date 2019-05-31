import ocr
import csv
import pandas as pd

testimage = '/home/pie/Desktop/hardtest.jpg'

data = ocr.extract_text(testimage)


#data = data.split()

print(data)

file = open('ocr_data.txt','w')
file.write(data)
file.close

df = pd.read_csv('ocr_data.txt', sep='\t')
df.to_excel('ocr_data.xlsx')
print(df.describe())

