import subprocess
import os
import time

start = time.time()
os.chdir("/home/andronikos/Documents/ialign_py")


# Bash command arguments

# The first one is the path to the perl script of iAlign
# -p -> contains the pdb files "/NIL/lib"
# -w -> output files will be saved "/ialign_py/outputs_new"
# Output format 2 = detailed a = "2"
# list.lst contains the names of the pdb files of the library
# target.lst contains the names of the files we run against the library (here only 1r0r.pdb)

bashCommand = "perl /home/andronikos/Documents/ialign/bin/ialign.pl -a 2 -mini 9 -w /home/andronikos/Documents/ialign_py/outputs_new -p /home/andronikos/Downloads/NIL/lib -l list.lst -l2 target.lst"
# bashCommand = "perl /home/andronikos/Documents/ialign/bin/ialign.pl -a 2 -mini 9 -w /home/andronikos/Documents/Optimus_Bind/ialign_py/test1_out -p /home/andronikos/Documents/Optimus_Bind/ialign_py/test1 1a4eABAB_int.pdb 1A4Y.pdb"
log = open('ial_out1.txt', 'a')
process = subprocess.Popen(bashCommand.split(), stdout=log)
output, error = process.communicate()
end = time.time()
print(end-start)
