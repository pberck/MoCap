import pandas as pd
import math
import matplotlib.pyplot as mp

# Use PYVENV in Development

mocap_filename = "mocap_valentijn/beach_repr_2b.tsv"

'''
(PYVENV) pberck@ip30-163 MoCap % head beach_repr_2b.tsv 
NO_OF_FRAMES	20887
NO_OF_CAMERAS	20
NO_OF_MARKERS	64
FREQUENCY	200
NO_OF_ANALOG	0
ANALOG_FREQUENCY	0
DESCRIPTION	--
TIME_STAMP	2022-06-02, 12:47:37.307	15048.13469883
DATA_INCLUDED	3D
MARKER_NAMES	x_HeadL	x_HeadTop	x_HeadR	x_HeadFront	x_LShoulderTop	x_LShoulderBack	x_LArm	x_LElbowOut	x_LWristOut	x_LWristIn	x_LHandOut	x_LHandIn	x_RShoulderTop	x_RShoulderBack	x_RArm	x_RElbowOut	x_RWristOut	x_RWristIn	x_RHandOut	x_RHandIn	x_Chest	x_SpineTop	x_BackL	x_BackR	x_WaistLFront	x_WaistLBack	x_WaistRFront	x_WaistRBack	x_LThigh	x_LKneeOut	x_LShin	x_LAnkleOut	x_LHeelBack	x_LForefootOut	x_LToeTip	x_LForefootIn	x_RThigh	x_RKneeOut	x_RShin	x_RAnkleOut	x_RHeelBack	x_RForefootOut	x_RToeTip	x_RForefootIn	x_RThumb1	x_RThumbTip	x_RIndex2	x_RIndexTip	x_RMiddle2	x_RMiddleTip	x_RRing2	x_RRingTip	x_RPinky2	x_RPinkyTip	x_LThumb1	x_LThumbTip	x_LIndex2	x_LIndexTip	x_LMiddle2	x_LMiddleTip	x_LRingx_LRingTip	x_LPinky2	x_LPinkyTip
'''

# Data is index plus timestamp plus 64*3 data points?

df = None
df_rows = []
lnum = 0
with open(mocap_filename, "r") as f:
    for line in f:
        bits = line.split()
        #print( lnum, len(bits) )
        if bits[0] == "MARKER_NAMES":
            column_names = bits[1:]
            print( column_names )
            # Expand to 3 coordinates?
            new_column_names = ["Timestamp"]
            for col in column_names:
                for coord in ["_X", "_Y", "_Z"]:
                    new_column_names.append( col+coord )
            print( new_column_names )
        if len(bits) > 65:
            bits = [ float(x) for x in bits ]
            triplets = [bits[i:i + 3] for i in range(2,len(bits)-2, 3)]
            #print( triplets )
            df_rows.append( bits[1:] ) #skip index number
            #print( bits[0], bits[1], len(triplets), triplets[0], triplets[1] ) #bits[2:2+6] )
        lnum += 1
        if lnum > (10000+10):
            pass
            #break

# Pre-calc the distances in a new dataframe
def dist3d(v0, v1):
    dist = sum( [ (x-y)*(x-y) for x,y in zip(v0, v1) ] )
    return math.sqrt( dist )

df_distances = []
df_dists_rows = [ [0.0] * len(column_names) ] # init with zeros for timestamp 000000
row = df_rows[0]
prev_triplets = [row[i:i + 3] for i in range(1,len(row)-1, 3)]
print( prev_triplets )
for row in df_rows[1:]:
    print( row )
    new_row = []
    triplets = [row[i:i + 3] for i in range(1,len(row)-1, 3)]
    for t0,t1 in zip(triplets, prev_triplets):
        dist = dist3d( t0, t1 )
        #print( t0, t1, dist )
        new_row.append( dist )
    prev_triplets = triplets
    df_dists_rows.append( new_row )
    
df = pd.DataFrame(df_rows, columns = new_column_names)
print( df )

# distances, use column names b/c one dist per "triplet"
df_dists = pd.DataFrame(df_dists_rows, columns = column_names)
print( df_dists )

# plot
df_dists.plot( 
    y=[1,2,3,4,5,6],
    kind="line",
    figsize=(16, 8)
)
mp.show()
