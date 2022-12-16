import pandas as pd
import math
import sys
import matplotlib.pyplot as mp
import matplotlib as mpl
import matplotlib.dates as dates
import numpy as np
from matplotlib.colors import Normalize
from matplotlib import cm
import argparse
import pympi

# Use PYVENV in Development
# (PYVENV) pberck@ip30-163 MoCap %
# python mocap_eaf.py -d mocap_valentijn/beach_repr_2b_dists.tsv -e ...

# Create/add to an existing EAF file.

# ----------------------------

parser = argparse.ArgumentParser()
parser.add_argument( "-d", "--distsfilename",
                     help="MoCap tsv file (distances, from mocap_gen_distances.py)." )
parser.add_argument( "-e", "--eaffilename",
                     help="EAF file to augment." )
args = parser.parse_args()

'''
ls mocap_valentijn/*tsv
  mocap_valentijn/beach_repr_2b.tsv		mocap_valentijn/beach_repr_2b_ang_acc_RH.tsv
  mocap_valentijn/beach_repr_2b_ang_acc_LH.tsv	mocap_valentijn/beach_repr_2b_velocity_M.tsv

ls *tsv
  beach_repr_2b.tsv		beach_repr_2b_ang_acc_RH.tsv	beach_repr_2b_velocity_M.tsv
  beach_repr_2b_ang_acc_LH.tsv	beach_repr_2b_dists.tsv
'''

# ----------------------------

# Read the distance data
df_dists = pd.read_csv(
    args.distsfilename,
    sep="\t"
)

# ----------------------------

'''
print( ",".join(sorted(df_dists.columns)) )
x_BackL, x_BackR, x_Chest, x_HeadFront, x_HeadL, x_HeadR, x_HeadTop, 

x_LAnkleOut, x_LArm, x_LElbowOut, x_LForefootIn, x_LForefootOut, x_LHandIn, x_LHandOut, x_LHeelBack, x_LIndex2, x_LIndexTip, x_LKneeOut, x_LMiddle2, x_LMiddleTip, x_LPinky2, x_LPinkyTip, x_LRing2, x_LRingTip, x_LShin, x_LShoulderBack, x_LShoulderTop, x_LThigh, x_LThumb1, x_LThumbTip, x_LToeTip, x_LWristIn, x_LWristOut, 

x_RAnkleOut, x_RArm, x_RElbowOut, x_RForefootIn, x_RForefootOut, x_RHandIn, x_RHandOut, x_RHeelBack, x_RIndex2, x_RIndexTip, x_RKneeOut, x_RMiddle2, x_RMiddleTip, x_RPinky2, x_RPinkyTip, x_RRing2, x_RRingTip, x_RShin, x_RShoulderBack, x_RShoulderTop, x_RThigh, x_RThumb1, x_RThumbTip, x_RToeTip, x_RWristIn, x_RWristOut, 

x_SpineTop, x_WaistLBack, x_WaistLFront, x_WaistRBack, x_WaistRFront
'''

# A few ad hoc distance groups.
group_Head = ["x_HeadFront", "x_HeadL", "x_HeadR", "x_HeadTop"]

group_LFoot = ["x_LAnkleOut", "x_LForefootIn", "x_LForefootOut", "x_LHeelBack", "x_LKneeOut",
               "x_LShin", "x_LThigh", "x_LToeTip"]
group_RFoot = ["x_RAnkleOut", "x_RForefootIn", "x_RForefootOut", "x_RHeelBack", "x_RKneeOut",
               "x_RShin", "x_RThigh", "x_RToeTip"]

group_LArm = ["x_LShoulderBack", "x_LShoulderTop", "x_LArm", "x_LElbowOut", "x_LHandIn",
              "x_LHandOut", "x_LWristIn", "x_LWristOut" ]
group_RArm = ["x_RShoulderBack", "x_RShoulderTop", "x_RArm", "x_RElbowOut", "x_RHandIn",
              "x_RHandOut", "x_RWristIn", "x_RWristOut" ]

group_Body = ["x_BackL", "x_BackR", "x_Chest", "x_SpineTop", 
              "x_WaistLBack", "x_WaistLFront", "x_WaistRBack", "x_WaistRFront"]


