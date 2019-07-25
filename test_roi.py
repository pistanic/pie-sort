import docMan
import roi

LOCAL_DIR = './'
PDF_DIR = LOCAL_DIR+'PDF/'
TMP_DIR = LOCAL_DIR+'tmp/'
SORT_DIR = LOCAL_DIR+'pd/'
IMG_DIR = TMP_DIR+'img/'
TXT_DIR = TMP_DIR+'txt/'
DIL_DIR = IMG_DIR+'dilation'
CON_DIR = IMG_DIR+'contour'
CRP_DIR = IMG_DIR+'crop'

docMan.init_folders([PDF_DIR, TMP_DIR, SORT_DIR, IMG_DIR, TXT_DIR, DIL_DIR, CON_DIR, CRP_DIR])

file_list = docMan.get_file_list(PDF_DIR)

for file_ in file_list:
	image_name = docMan.pdf2jpg((PDF_DIR+file_), IMG_DIR) # store image in IMG_DIR
	img_path = IMG_DIR+image_name
	jpg_list = docMan.get_file_list(img_path)
	
	for jpg in jpg_list:
		print(img_path+jpg)
		roi.roi_main(img_path+'/'+jpg, img_path)
