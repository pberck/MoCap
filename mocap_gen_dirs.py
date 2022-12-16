import pandas as pd
import math
import argparse
import os

# Use PYVENV in Development

# Creates a file with "directions" from 3D positions.
# Analogeous to gen_dists.py

parser = argparse.ArgumentParser()
parser.add_argument( "-f", "--filename", help="MoCap tsv file (3D positions).",
                     default="mocap_valentijn/beach_repr_2b.tsv" )
args = parser.parse_args()

filepath_bits  =  os.path.split( args.filename )
dirs_filename = os.path.join( filepath_bits[0], filepath_bits[1][:-4] + "_dirs.tsv" ) # Note, no error checking
print( filepath_bits, dirs_filename )

# Data is index plus timestamp plus 64*3 data points?

# Read the original data, save in df_rows which is used later to calculate
# the distances.
df      = None
df_rows = []
lnum    = 0
freq    = 200 # parse from file header
with open(args.filename, "r") as f:
    for line in f:
        bits = line.split()
        #print( lnum, len(bits) )
        if bits[0] == "FREQUENCY":
            freq = int(bits[1])
        if bits[0] == "MARKER_NAMES":
            column_names = bits[1:] # We add a Timestamp later to this one too
            print( column_names )
            # Expand to 3 coordinates later
            new_column_names = ["Timestamp"]
            for col in column_names:
                for coord in ["_X", "_Y", "_Z"]:
                    new_column_names.append( col+coord )
            print( new_column_names )
        if len(bits) > 65:
            bits     = [ float(x) for x in bits ]
            triplets = [bits[i:i + 3] for i in range(2,len(bits)-2, 3)]
            df_rows.append( bits[1:] ) #skip index number
            #print( bits[0], bits[1], len(triplets), triplets[0], triplets[1] ) #bits[2:2+6] )
        lnum += 1

# Calcuate the distances, save in a new dataframe.
def dist3d(v0, v1):
    dist = sum( [ (x-y)*(x-y) for x,y in zip(v0, v1) ] )
    return math.sqrt( dist )

# Direction. Should we do some post-processing here?
# Return a binary vector, if delta larger than threshold?
# Do we need rotation? Are the delta's along axes?
def delta(v0, v1):
    deltas = [ x-y for x,y in zip(v0, v1) ]
    return deltas

df_distances  = []
df_dists_rows = [ [0.0] * len(column_names) ] # init with zeros for timestamp 000000
row           = df_rows[0]
prev_triplets = [ row[i:i + 3] for i in range(1,len(row)-1, 3) ]
#print( prev_triplets )
for row in df_rows[1:]:
    #print( row )
    ts       = row[0] # timestamp
    new_row  = [ ts ]
    triplets = [ row[i:i + 3] for i in range(1,len(row)-1, 3) ]
    for t0,t1 in zip(triplets, prev_triplets):
        direction = delta( t0, t1 ) # three values
        new_row.append( direction )
    prev_triplets = triplets
    df_dists_rows.append( new_row )

# Distances, use original column names b/c only one dist per "triplet", we add timestamp.
column_names = ["Timestamp"] + column_names
df_dists     = pd.DataFrame(
    df_dists_rows,
    columns=column_names
)
print( df_dists.head() )

# Save it
df_dists.to_csv(
    dirss_filename,
    index=False,
    sep="\t"
)
print( "Saved:", dists_filename )




df      = None
df_rows = []
lnum    = 0
freq    = 200 # parse from file header

for row in df_rows[1:]:
    #print( row )
    ts       = row[0] # timestamp
    new_row  = [ ts ]
    triplets = [ row[i:i + 3] for i in range(1,len(row)-1, 3) ]
    for t0,t1 in zip(triplets, prev_triplets):
        dist = dist3d( t0, t1 )
        new_row.append( dist )
    prev_triplets = triplets
    df_dists_rows.append( new_row )

# Distances, use original column names b/c only one dist per "triplet", we add timestamp.
column_names = ["Timestamp"] + column_names
df_dists     = pd.DataFrame(
    df_dists_rows,
    columns=column_names
)
print( df_dists.head() )



