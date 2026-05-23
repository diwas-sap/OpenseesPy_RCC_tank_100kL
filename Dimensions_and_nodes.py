import openseespy.opensees as ops
import numpy as np
import matplotlib.pyplot as plt
import opsvis as opsv

ops.wipe()
ops.model('BasicBuilder', '-ndm', 3, '-ndf', 6)


#----------------------------------------------------------------------------------
# Geometry, Dimensions And Units (mm, s, N) , Global axes X, Y, Z (vertical) 
#----------------------------------------------------------------------------------

inch = 25.4
ft = 12. * inch
rigidDiaphragm = 1
LRB_inclusion = 0   # 1 = yes, 0 = no 



# --------------------------------------------------------------------------------
# LRB Dimensions
# --------------------------------------------------------------------------------

D1 = 80          	            # Internal diameter of lead rubber bearing
D2 = 500              		    # Outer diameter of lead rubber bearing (excluding cover thickness)

ts = 3.0         				    # Thickness of single steel shim plate mm
tr = 5.6     					    # Thicness of a single rubber layer mm
tc = 15.              				# Bearing cover mm

n = 17           				# Number of rubber layers

Tr = n*tr             				# Total rubber thickness
h_LRB = Tr + (n-1)*ts          		# Total height of bearing

# ─────────────────────────────────────────────────────────────────────────────
# 3.  NODES  (explicit coordinates, mm)
# ─────────────────────────────────────────────────────────────────────────────
#
#  Elevation summary:
#    Floor 0 (base)   Z =     0
#    Floor 1          Z =  4000
#    Floor 2          Z =  7500
#    Floor 3          Z = 11000
#    Floor 4          Z = 14500
#    Floor 5          Z = 18000
#    Floor 6          Z = 21500
#    Floor 7 (roof)   Z = 25000
#
#  Plan corners:
#    col0 → (    0,    0)
#    col1 → ( 3850,    0)
#    col2 → ( 3850, 3850)
#    col3 → (    0, 3850)
#
# ── Floor 0  (base, Z = 0) ───────────────────────────────────────────────────
if LRB_inclusion == 1:
    print("LRB is installed...")
    ops.node( 101,    0.,    0.,  -h_LRB)   # floor0, col0
    ops.node( 102, 3850.,    0.,   -h_LRB)   # floor0, col1
    ops.node( 103, 3850., 3850.,   -h_LRB)   # floor0, col2
    ops.node( 104,    0., 3850.,    -h_LRB)   # floor0, col3
    LRB_nodes = [101, 102, 103, 104]
else:
    print("LRB is not installed...")

ops.node( 1,    0.,    0.,  0.)   # floor0, col0
ops.node( 2, 3850.,    0.,  0.)   # floor0, col1
ops.node( 3, 3850., 3850.,  0.)   # floor0, col2
ops.node( 4,    0., 3850.,  0.)   # floor0, col3
floor_0_nodes = [1, 2, 3, 4]  

if LRB_inclusion == 1:
    for node in LRB_nodes:
        ops.fix(node, 1, 1, 1, 1, 1, 1)

    Base_nodes = LRB_nodes
else:
    for node in floor_0_nodes:
        ops.fix(node, 1, 1, 1, 1, 1, 1)

    Base_nodes = floor_0_nodes
   
# ── Floor 1  (Z = 4000) ──────────────────────────────────────────────────────
ops.node(11,    0.,    0.,  4000.)   # floor1, col0
ops.node(12, 3850.,    0.,  4000.)   # floor1, col1
ops.node(13, 3850., 3850.,  4000.)   # floor1, col2
ops.node(14,    0., 3850.,  4000.)   # floor1, col3

floor_1_nodes = [11, 12, 13, 14]

# ── Floor 2  (Z = 7500) ──────────────────────────────────────────────────────
ops.node(21,    0.,    0.,  7500.)   # floor2, col0
ops.node(22, 3850.,    0.,  7500.)   # floor2, col1
ops.node(23, 3850., 3850.,  7500.)   # floor2, col2
ops.node(24,    0., 3850.,  7500.)   # floor2, col3

floor_2_nodes = [21, 22, 23, 24]

# ── Floor 3  (Z = 11000) ─────────────────────────────────────────────────────
ops.node(31,    0.,    0., 11000.)   # floor3, col0
ops.node(32, 3850.,    0., 11000.)   # floor3, col1
ops.node(33, 3850., 3850., 11000.)   # floor3, col2
ops.node(34,    0., 3850., 11000.)   # floor3, col3

floor_3_nodes = [31, 32, 33, 34]

# ── Floor 4  (Z = 14500) ─────────────────────────────────────────────────────
ops.node(41,    0.,    0., 14500.)   # floor4, col0
ops.node(42, 3850.,    0., 14500.)   # floor4, col1
ops.node(43, 3850., 3850., 14500.)   # floor4, col2
ops.node(44,    0., 3850., 14500.)   # floor4, col3

floor_4_nodes = [41, 42, 43, 44]

