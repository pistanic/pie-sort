import ocr

testimage = '/home/pie/Desktop/hardtest.jpg'

data = ocr.extract_text(testimage)

#data = data.split()

print(data)
