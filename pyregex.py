import linecache
import re

txt_file = "ial_temp.txt"
is_lines = []
align_lines = []
pattern1 = "\AIS-score"
pattern2 = "\A Index"

for i, line in enumerate(open(txt_file)):
    for match in re.finditer(pattern1, line):
        is_lines.append(i+1)
    for match in re.finditer(pattern2, line):
        align_lines.append(i+2)

print(is_lines)
print(align_lines)