# RESAMPLING

df_dists['td'] = pd.to_timedelta(df_dists['Timestamp'], 's') # Create a timedelta column
df_dists = df_dists.set_index(df_dists['td']) # and use it as index
print( df_dists.head() )

# max() works better than mean()
df_dists = df_dists.resample("50ms").max() # This resamples the 200 Hz to 20 Hz
print( df_dists.head() )

# NAIVE IMPLEMENTATION OVER DISTANCE GROUPS

# maybe group the st/et's in a new trier, take the "max" extent over the columns to catch
# "group" movement -> resampling helps here!

# Take several sensors, put values in one timeseries to "collapse" to one dimension
# df['total']= df.iloc[:, -4:-1].sum(axis=1)
# col_list= list(df)
# col_list.remove('english')
# df['Sum'] = df[col_list].sum(axis=1)

df_dists['LATotal'] = df_dists[["x_LHandIn", "x_LHandOut", "x_LWristIn", "x_LWristOut"]].sum(axis=1)
df_dists['RATotal'] = df_dists[["x_RHandIn", "x_RHandOut", "x_RWristIn", "x_RWristOut"]].sum(axis=1)

if not args.eaffilename:
    print( "No EAF filename specified, quitting." )
    sys.exit(1)

eaf = pympi.Elan.Eaf(file_path=args.eaffilename, author='mocap_04.py')

for sensor in ["LATotal", "RATotal"]:
#for sensor in ["x_LHandIn", "x_LHandOut", "x_LWristIn", "x_LWristOut",
#               "x_RHandIn", "x_RHandOut", "x_RWristIn", "x_RWristOut",
#               "x_WaistLBack", "x_WaistRBack"]:# group_LArm+group_RArm:
    dist_max = df_dists[sensor].max()
    dist_min = df_dists[sensor].min()
    print( sensor, dist_min, dist_max )
    eaf.add_tier( sensor, ling='default-lt' )
    # instead of threshhold, difference in direction, we have that data?
    threshold = dist_max - (dist_max * 0.90) # take if > "10%"
    inside = False
    st = -1
    et = -1
    annotations = []
    previous_annotation = [0, 0]
    current_annotation = [0, 0]
    for ts, x in zip(df_dists["Timestamp"].values, df_dists[sensor].values):
    #for ts, x in zip(df_dists.index.values, df_dists[sensor].values): # timedeltas are microseconds
        if not inside and x > threshold:
            print( "NEW {:.3f} {:.4f}".format(float(ts), float(x)) )
            inside = True
            #st = int(ts / 1000000) # start time
            st = int(ts * 1000) # start time
            empty_time = st - previous_annotation[1] # to see if close to previous
            if empty_time < 200: #arbitrary... 120ms
                print( "Short" )
                print( " p ", previous_annotation )
                print( " c ", current_annotation )
                st = previous_annotation[0] # cheat, and put the previous start time
                annotations = annotations[:-1] # and remove previous annotation.
            # add to annotations here?
            current_annotation = [ st ] 
            empty = 0
            # concat annotations if close to gether? postprocess?
        elif not inside:
            pass
        elif inside and x <= threshold:
            print( "--- {:.3f} {:.4f}".format(float(ts), float(x)) )
            inside = False
            #et = int(ts / 1000000)
            et = int(ts * 1000)
            #eaf.add_annotation(sensor, st, et, value='Move')
            empty_time = et - previous_annotation[1] # not used
            previous_annotation = current_annotation
            current_annotation += [et, empty_time]
            annotations.append( current_annotation )
            current_annotation = []
    # we might have lost the last one if it is "inside" until the end.
    print( annotations )
    for annotation in annotations:
        if annotation[1] - annotation[0] > 250:
            eaf.add_annotation(sensor, annotation[0], annotation[1], value='Move')
            
eaf.to_file("mocap_valentijn/beach_repr_2_pb.eaf", pretty=True)

'''
Merging, list with intervals [start, end]
Fínd if start within x milliseconds, take the "most left" one
Find the "most right" one, that is largest in that "group"
Or just merge the rows into one.
'''


