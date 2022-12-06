import pandas as pd

mocap_filename = "beach_repr_2b.tsv"

df = pd.read_csv(
    mocap_filename,
    delim_whitespace=True,
    #sep='\t',
    skiprows=10
)

'''
MARKER_NAMES	x_HeadL	x_HeadTop	x_HeadR	x_HeadFront	x_LShoulderTop	x_LShoulderBack	x_LArm	x_LElbowOut	x_LWristOut	x_LWristIn	x_LHandOut	x_LHandIn	x_RShoulderTop	x_RShoulderBack	x_RArm	x_RElbowOut	x_RWristOut	x_RWristIn	x_RHandOut	x_RHandIn	x_Chest	x_SpineTop	x_BackL	x_BackR	x_WaistLFront	x_WaistLBack	x_WaistRFront	x_WaistRBack	x_LThigh	x_LKneeOut	x_LShin	x_LAnkleOut	x_LHeelBack	x_LForefootOut	x_LToeTip	x_LForefootIn	x_RThigh	x_RKneeOut	x_RShin	x_RAnkleOut	x_RHeelBack	x_RForefootOut	x_RToeTip	x_RForefootIn	x_RThumb1	x_RThumbTip	x_RIndex2	x_RIndexTip	x_RMiddle2	x_RMiddleTip	x_RRing2	x_RRingTip	x_RPinky2	x_RPinkyTip	x_LThumb1	x_LThumbTip	x_LIndex2	x_LIndexTip	x_LMiddle2	x_LMiddleTip	x_LRing2	x_LRingTip	x_LPinky2	x_LPinkyTip
'''

print( df )
print( df.columns, len(df.columns) )

for i in range(10): #len(df)):
    for j in range(65):
        print( df.iloc[i, j] )
    print()
