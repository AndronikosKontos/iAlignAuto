import os
import linecache
import re
import pandas as pd

os.chdir("/home/andronikos/Documents/ialign_py") # Replace this with your specific directory

# int_1r0r contains the positions of the residues in the interface of 1r0r
# Will be extracted automatically, here it is mannually filled
int_1r0r = [11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 35, 33, 64, 96, 99, 100, 101, 102, 103, 104, 107, 125, 126, 127, 128, 152, 154, 155, 189, 209, 217, 218, 219, 220, 221]
dict_temp = dict.fromkeys(int_1r0r, '-')    # Use the positions as keys for the dictionary
dict = {'pID': '-', 'is-score': [0]}
dict.update(dict_temp)
temp_dict = dict.copy()     # Temporary dictionary. Will be used to load data in the dataframe
df_1r0r = pd.DataFrame(data=dict)   # Create a dataframe from the dictionary
txt_file = 'ial_out1.txt'
n_align = 0         # Number of alignments (occured from running iAlign)

# The following lists will be used to store the lines that contain the information we want

is_lines = []       # Each item of the list contains the number of the line where the IS score is
align_lines = []    # Each item of the list contains the number of the line where the residues' columns begin
struct1_lines = []  # Each item of the list contains the number of the line where the name of the Protein interface is
num_res = []        # List of the number of the residues

# Regex patterns to search the output file of iAlign
pattern1 = "\A>>>"
pattern2 = "\AIS-score"
pattern3 = "\A Index"

# Function to change amino acid name i.e ALA -> A


def changeAA(amino_acid):
    switcher = {
        "ALA": 'A',
        "ARG": 'R',
        "ASP": 'D',
        "ASN": 'N',
        "CYS": 'C',
        "GLN": 'Q',
        "GLY": 'G',
        "GLU": 'E',
        "HIS": 'H',
        "ILE": 'I',
        "LEU": 'L',
        "LYS": 'K',
        "MET": 'M',
        "PHE": 'F',
        "PRO": 'P',
        "SER": 'S',
        "THR": 'T',
        "TRP": 'W',
        "TYR": 'Y',
        "VAL": 'V',
    }

    return switcher.get(amino_acid, "0")


# Loop through the file to find the lines using regex
for i, line in enumerate(open(txt_file)):
    for match in re.finditer(pattern1, line):
        struct1_lines.append(i+1)
    for match in re.finditer(pattern2, line):
        is_lines.append(i+1)
    for match in re.finditer(pattern3, line):
        align_lines.append(i+2)

# The length of the two lists must be the same
if (len(is_lines) == len(align_lines)):
    n_align = len(align_lines)

# Loop through the lists to get the name, the IS score and the alignment
for i in range(n_align):

    # Get the name of the target protein and use it as ID
    struct1_line = linecache.getline(txt_file, struct1_lines[i])
    spl = struct1_line.split()
    str1 = spl[0]
    str1 = str1[3:]
    temp_dict['pID'] = str1

    # Get IS score
    is_score_line = linecache.getline(txt_file, is_lines[i])
    spl = is_score_line.split()
    isc = spl[2]
    if isc[-1] == ',':
        isc = isc[:-1]  # If the IS-Score ends with a comma remove it
    temp_dict['is-score'] = isc

    # Get number of aligned residues
    num_res_line = linecache.getline(txt_file, is_lines[i] + 1)
    spl = num_res_line.split()
    num_res.append(int(spl[5]))

    # Get all aligned residues in list res1 and the positions in res_pos
    res1 = []
    res_pos = []
    count = 0
    for n in range(align_lines[i], align_lines[i] + num_res[i]):
        res1_line = linecache.getline(txt_file, n).split()
        res1.append(res1_line[3])
        respos_line = linecache.getline(txt_file, n).split()
        res_pos.append(int(respos_line[5]))

    # Replace '-' with the aligned residue (if it exists) and update the dataframe

    for r in range(num_res[i]):
        res1[r] = changeAA(res1[r])
        temp_dict[res_pos[r]] = res1[r]
    df_1r0r = df_1r0r.append(temp_dict, ignore_index=True)
    temp_dict = dict.copy()

df_1r0r.to_csv('1r0r_vs_lib.csv')
print(df_1r0r)
