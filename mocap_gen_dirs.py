import pandas as pd
import math
import argparse
import os
import sys

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
                for coord in ["_X_dir", "_Y_dir", "_Z_dir"]:
                    new_column_names.append( col+coord )
            print( new_column_names )
        if len(bits) > 65:
            bits     = [ float(x) for x in bits ]
            triplets = [bits[i:i + 3] for i in range(2,len(bits)-2, 3)]
            df_rows.append( bits[1:] ) #skip index number
            #print( bits[0], bits[1], len(triplets), triplets[0], triplets[1] ) #bits[2:2+6] )
        lnum += 1

# Direction. Should we do some post-processing here?
# Return a binary vector, if delta larger than threshold?
# Do we need rotation? Are the delta's along axes?
#sign = lambda x: math.copysign(1, x)
def sign(n):
    #return n
    if abs(n) < 1:
        return 0
    return n 

def delta(v0, v1):
    deltas = [ sign(x-y) for x,y in zip(v0, v1) ] # with sign we return -1/0/1
    '''
    dirs = [] # do this in postprocessing/annotation generation.
    if deltas[0] < 0:
        dirs.append( "L" ) # X, left
    elif deltas[0] > 0:
        dirs.append( "R" ) # X, right
    else:
        dirs.append( "-" ) # X, nothing
    if deltas[1] < 0:
        dirs.append( "B" ) # Y, backwards
    elif deltas[1] > 0:
        dirs.append( "F" ) # Y, fowards
    else:
        dirs.append( "-" ) # Y, nothing
    if deltas[2] < 0:
        dirs.append( "D" ) # Z, down
    elif deltas[2] > 0:
        dirs.append( "U" ) # Z, up
    else:
        dirs.append( "-" ) # Z, nothing
    '''
    return deltas #dirs

df_dirs_rows  = [ [0.0] * len(new_column_names) ] # init with zeros for timestamp 000000
row           = df_rows[0]
prev_triplets = [ row[i:i + 3] for i in range(1,len(row)-1, 3) ]
#print( prev_triplets )
for row in df_rows[1:]:
    #print( row )
    ts       = row[0] # timestamp
    new_row  = [ ts ]
    triplets = [ row[i:i + 3] for i in range(1,len(row)-1, 3) ]
    for t0,t1 in zip(triplets, prev_triplets):# X, Y, Z
        direction = delta( t0, t1 ) # three values
        new_row += direction 
    prev_triplets = triplets
    df_dirs_rows.append( new_row )

# Directions, we have three per triplet, so we need the new "extended" column names.
column_names = ["Timestamp"] + new_column_names
df_dirs      = pd.DataFrame(
    df_dirs_rows,
    columns=new_column_names
)
print( df_dirs.head() )

# Save it
df_dirs.to_csv(
    dirs_filename,
    index=False,
    sep="\t"
)
print( "Saved:", dirs_filename )

print( df_dirs.max() )


