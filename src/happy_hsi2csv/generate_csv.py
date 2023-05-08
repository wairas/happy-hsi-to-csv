import os
import json
import numpy as np
import pandas as pd
from datetime import datetime
from pixel_selectors.column_wise_pixel_selector import ColumnWisePixelSelector
from pixel_selectors.averaged_grid_pixel_selector import AveragedGridSelector
import argparse

from criteria import Criteria, CriteriaGroup
from readers.mat_reader import MatReader

parser = argparse.ArgumentParser(description='Generate datasets as numpy cubes, to be loaded into deep learning datasets.')
#parser.add_argument('input_file', type=str, help='Path to input file (list of ids) in JSON format')
parser.add_argument('output_folder', type=str, help='Path to output folder')
args = parser.parse_args()

experiment_dict={}
experiment_dict["per_image"]={}
experiment_dict["per_image"]["meta_data"]=["sample_id","r_x","x0","x1","y0","y1"]  #x0,x1,y0,y0 -> if cropped from original image
#experiment_dict["per_image"]["targets"]=["bnf","nitrogen"]
experiment_dict["per_pixel"]={}
experiment_dict["per_pixel"]["meta_data"]=["sample_id","r_x","x","y","type","object"]
experiment_dict["per_pixel"]["targets"]=["THCA"]    

def load_sampleids(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def load_global_jsons(ids_filename, output_path, spectra_reader, pixel_selectors=[]):

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    meta_data_keys = experiment_dict["per_pixel"]["meta_data"]
    target_keys = experiment_dict["per_pixel"]["targets"]

    output_dict = {}
    ids = load_sampleids(ids_filename)
    for pixel_selector in pixel_selectors:
        # Create the filename for the CSV and JSON files
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        columns_created = False
        output_df = pd.DataFrame()
        for id in ids:
        #if filename.endswith("_global.json"):
            # Load the global json
            #print(filename)
            #id = filename[:-len("_global.json")]
            print(id)
            spectra_reader.load_data(id)

            selectedp = pixel_selector.select_pixels()
            
            wn = spectra_reader.get_wavelengths()
            for ind, (x, y, z_data) in enumerate(selectedp):
                # If pixel type is valid and z data is not zero, add row to output dataframe
                if not np.all(z_data == 0):
                    if not columns_created:
                        column_names = meta_data_keys + [f"z_{wn[i]}" for i in range(len(z_data))] + target_keys
                        output_df = pd.DataFrame(columns=column_names)
                        columns_created = True
                    # Create a dictionary of values for the row
                    row_values = {
                        key: spectra_reader.json_reader.get_meta_data(x=x, y=y, key=key)
                        for key in meta_data_keys
                    }
                    row_values.update({f"z_{wn[i]}": v for i, v in enumerate(z_data)})
                    row_values.update({
                        key: spectra_reader.json_reader.get_meta_data(x=x, y=y, key=key)
                        for key in target_keys
                    })

                    # Add the row to the output dataframe
                    output_df = output_df.append(row_values, ignore_index=True)

        # Write the multi-target output CSV file
        n = pixel_selector.get_n()
        target="multi_target"
        filename = f"{pixel_selector.__class__.__name__}_{n}_{timestamp}.csv"
        output_dir = os.path.join(output_path, target)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_file = os.path.join(output_dir, filename)
        if target not in output_dict:
            output_dict[target] = {}
        output_dict[target][filename] = pixel_selector.to_dict()
        output_df.to_csv(output_file, index=False, columns=column_names)
        #output_file = os.path.join(output_path, filename)
        #output_dict[filename] = pixel_selector.to_dict()
        #output_df.to_csv(output_file, index=False, columns=column_names)
        
        for target in target_keys:
            # make columns
            column_names = meta_data_keys + [f"z_{wn[i]}" for i in range(len(z_data))] + [target]
            # output dir/file
            output_dir = os.path.join(output_path, target)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            output_file = os.path.join(output_dir, filename)
            if target not in output_dict:
                output_dict[target] = {}
            output_dict[target][filename] = pixel_selector.to_dict()
            output_df.to_csv(output_file, index=False, columns=column_names)
            # Add the pixel selector dictionary to the output dictionary
        

    # Write the output JSON file
    output_json = os.path.join(output_path, "output_csvs.json")
    with open(output_json, "w") as f:
        json.dump(output_dict, f, indent=2)

def simple_filename_func(base_dir, sample_id):
    base_id, sub_dir, _ = sample_id.split("__")
    return os.path.join(base_dir, sub_dir, "normcubes",f"{base_id}.mat")

# Initialize the spectra reader object for reading .mat files
mat_reader = MatReader("/home/fracpete/temp/happy-dale/for_peter/data", "/home/fracpete/temp/happy-dale/for_peter/jsons", simple_filename_func, "normcube",wavelengths_struct="lambda")

crit1 = Criteria("in", key="type", value=[2,3], spectra_reader=mat_reader)

##crit = crit1 = Criteria("in", key="type", value=pixel_type_filter, spectra_reader=spectra_reader)
#crit2 = Criteria("matches", key="r_x", value="X", spectra_reader=mat_reader)
#crit = CriteriaGroup(criteria_list=[crit1,crit2])
crit=crit1
pixel_selectors = [AveragedGridSelector(mat_reader, 32, crit, 4),AveragedGridSelector(mat_reader, 4, crit, 4), AveragedGridSelector(mat_reader, 4, crit, 2), ColumnWisePixelSelector(mat_reader, 32, crit, 4)]

if not os.path.exists(args.output_folder):
    os.makedirs(args.output_folder)
    print(f"Folder '{args.output_folder}' created successfully!")
else:
    print(f"Folder '{args.output_folder}' already exists.")   
    
# Call loop_jsons() function with the reader object
load_global_jsons("/home/fracpete/temp/happy-dale/for_peter/jsons/alldata.json", output_path=args.output_folder, spectra_reader=mat_reader, pixel_selectors=pixel_selectors)

#command line
#python generate_csv_cl.py ..\new_output\csvs\csvout_1
