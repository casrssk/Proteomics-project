#authors: Tom Altenburgh and Satwant Kaur
# This helps to compile the results from deepNovo and groud truth data together in one csv file.
from pyteomics import mgf
import pandas as pd
import numpy as np

import os

def prep_input(input_filepath,brackets=False):
    
    scan_seq = {}
    scan_mass = {}
    scan_charge = {}
    read = mgf.read(input_filepath)
    
    while True:
        try:
            elem = read.next()
            scan = elem['params']['scans']
            seq = elem['params']['seq']
            mass = elem['params']['pepmass'][0]
            charge = elem['params']['charge'][0]
            if brackets:
                seq = seq.replace('(+15.99)','mod')
                seq = seq.replace('(+.98)','mod')
                seq = seq.replace('(+57.02)','')
            else:
                seq = seq.replace('+15.99','mod')
                seq = seq.replace('+.98','mod')
                seq = seq.replace('+57.02','')
            scan_seq[scan]=seq
            scan_mass[scan]=mass
            scan_charge[scan]=charge
        except:
            break

           
    original_seq = pd.DataFrame.from_dict(scan_seq,orient='index',dtype=str)
    original_seq = original_seq.reset_index()
    original_seq.columns = ['scan','sequence']
    original_seq['pepmass'] = original_seq['scan'].map(scan_mass)
    original_seq['charge'] = original_seq['scan'].map(scan_charge)
    
    original_seq['scan'] = original_seq['scan'].str.split('=',n=1, expand=True)[0]
    #print(original_seq)
    return original_seq

def prep_output(output_filepath,force_iso_leucin_wildcard=True):

   
    df = pd.read_csv(output_filepath,delimiter='\t')
    df['scan'] = pd.DataFrame(df['scan'],dtype='str')
    df['predicted_sequence'] = df['predicted_sequence'].str.replace('Cmod','C') 
    df['predicted_sequence'] = df['predicted_sequence'].str.replace('Qmod','Q')
    df['predicted_sequence'] = df['predicted_sequence'].str.replace('Nmod','N')
    df['predicted_sequence'] = df['predicted_sequence'].str.replace('Mmod','M') 
    df['predicted_sequence'] = df['predicted_sequence'].str.replace(',','')
    if force_iso_leucin_wildcard:
        df['predicted_sequence'] = df['predicted_sequence'].str.replace(r'[IL]','I')
    #print(df)
    return df

def compare_labels(input_filepath,output_filepath):
    original_seq = prep_input(input_filepath,brackets=True)
    result = prep_output(output_filepath)
    combined = pd.merge(original_seq,result,how='left',on='scan')
    combined['hit'] = np.where(combined['sequence'] == combined['predicted_sequence'],True,False)
    combined = combined.replace([np.inf, -np.inf], np.nan)
    combined = combined.dropna(subset=['predicted_score'])
    combined['probability_score'] = np.exp(combined['predicted_score'])
    cols = combined.columns.tolist()
    cols = cols[:2] + cols[4:] + cols[2:4] 
    combined = combined[cols]
    print(combined.predicted_sequence.map(lambda x: len(x)).max())
    print(combined.sequence.map(lambda x: len(x)).max())
    results = combined.to_csv('/Users/satwantkaur/Downloads/DeepNovo-master2/data.training/yeast.low.coon_2013/test_mouse_10k.csv')
    return results
    

input_filepath = '/Users/satwantkaur/Downloads/DeepNovo-master2/data.training/yeast.low.coon_2013/peaks_mouse.db.10k.mgf'
output_filepath = input_filepath + '.deepnovo_denovo.kmer'  
combined_mouse = compare_labels(input_filepath=input_filepath,output_filepath=output_filepath)

print(combined_mouse)