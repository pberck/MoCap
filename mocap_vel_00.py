import pandas as pd
import math
import matplotlib.pyplot as mp
import numpy as np

# Use PYVENV in Development


mocap_filename = "mocap_valentijn/beach_repr_2b_velocity_M.tsv"

'''
(PYVENV) pberck@ip30-163 MoCap % head beach_repr_2b_velocity_M.tsv
NO_OF_FRAMES	20887
NO_OF_DATA_TYPES	28
FREQUENCY	200
TIME_STAMP	2022-11-22, 21:34:11
DATA_INCLUDED	Velocity
DATA_TYPES	x_LWristOut_vel_M	X_LWristIn_vel_M	x_LHandOut_vel_M	x_LHandIn_vel_M	x_RWristOut_vel_M	x_RWristIn_vel_M	x_RHandOut_vel_M	x_RHandIn_vel_M	x_RThumb1_vel_M	x_RThumbTip_vel_M	x_RIndex2_vel_M	x_RIndexTip_vel_M	x_RMiddle2_vel_M	x_RMiddleTip_vel_M	x_RRing2_vel_M	x_RRingTip_vel_M	x_RPinky2_vel_M	x_RPinkyTip_vel_M	x_LThumb1_vel_M	x_LThumbTip_vel_M	x_LIndex2_vel_M	x_LIndexTip_vel_M	x_LMiddle2_vel_M	x_LMiddleTip_vel_M	x_LRing2_vel_M	x_LRingTip_vel_M	x_LPinky2_vel_M	x_LPinkyTip_vel_M


1	0.00000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000
2	0.00500	12.438	14.483	73.739	109.118	12.927	11.315	11.895	12.532	14.295	14.165	73.827	265.273	191.557	22.159	16.281	16.797	19.674	26.238	161.599	184.912	109.435	119.367	142.256	161.760	164.861	208.077	124.859	144.613
'''

# Data is index plus timestamp plus 64*3 data points?

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
            if bits[0] == "DATA_TYPES":
                column_names = bits # We add a Timestamp later to this one too
                print( column_names )
        if len(bits) > 15 and lnum > 9:
            bits = [ float(x) for x in bits ]
            df_rows.append( bits[1:] ) #skip index number
        lnum += 1

for x in column_names:
    print( x )
# check for "finger movement only", "hand movement", "arm movement" (not in this data, use distances?)
'''
x_LWristOut_vel_M
x_LWristIn_vel_M

x_LHandOut_vel_M
x_LHandIn_vel_M

x_LThumb1_vel_M
x_LThumbTip_vel_M

x_LIndex2_vel_M
x_LIndexTip_vel_M

x_LMiddle2_vel_M
x_LMiddleTip_vel_M

x_LRing2_vel_M
x_LRingTip_vel_M

x_LPinky2_vel_M
x_LPinkyTip_vel_M

# ---

x_RWristOut_vel_M
x_RWristIn_vel_M

x_RHandOut_vel_M
x_RHandIn_vel_M

x_RThumb1_vel_M
x_RThumbTip_vel_M

x_RIndex2_vel_M
x_RIndexTip_vel_M

x_RMiddle2_vel_M
x_RMiddleTip_vel_M

x_RRing2_vel_M
x_RRingTip_vel_M

x_RPinky2_vel_M
x_RPinkyTip_vel_M

'''

column_names[0] = "Timestamp"
df = pd.DataFrame(df_rows, columns = column_names)
df['Time'] = pd.to_datetime(df['Timestamp'])
df['x_LWristOut_vel_M_T'] = np.where( df["x_LWristOut_vel_M"] > 240, 240, 0 )
print( df )

# plot, with "x=0" interesting plot
df.plot(
    x=0, #df["Time"],
    #y=[1,2,3,4,5,6,7,8,9,10],
    y=[1,2, 5,6], #["x_LWristOut_vel_M"],
    kind="line",
    figsize=(16, 8)
)

import matplotlib.dates as dates
fig, axes = mp.subplots(nrows=2, ncols=1, figsize=(12,6), sharex=True)
axes[0].plot(
    "Timestamp",
    "x_LWristOut_vel_M",
    data=df,
    label="LW"
)
col = np.where(df["x_LWristOut_vel_M_T"]<200,'b', 'r')
siz = np.where(df["x_LWristOut_vel_M_T"]<200,0,1)
axes[0].scatter(
    "Timestamp",
    "x_LWristOut_vel_M_T",
    marker='o',
    s=siz, c=col, #"red",
    data=df,
    label=""
)
axes[0].legend(loc="upper right")

#axes[1].plot(
#    "Timestamp",
#    "x_LHandOut_vel_M",
#    data=df
#)
for sensor in ["x_LThumb1_vel_M", "x_LThumbTip_vel_M", "x_LIndex2_vel_M", "x_LIndexTip_vel_M", "x_LMiddle2_vel_M", "x_LMiddleTip_vel_M", "x_LRing2_vel_M", "x_LRingTip_vel_M", "x_LPinky2_vel_M", "x_LPinkyTip_vel_M"]:
    axes[1].plot(
        "Timestamp",
        sensor,
        data=df
    )
#axes[1].legend(loc="upper right")
box = axes[1].get_position()
axes[1].set_position([box.x0, box.y0 + box.height * 0.12, box.width, box.height * 0.88])
axes[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=6)


'''
axes[1].plot(
    df["Timestamp"].values,
    df[5].values
    #x="Timestamp",
    #y=[1,2,3,4,5,6,7,8,9,10],
    #y=["x_LArm", "x_RArm", "x_LHandOut"],
    #kind="line",
)
axes[1].plot(
    df["Timestamp"].values,
    df[6].values
)
'''

mp.show()