# ── Floor 5  (Z = 18000) ─────────────────────────────────────────────────────
ops.node(51,    0.,    0., 18000.)   # floor5, col0
ops.node(52, 3850.,    0., 18000.)   # floor5, col1
ops.node(53, 3850., 3850., 18000.)   # floor5, col2
ops.node(54,    0., 3850., 18000.)   # floor5, col3

floor_5_nodes = [51, 52, 53, 54]

# ── Floor 6  (Z = 21500) ─────────────────────────────────────────────────────
ops.node(61,    0.,    0., 21500.)   # floor6, col0
ops.node(62, 3850.,    0., 21500.)   # floor6, col1
ops.node(63, 3850., 3850., 21500.)   # floor6, col2
ops.node(64,    0., 3850., 21500.)   # floor6, col3

floor_6_nodes = [61, 62, 63, 64]

# ── Floor 7  (roof, Z = 25000) ───────────────────────────────────────────────
ops.node(71,    0.,    0., 25000.)   # floor7, col0
ops.node(72, 3850.,    0., 25000.)   # floor7, col1
ops.node(73, 3850., 3850., 25000.)   # floor7, col2
ops.node(74,    0., 3850., 25000.)   # floor7, col3

floor_7_nodes = [71, 72, 73, 74]


# ── roof  (roof, Z = 28425) ───────────────────────────────────────────────
ops.node(81,    0.,    0., 28425.)   # roof, col0
ops.node(82, 3850.,    0., 28425.)   # roof, col1
ops.node(83, 3850., 3850., 28425.)   # roof, col2
ops.node(84,    0., 3850., 28425.)   # roof, col3

roof_nodes = [81, 82, 83, 84]



# Nodes for impulsive and empty tank mass, convective mass ------------------------------------------------------------
ops.node(9001, 1925.0, 1925.0, 28425 + 1238.9)  # impulsive and empty tank mass location
ops.node(9002, 1925.0, 1925.0, 28425 + 2756.2)  # convective mass node for rigid link with staging
ops.node(9003, 1925.0, 1925.0, 28425 + 2756.2)  # convective mass node for zero length element 

ops.fix(9001, 0, 0, 1, 1, 1, 1)
ops.fix(9002, 0, 0, 1, 1, 1, 1)
ops.fix(9003, 0, 0, 1, 1, 1, 1)


# --------------------------------------------------------------------------------
# Master Nodes # ops.node(nodeTag, x, y, z)
# --------------------------------------------------------------------------------

print("Rigid Diaphragm ON....")
ops.constraints('Transformation')
perp_direction = 3 

master_nodes = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009]

ops.node(1001, 1925.0, 1925.0, 0.0)          # Master node for base floor
ops.node(1002, 1925.0, 1925.0, 4000.0)       # Master node for floor 1
ops.node(1003, 1925.0, 1925.0, 7500.0)       # Master node for floor 2
ops.node(1004, 1925.0, 1925.0, 11000.0)      # Master node for floor 3
ops.node(1005, 1925.0, 1925.0, 14500.0)      # Master node for floor 4
ops.node(1006, 1925.0, 1925.0, 18000.0)      # Master node for floor 5
ops.node(1007, 1925.0, 1925.0, 21500.0)      # Master node for floor 6
ops.node(1008, 1925.0, 1925.0, 25000.0)      # Master node for floor 7
ops.node(1009, 1925.0, 1925.0, 28425.0)      # Master node for roof


# ops.rigidDiaphragm(perp_direction, master_nodeTag, *slaveNodeTags) 
ops.rigidDiaphragm(perp_direction, 1001, *floor_0_nodes)  
ops.rigidDiaphragm(perp_direction, 1002, *floor_1_nodes)      
ops.rigidDiaphragm(perp_direction, 1003, *floor_2_nodes)      
ops.rigidDiaphragm(perp_direction, 1004, *floor_3_nodes)      
ops.rigidDiaphragm(perp_direction, 1005, *floor_4_nodes)      
ops.rigidDiaphragm(perp_direction, 1006, *floor_5_nodes)      
ops.rigidDiaphragm(perp_direction, 1007, *floor_6_nodes)      
ops.rigidDiaphragm(perp_direction, 1008, *floor_7_nodes)      
ops.rigidDiaphragm(perp_direction, 1009, *roof_nodes)

# ops.fix(master_nodeTag, x, y, z, Mx, My, Mz)  

if LRB_inclusion == 1:       
    ops.fix(1001, 0, 0, 1, 1, 1, 0)    
else:    
    ops.fix(1001, 1, 1, 1, 1, 1, 1) 


ops.fix(1002, 0, 0, 1, 1, 1, 0)       
ops.fix(1003, 0, 0, 1, 1, 1, 0)      
ops.fix(1004, 0, 0, 1, 1, 1, 0)     
ops.fix(1005, 0, 0, 1, 1, 1, 0)
ops.fix(1006, 0, 0, 1, 1, 1, 0)
ops.fix(1007, 0, 0, 1, 1, 1, 0)
ops.fix(1008, 0, 0, 1, 1, 1, 0)
ops.fix(1009, 0, 0, 1, 1, 1, 0)


vertical_nodes= master_nodes + [9001, 9002, 9003]