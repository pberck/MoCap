import pandas as pd
import math
import matplotlib.pyplot as mp
import matplotlib.dates as dates
import numpy as np

# Use PYVENV in Development

# Also read dist files. 

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
        if len(bits) > 15 and lnum > 7:
            bits = [ float(x) for x in bits ]
            df_rows.append( bits[1:] ) #skip index number
        lnum += 1

#for x in column_names:
#    print( x )
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

group_LHand    = ["x_LWristOut_vel_M", "x_LWristIn_vel_M", "x_LHandOut_vel_M", "x_LHandIn_vel_M"]
group_LFingers = ["x_LThumb1_vel_M", "x_LThumbTip_vel_M", "x_LIndex2_vel_M", "x_LIndexTip_vel_M",
                  "x_LMiddle2_vel_M", "x_LMiddleTip_vel_M", "x_LRing2_vel_M", "x_LRingTip_vel_M",
                  "x_LPinky2_vel_M", "x_LPinkyTip_vel_M"]

group_RHand    = ["x_RWristOut_vel_M", "x_RWristIn_vel_M", "x_RHandOut_vel_M", "x_RHandIn_vel_M"]
group_RFingers = ["x_RThumb1_vel_M", "x_RThumbTip_vel_M", "x_RIndex2_vel_M", "x_RIndexTip_vel_M",
                  "x_RMiddle2_vel_M", "x_RMiddleTip_vel_M", "x_RRing2_vel_M", "x_RRingTip_vel_M",
                  "x_RPinky2_vel_M", "x_RPinkyTip_vel_M"]


column_names[0] = "Timestamp"
df = pd.DataFrame(df_rows, columns = column_names)
#df['Time'] = pd.to_datetime(df['Timestamp']) # not used
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

# ----------------------------

# Read the dist data
df_dists = pd.read_csv("beach_repr_2b_dists.tsv", sep="\t")
print( df_dists )

#print( ",".join(sorted(df_dists.columns)) )
'''
x_BackL,x_BackR,x_Chest,x_HeadFront,x_HeadL,x_HeadR,x_HeadTop,

x_LAnkleOut,x_LArm,x_LElbowOut,x_LForefootIn,x_LForefootOut,x_LHandIn,x_LHandOut,x_LHeelBack,x_LIndex2,x_LIndexTip,x_LKneeOut,x_LMiddle2,x_LMiddleTip,x_LPinky2,x_LPinkyTip,x_LRing2,x_LRingTip,x_LShin,x_LShoulderBack,x_LShoulderTop,x_LThigh,x_LThumb1,x_LThumbTip,x_LToeTip,x_LWristIn,x_LWristOut,

x_RAnkleOut,x_RArm,x_RElbowOut,x_RForefootIn,x_RForefootOut,x_RHandIn,x_RHandOut,x_RHeelBack,x_RIndex2,x_RIndexTip,x_RKneeOut,x_RMiddle2,x_RMiddleTip,x_RPinky2,x_RPinkyTip,x_RRing2,x_RRingTip,x_RShin,x_RShoulderBack,x_RShoulderTop,x_RThigh,x_RThumb1,x_RThumbTip,x_RToeTip,x_RWristIn,x_RWristOut,

x_SpineTop,x_WaistLBack,x_WaistLFront,x_WaistRBack,x_WaistRFront
'''

# Create a dataframe with "distance moved across threshold" indicators.
df_dists_t = pd.DataFrame()
df_dists_t["Timestamp"] = df_dists["Timestamp"]

for sensor in ["x_LArm", "x_LElbowOut", "x_LHandIn","x_LHandOut", "x_LShoulderBack","x_LShoulderTop",
               "x_LThigh","x_LThumb1","x_LThumbTip","x_LToeTip","x_LWristIn","x_LWristOut"]:
    df_dists_t[sensor+'_T'] = np.where( df_dists[sensor] > 1, 3, 0 )

print( df_dists_t )

fig, axes = mp.subplots(nrows=2, ncols=1, figsize=(12,6), sharex=True, sharey=True)
fig.suptitle( "distances" )

col = np.where(df_dists_t["x_LElbowOut_T"] > 1, 'r', 'b')
siz = np.where(df_dists_t["x_LElbowOut_T"] > 1, 1, 0)

axes[0].plot(
    df_dists["Timestamp"].values,
    df_dists["x_LElbowOut"].values
)
axes[0].set_title("x_LElbowOut and marker")
axes[0].scatter(
    df_dists["Timestamp"].values,
    df_dists_t["x_LElbowOut_T"].values,
    s=siz, c=col
)
axes[1].set_title("x_RElbowOut")
axes[1].plot(
    df_dists["Timestamp"].values,
    df_dists["x_RElbowOut"].values
)


df_dists.plot(
    x="Timestamp",
    #y=[1,2,3,4,5,6,7,8,9,10],
    y=["x_LArm", "x_RArm", "x_LHandOut", "x_RHandOut"],
    kind="line",
    figsize=(16, 8)
)
#axes[0].scatter(
#    "Timestamp",
#    "x_LWristOut_vel_M_T",
#    marker='o',
#    s=siz, c=col, #"red",
#    data=df,
#    label=""
#)

# ----------------------------

# Plot
fig, axes = mp.subplots(nrows=2, ncols=1, figsize=(16,8), sharex=True, sharey=True)

''' see mocap_vel00.py
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
'''

for sensor in ["x_RThumb1_vel_M", "x_RThumbTip_vel_M", "x_RIndex2_vel_M", "x_RIndexTip_vel_M", "x_RMiddle2_vel_M", "x_RMiddleTip_vel_M", "x_RRing2_vel_M", "x_RRingTip_vel_M", "x_RPinky2_vel_M", "x_RPinkyTip_vel_M"]:
    axes[0].plot(
        "Timestamp",
        sensor,
        data=df
    )
#axes[1].legend(loc="upper right")
box = axes[0].get_position()
axes[0].set_position([box.x0, box.y0 + box.height * 0.12, box.width, box.height * 0.88])
axes[0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=6)

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

# Use "np.condition" to determine hand/finger/arm movements? (1/0 columns)

mp.show()
'''
# For creating new column with multiple conditions
conditions = [
    (df['Base Column 1'] == 'A') & (df['Base Column 2'] == 'B'),
    (df['Base Column 3'] == 'C')]
choices = ['Conditional Value 1', 'Conditional Value 2']
df['New Column'] = np.select(conditions, choices, default='Conditional Value 1')

siz = np.where(df["x_LWristOut_vel_M_T"]<200,0,1)

conditions = [
    df['gender'].eq('male') & df['pet1'].eq(df['pet2']),
    df['gender'].eq('female') & df['pet1'].isin(['cat', 'dog'])
]
choices = [5,5]
df['points'] = np.select(conditions, choices, default=0)
print(df)
'''
