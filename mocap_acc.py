import pandas as pd
import math
import matplotlib.pyplot as mp
import numpy as np

# Use PYVENV in Development


mocap_filename = "mocap_valentijn/beach_repr_2b_ang_acc_LH.tsv"

'''
NO_OF_FRAMES	20887
NO_OF_DATA_TYPES	1
FREQUENCY	200
TIME_STAMP	2022-11-22, 22:00:35
DATA_INCLUDED	Angular Acceleration
DATA_TYPES	Angular_Acceleration


1	0.00000	0.000
2	0.00500	165.227
'''

df = None
df_rows = []
lnum = 0
freq = 200 # available in file header
with open(mocap_filename, "r") as f:
    for line in f:
        bits = line.split()
        #print( lnum, len(bits) )
        if len(bits) > 1:
            if bits[0] == "FREQUENCY":
                freq = int(bits[1])
        if len(bits) == 3 and lnum > 7:
            bits = [ float(x) for x in bits ]
            df_rows.append( bits[1:] ) #skip index number
        lnum += 1

column_names = ["Timestamp", "AngAcc"]
df = pd.DataFrame(df_rows, columns = column_names)
df['Time'] = pd.to_datetime(df['Timestamp'])
print( df )

# plot, with "x=0" interesting plot
df.plot(
    x=0, #df["Time"],
    #y=[1,2,3,4,5,6,7,8,9,10],
    y=[1], #["x_LWristOut_vel_M"],
    kind="line",
    figsize=(16, 8)
)

mp.show()
