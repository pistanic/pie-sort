import preproc # for source see: preproc/
import ocr # for source see: ocr/
import nlp # for source see: nlp/
import ezRead
import docMan # four source see: docMan/
import searchHelp
import validate
import roi
import pandas as pd
from os import makedirs

def printf(name, value):
    print('+------------------------------------------------------------+')
    print('  Main Debug - '+name+':')
    print(' '+str(value))
    print('+------------------------------------------------------------+')

def main():
    LOCAL_DIR = './'
    PDF_DIR = LOCAL_DIR+'PDF/'
    TMP_DIR = LOCAL_DIR+'tmp/'
    SORT_DIR = LOCAL_DIR+'pd/'
    IMG_DIR = TMP_DIR+'img/'
    TXT_DIR = TMP_DIR+'txt/'

    docMan.init_folders([PDF_DIR, TMP_DIR, SORT_DIR, IMG_DIR, TXT_DIR])

    # #test db
    # patient_database = searchHelp.init_test_db()

    # real db
    try:
        patient_database = pd.read_csv('./pie_patient_db.csv', dtype=str)
        patient_database = patient_database.applymap(str)  # converts data to string format

    except FileNotFoundError:
        print('*************** CVS DB NOT FOUND ***************')
        patient_database = docMan.init_validation_df("../pdb.xlsx")

    file_list = docMan.get_file_list(PDF_DIR)

    #try:
    # Counter to terminate program after a set number of iterations
    max_num_docs = 200
    cur_num_docs = 0
    # Validation Stats
    num_val_docs = 0
    failed_docs = []
    validated_docs = []
    # Main processing loop
    for file_ in file_list:
        # Print processing file
        printf('file_ in file_list', file_)
        image_name = docMan.pdf2jpg((PDF_DIR+file_), IMG_DIR) # store image in IMG_DIR
        # Print processing Image name
        print('image_name', image_name)
        img_path = IMG_DIR+image_name
	
        # Make image specific paths
        DIL_DIR = img_path+'/dilation'
        CON_DIR = img_path+'/contour'
        CRP_DIR = img_path+'/crop'
        CRP_TXT_DIR = CRP_DIR+'/txt'
        docMan.init_folders([DIL_DIR, CON_DIR, CRP_DIR, CRP_TXT_DIR])

        # Apply first layer of preprocessing.
        # Resize will increase the size of the immage and apply a mild blur
        # to average pixle values after they have been stretched.
        #img_path = preproc.resize(img_path)

        # OCR Stage
        printf('txt_dir + img_name',TXT_DIR+image_name)

        try:
            makedirs(TXT_DIR+image_name.replace('.jpg',''))
        except:
           print('Text Directory already exists')

        printf('TXT_DIR+image_name.replace(.jpg)',TXT_DIR+image_name.replace('.jpg',''))


        txt_path = TXT_DIR+image_name.replace('.jpg','')

        # Ocr Processing stage Create a text file from the image and use that
        # text file to produce the ocr data frame. Also create ocr string directly
        # from the image. Both are returned as ocr_list.
        # ocr_list = [ocr_df, ocr_str]
        ocr_list = ocr.processing(img_path, txt_path)

        # NLP Stage
        # Extract the identifying infromation from contents of ocr_list
        # id_list = [PHNs, names, DOBs]
        id_list = nlp.processing(ocr_list)

        #Validate stage
        print('*************** ENTERING VALIDATION ***************')
        printf('Stage Of validation','Preproc = resize')
        if (validate.validate(ocr_list, id_list, patient_database)):
            validated_docs.append(file_,)
            num_val_docs = 1 + num_val_docs
            #dist_path = SORT_DIR+valid_phn+'/'+file_
            source_path = PDF_DIR+file_
            print('*************** VALIDATION STAT ***************')
            print("Docments validated up to this point: "+str(num_val_docs)+'/'+str(cur_num_docs))
            #docMan.sort(source_path, dist_path)
            #docMan.sort(source_path, "./val/"+file_)
            ## DEBUG OPERATION! #
            ## Move files back to PDF folder to aviod reverting manually.
            #docMan.un_sort(dist_path, source_path)
            # ---------------- #
        else:
            printf('Stage Of validation','Preproc = roi')
            # Use roi to generate cropped images    
            file_pages = docMan.get_file_list(img_path)
            for page in file_pages:
                roi.roi_main(img_path+'/'+page, img_path)
			    
            #file_crops = docMan.get_file_list(CRP_DIR)
            #for crop in file_crops:
            ocr_list = ocr.processing(CRP_DIR, CRP_TXT_DIR)
            id_list = nlp.processing(ocr_list)
            if (validate.validate(ocr_list, id_list, patient_database)):
                validated_docs.append(file_,)
                num_val_docs = 1 + num_val_docs
                print('*************** VALIDATION STAT ***************')
                print("Docments validated up to this point: "+str(num_val_docs)+'/'+str(cur_num_docs))
            
            #docMan.sort(source_path, "./not_val/"+file_)
            #preproc.filtering(img_path)
            #ocr_list = ocr.processing(img_path, txt_path)
            #id_list = nlp.processing(ocr_list)
            #if (validate.validate(ocr_list, id_list, patient_database)):
            #    validated_docs.append(file_,)
            #    num_val_docs = 1 + num_val_docs
            else:
               failed_docs.append(file_)

        cur_num_docs = cur_num_docs + 1;
        if (cur_num_docs == max_num_docs):
            print("Number of Documents Processed: "+str(cur_num_docs))
            break

    printf('Number of Validated Documents out of '+str(len(file_list)),num_val_docs)
    printf('Accuracy', (len(validated_docs)/(len(validated_docs)+len(failed_docs))))
    printf('Validated Documents',validated_docs)
    printf('Failing Documents',failed_docs)

    #except Exception as e:
    #    print(e)
    #    source_path = PDF_DIR+file_
    #    docMan.sort(source_path, "./except/"+file_)

if __name__ == '__main__':
    main()
