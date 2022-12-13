import pympi

foo = pympi.Elan.Eaf(file_path="mocap_valentijn/beach_repr_2.eaf", author='pympi')
print( foo.tiers )

foo.add_tier("RHand", ling='default-lt') 

print( foo.tiers )
foo.add_annotation("RHand", 1200, 1500, value='AI')

foo.to_file("mocap_valentijn/beach_repr_2_pb.eaf", pretty=True)


