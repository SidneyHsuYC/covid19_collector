from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger, EarlyStopping, TensorBoard, ReduceLROnPlateau
from tensorflow.keras.layers import Dense, Input, Dropout
from tensorflow.keras.models import load_model

import efficientnet.tfkeras as ef

import os
import glob
import h5py
import pandas as pd
import numpy as np
import json
import pydicom
import SimpleITK as sitk

from pathlib import Path
from tqdm import tqdm
from skimage.transform import resize

root_dir = Path.cwd()
covid19_path = root_dir / 'bimcv_covid19_posi_head_iter1'
output_dir = root_dir

# Set Ture to generate generate dataset hdf5 and csv file
generate_h5_and_pandas = True

# Model to identify position
pa_ll_model_file = root_dir / 'Frontal_Lateral_Model.h5'

# # Paths to the dataset
covid19_labels_nlp = covid19_path / 'derivatives' / 'labels' / 'labels_covid19_posi.tsv'
# tests_file = os.path.join(covid19_path, 'derivatives/EHR/sil_reg_covid.tsv')

# Output files - several csvs and a h5 with the image data
covid19_pandas = output_dir / f"bimcv_metadata.csv"
covid19_h5 = output_dir / f"bimcv_metadata.hdf5"

# png_paths = glob.glob(str(root_dir / "/*/*/*/*/*.png"))
png_paths = glob.glob(str(root_dir) + "/bimcv_covid19_posi_subjects_*/**/*.png", recursive=True)

# Model Frontal_Lateral_Model.h5 can be downloaded from:
# https://www.dropbox.com/s/nn1me22ie5iye1e/Frontal_Lateral_Model.h5?dl=0
if not os.path.exists(pa_ll_model_file):
    print(f"No Frontal_Lateral_Model.h5 found.")
    exit(1)
else:
    model = load_model(pa_ll_model_file)

############################
##### Generate dataset #####
############################
# Read in labels
df_label = pd.read_csv(covid19_labels_nlp, sep='\t')
# indexing for pandas
header = list(df_label.columns)
labels_index = header.index('Labels')
labels_local_index = header.index('LabelsLocalizationsBySentence')

# List formater to format tab string in json file
lst_formator = lambda label_str: label_str[1:-1].replace("'", '').strip().replace('\t \t ', '\t').replace('\t', ',')
def get_labels(subject, session):
    select = df_label[(df_label['PatientID'] == subject) & (df_label['ReportID'] == session)]
    if len(select):
        label = lst_formator(select.iloc[0, labels_index])
        label_local = lst_formator(select.iloc[0, labels_local_index])
        return label, label_local
    else:
        return None, None

def json_to_dict(path_str):
    dti = dict()

    # Find modality from last two chars from name, eg. cr
    path = Path(path_str)
    modality = path.stem.split("_")[-1]
    path_parts = path.parts
    dti['Subject'] = path_parts[-4]
    dti['Session'] = path_parts[-3]
    dti['mod'] = path_parts[-2]
    dti['File'] = path_parts[-1]
    dti['Type'] = modality
    dti['Path'] = path
    dti['Labels'], dti['LabelsLocalizationsBySentence'] = get_labels(path_parts[-4], path_parts[-3])
    
    json_file = path_str.replace('.png', '.json').replace('.nii.gz', '.json')
    # If there is no json associated with the file, then pick the json on the series. 
    # Maybe multiple acquisitions with the same parameters in the same series?
    if not os.path.exists(json_file):
        json_in_series = glob.glob(str(path.parent / '*.json'))
        if len(json_in_series) >= 1:
            json_file = json_in_series[0]

    if os.path.exists(json_file):
        with open(json_file) as f:
            dtij = json.load(f)
        # Only transform DICOM code to string if "value" is within the keys
        for l in dtij.keys():
            if 'Value' in dtij[l].keys():
                try:
                    dti[pydicom.datadict.dictionary_description(str(l))] = dtij[l]['Value'][0].strip("'") if (len(dtij[l]['Value']) == 1) else dtij[l]['Value']
                except:
                    pass

    return dti

if generate_h5_and_pandas:
    # Dictionary used to convert to panda and convert to csv file
    dtl = []
    '''
    if os.path.exists(covid19_h5):
        print(f"{covid19_h5} already exists.")
        delete = input(f"Do you want to overwrite {covid19_h5}? (Y/N)")
        if delete.strip() in ['Y', 'y']:
            os.remove(covid19_h5)
            print(f"Removed {covid19_h5}")
        elif delete.strip() in ['N', 'n']:
            print(f"No overwrite perform")
            exit(0)
        else:
            print(f"Response not correct")
            exit(1)
    '''
    # Initiate h5 file
    fh5 = h5py.File(covid19_h5, 'w')
    fh5.create_dataset("images", (len(png_paths), 299, 299), chunks=(1, 299, 299), dtype=np.uint16)
    
    # indexing for fh5 file
    count = 0
    print(f"Detected total {len(png_paths)} png files under {root_dir}")
    print("Parsing the jsons of the chest images and creating the h5 - this takes a while ...")
    for png in tqdm(png_paths):
        # transfrom json file to dictionary
        dti = json_to_dict(png)

        # Skip if Modelity does not contain in dicom metadata
        if not dti.get('Modality'):
            continue

        if dti['Modality'] == 'DX' or dti['Modality'] == 'CR':
            # Use SITK library to read image
            sitk_img = sitk.ReadImage(png)
            img = sitk.GetArrayFromImage(sitk_img)
            if dti['Photometric Interpretation'] == "MONOCHROME1":
                img = -img
                
            # imgl is short side 
            imgl = min(img.shape[0], img.shape[1])
            # divide imgl by 2 and floor that value
            imgl = int((imgl - imgl%2)/2)
            # Not sure...
            imgc = img[ int(img.shape[0]/2 - imgl):int(img.shape[0]/2 + imgl),
                        int(img.shape[1]/2 - imgl):int(img.shape[1]/2 + imgl)]
            
            # Normalize image 
            imgc = 1.0*(imgc - np.min(np.ravel(imgc))) / (np.max(np.ravel(imgc)) - np.min(np.ravel(imgc)) )
            imgr = resize(imgc, (299,299), anti_aliasing=True, preserve_range=True)
            
            # if image is 3-dimensions np-array, select the first layer
            if len(imgr.shape) != 2:
                imgr = imgr[:,:,0]

            fh5["images"][count,:,:] = (( (imgr[:,:] - np.min(np.ravel(imgr))) / (np.max(np.ravel(imgr)) - np.min(np.ravel(imgr)) ))*(2**16-1)).astype(np.uint16)
            
            # Predict Posistion on three dimension image
            imgp = np.zeros((1,299,299,3))
            for k in range(0,3):
                imgp[0,:,:,k] = imgr
            score = model.predict(imgp)[0][0]
            dti['Position_DL_Score'] = score
            if score > 0.5:
                dti['Position_DL'] = 'PA'
            else:
                dti['Position_DL'] = 'L'

            dti['h5_idx'] = count
            count += 1

            # Append h5 indexing to csv
            dtl.append(dti) 
            

    print(f"Processed {count} number of records.")
    fh5.close()
    
    # # Converted pandas to csv file
    dt = pd.DataFrame.from_dict(dtl)    
    dt.to_csv(covid19_pandas, index=False)
    print(f"Created {covid19_pandas}.") 