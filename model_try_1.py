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

kg = 1.0/1000     # Mass in Ns2/mm or tonne

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
ops.node( 1,    0.,    0.,     0.)   # floor0, col0
ops.node( 2, 3850.,    0.,     0.)   # floor0, col1
ops.node( 3, 3850., 3850.,     0.)   # floor0, col2
ops.node( 4,    0., 3850.,     0.)   # floor0, col3

base_nodes = [1, 2, 3, 4]

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



# ─────────────────────────────────────────────────────────────────────────────
# 4.  BOUNDARY CONDITIONS
# ─────────────────────────────────────────────────────────────────────────────
# Fixed column bases (floor 0)
for node in base_nodes:
    ops.fix(node, 1, 1, 1, 1, 1, 1)

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
ops.rigidDiaphragm(perp_direction, 1001, *base_nodes)      
ops.rigidDiaphragm(perp_direction, 1002, *floor_1_nodes)      
ops.rigidDiaphragm(perp_direction, 1003, *floor_2_nodes)      
ops.rigidDiaphragm(perp_direction, 1004, *floor_3_nodes)      
ops.rigidDiaphragm(perp_direction, 1005, *floor_4_nodes)      
ops.rigidDiaphragm(perp_direction, 1006, *floor_5_nodes)      
ops.rigidDiaphragm(perp_direction, 1007, *floor_6_nodes)      
ops.rigidDiaphragm(perp_direction, 1008, *floor_7_nodes)      
ops.rigidDiaphragm(perp_direction, 1009, *roof_nodes)

# ops.fix(master_nodeTag, x, y, z, Mx, My, Mz)      
ops.fix(1001, 1, 1, 1, 1, 1, 1)       
ops.fix(1002, 0, 0, 1, 1, 1, 0)       
ops.fix(1003, 0, 0, 1, 1, 1, 0)      
ops.fix(1004, 0, 0, 1, 1, 1, 0)     
ops.fix(1005, 0, 0, 1, 1, 1, 0)
ops.fix(1006, 0, 0, 1, 1, 1, 0)
ops.fix(1007, 0, 0, 1, 1, 1, 0)
ops.fix(1008, 0, 0, 1, 1, 1, 0)
ops.fix(1009, 0, 0, 1, 1, 1, 0)


gamma_conc = 2.5e-5       # N/mm^3 (for γ = 25 kN/m^3)
gamma_masonry = 2.0e-5    # N/mm^3 (for γ = 20 kN/m^3)
g = 9.81e3                # mm/s^2

unconfined_concrete_tag = 1     # unconfined concrete for cover
confined_concrete_tag = 2       # confined concrete for core
steel_tag = 3                   # reinforcement
elastic_material_tag = 4        # elastic material for spring in zero length element

Kc = 234.37                    # Convective Mass Spring Constant (Kc) in N/mm or kN/m

# nominal concrete compressive strength
fc = -25.               # CONCRETE Compressive Strength (+Tension, -Compression)
Ec = 5000 * (-fc)**0.5  # Concrete Elastic Modulus (the term in sqr root in Mpa)
Kfc = 1.10			    # ratio of confined to unconfined concrete strength
Kres = 0.1			    # ratio of residual/ultimate to maximum stress
lambda_u = 0.1          # ratio between unloading slope at $eps2 and initial slope $Ec

# unconfined concrete (U) : compressive stress-strain properties
fc1U = fc               # (todeschini parabolic model), maximum compressive stress
eps1U = -0.002          # strain at maximum compressive stress
fc2U = Kres * fc1U      # ultimate compressive stress
eps2U = -0.02           # strain at ultimate compressive stress

# confined concrete (C) : compressive stress-strain properties
fc1C = Kfc * fc1U           # (mander model), maximum compressive stress
eps1C  = max(eps1U * (1 + 5 * (Kfc - 1)), -0.006)    # strain at maximum compressive stress
fc2C = Kres * fc1C          # ultimate compressive stress
eps2C = 10 * eps1C          # strain at ultimate compressive stress

# tensile stress-strain properties
ftC = -0.1 * fc1C  # tensile strength +tension
ftU = -0.1 * fc1U  # tensile strength +tension
Ets = ftU / 0.002   # tension softening stiffness

# STEEL parameters for Steel02
Fy_steel = 500.     # Yield stress (MPa)
E0_steel = 2.0e5    # Initial modulus (MPa)
Bs = 0.01           # strain-hardening ratio
params_steel = [20,0.925,0.15]             # control the transition from elastic to plastic branches

# uniaxialMaterial('Concrete02', matTag, fpc, epsc0, fpcu, epsU, lambda, ft, Ets)
ops.uniaxialMaterial("Concrete02", unconfined_concrete_tag, fc1U, eps1U, fc2U, eps2U, lambda_u, ftU, Ets)   # unconfined concrete for cover
ops.uniaxialMaterial("Concrete02", confined_concrete_tag, fc1C, eps1C, fc2C, eps2C, lambda_u, ftC, Ets)     # confined concrete for core
ops.uniaxialMaterial("Steel02", steel_tag, Fy_steel, E0_steel, Bs, *params_steel)
ops.uniaxialMaterial('Elastic', elastic_material_tag, Kc)                                                   # uniaxialMaterial('Elastic', matTag, E, eta=0.0, Eneg=E)




def area(diameter):
    return (np.pi * diameter ** 2) / 4.0

Staging_Beam_SecTag = 1
Tank_Buttom_Beam_SecTag = 3
Staging_Col_SecTag = 2

# ------------------------------------------------------------------
# Beams 
# ------------------------------------------------------------------

fiber_section_staging_beam = [

['section', 'Fiber', Staging_Beam_SecTag, '-GJ', 1.0e6],
['patch', 'rect', confined_concrete_tag, 6, 6, *[-225.0, -150.0], *[225.0, 150.0]], # core

['patch', 'quad', unconfined_concrete_tag, 2, 6, *[225.0,-150.0], *[250.0, -175.0], *[250.0, 175.0], *[225.0, 150.0]],    # right side cover
['patch', 'quad', unconfined_concrete_tag, 2, 6, *[-250.0,-175.0], *[-225.0,-150.0], *[-225.0, 150.0], *[-250.0, 175.0]], # left side cover

['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-225.0,150.0], *[225.0,150.0], *[250.0, 175.0], *[-250.0, 175.0]],     # top side cover
['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-250.0,-175.0], *[250.0,-175.0], *[225.0,-150.0], *[-225.0,-150.0]],   # bottom side cover

['layer', 'straight', steel_tag, 3, area(16), *[225.0, -150.0], *[225.0, 150.0]],  # right layer
['layer', 'straight', steel_tag, 3, area(16), *[-225.0, -150.0], *[-225.0, 150.0]] # left layer

]

opsv.fib_sec_list_to_cmds(fiber_section_staging_beam)

# opsv.plot_fiber_section(fiber_section_staging_beam)
# plt.title("Beam Section for Staging")
# plt.axis('equal')
# plt.grid(True, color='gray', linestyle='--', linewidth=0.4, alpha=0.3)

fiber_section_tank_bottom_beam = [

['section', 'Fiber', Tank_Buttom_Beam_SecTag, '-GJ', 1.0e6],
['patch', 'rect', confined_concrete_tag, 9, 6, *[-225.0, -150.0], *[225.0, 150.0]],  # confined core

['patch', 'rect', unconfined_concrete_tag, 4, 6, *[25.0, 150.0], *[225.0, 425.0]],   # unconfined upper core
['patch', 'rect', unconfined_concrete_tag, 4, 6, *[25.0, -425.0], *[225.0, -150.0]], # unconfined bottom core

['patch', 'quad', unconfined_concrete_tag, 2, 18, *[225.0,-425.0], *[250.0, -450.0], *[250.0, 450.0], *[225.0, 425.0]],    # right side cover
['patch', 'quad', unconfined_concrete_tag, 2, 6, *[0.0,175.0], *[25.0, 150.0], *[25.0, 425.0], *[0.0, 450.0]],            # middle up cover
['patch', 'quad', unconfined_concrete_tag, 2, 6, *[0.0,-450.0], *[25.0,-425.0], *[25.0, -150.0], *[0.0, -175.0]],         # middle down cover
['patch', 'quad', unconfined_concrete_tag, 2, 6, *[-250.0,-175.0], *[-225.0,-150.0], *[-225.0, 150.0], *[-250.0, 175.0]], # left side cover

['patch', 'quad', unconfined_concrete_tag, 5, 2, *[-225.0,150.0], *[25.0,150.0], *[0.0, 175.0], *[-250.0, 175.0]],        # top left cover
['patch', 'quad', unconfined_concrete_tag, 4, 2, *[25.0,425.0], *[225.0,425.0], *[250.0, 450.0], *[0.0, 450.0]],          # top right cover
['patch', 'quad', unconfined_concrete_tag, 5, 2, *[-250.0,-175.0], *[0.0,-175.0], *[25.0,-150.0], *[-225.0,-150.0]],      # bottom left cover
['patch', 'quad', unconfined_concrete_tag, 4, 2, *[0.0,-450.0], *[250.0,-450.0], *[225.0,-425.0], *[25.0,-425.0]],        # bottom right cover

['layer', 'straight', steel_tag, 4, area(20), *[225.0, -150.0], *[225.0, 150.0]],           # right right layer
['layer', 'straight', steel_tag, 4, area(20), *[175.0, -150.0], *[175.0, 150.0]],           # right left layer
['layer', 'straight', steel_tag, 4, area(20), *[-225.0, -150.0], *[-225.0, 150.0]],         # left left layer
['layer', 'straight', steel_tag, 4, area(20), *[-175.0, -150.0], *[-175.0, 150.0]],         # left right layer
['layer', 'straight', steel_tag, 2, area(12), *[75.0, -150.0], *[75.0, 150.0]],             # middle right layer
['layer', 'straight', steel_tag, 2, area(12), *[-75.0 , -150.0], *[-75.0, 150.0]]           # middle left layer

]

opsv.fib_sec_list_to_cmds(fiber_section_tank_bottom_beam)

# opsv.plot_fiber_section(fiber_section_tank_bottom_beam)
# plt.title("Beam Section for tank bottom")
# plt.axis('equal')
# plt.grid(True, color='gray', linestyle='--', linewidth=0.4, alpha=0.3)

# ------------------------------------------------------------------
# Columns 
# ------------------------------------------------------------------

fiber_section_staging_col = [

['section', 'Fiber', Staging_Col_SecTag, '-GJ', 1.0e6],
['patch', 'rect', confined_concrete_tag, 6, 6, *[-185.0, -185.0], *[185.0, 185.0]], # core

['patch', 'quad', unconfined_concrete_tag, 2, 6, *[185.0,-185.0], *[225.0,-225.0], *[225.0, 225.0], *[185.0,185.0]],     # right side cover
['patch', 'quad', unconfined_concrete_tag, 2, 6, *[-225.0,-225.0], *[-185.0,-185.0], *[-185.0,185.0], *[-225.0, 225.0]], # left side cover

['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-185.0,185.0], *[185.0,185.0], *[225.0, 225.0], *[-225.0,225.0]],     # top side cover
['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-225.0,-225.0], *[225.0,-225.0], *[185.0,-185.0], *[-185.0,-185.0]],  # bottom side cover

['layer', 'straight', steel_tag, 3, area(16), *[185.0, -185.0], *[185.0, 185.0]],               # Right Layer
['layer', 'straight', steel_tag, 3, area(16), *[-185.0, -185.0], *[-185.0, 185.0]],             # Left Layer
['layer', 'straight', steel_tag, 2, area(16), *[0, -185.0], *[0, 185.0]]                        # Middle Layer

]

opsv.fib_sec_list_to_cmds(fiber_section_staging_col)

# opsv.plot_fiber_section(fiber_section_staging_col)
# plt.title("Column Section for Staging")
# plt.axis('equal')
# plt.grid(True, color='gray', linestyle='--', linewidth=0.4, alpha=0.3)

# ------------------------------------------------------------------
# Plotting of the sections 
# ------------------------------------------------------------------

# plt.show()



# --------------------------------------------------------------------------------
# Rigid Link and Elastic Link Elements  # rigidLink(type, rNodeTag, cNodeTag)
# --------------------------------------------------------------------------------

ops.rigidLink('beam', 1008, 9001)
ops.rigidLink('beam', 1008, 9002)
ops.element('zeroLength', 90023, 9002, 9003, '-mat', elastic_material_tag, elastic_material_tag, '-dir', 1, 2)


# ─────────────────────────────────────────────────────────────────────────────
# 5.  GEOMETRIC TRANSFORMATIONS
# ─────────────────────────────────────────────────────────────────────────────
Staging_Beam_X_TransfTag = 1   # beams along X
Staging_Beam_Y_TransfTag = 2   # beams along Y
Tank_Buttom_Beam_X_TransfTag = 3   # beams along X
Tank_Buttom_Beam_Y_TransfTag = 4   # beams along Y
Col_TransfTag       = 5   # vertical columns
rigid_TransfTag     = 6   # rigid links & tank verticals

ops.geomTransf('PDelta', Col_TransfTag,       -1.,  0.,  0)  # columns (Z-axis, vecxz=Y)
ops.geomTransf('Linear', Staging_Beam_X_TransfTag,  0, -1.,  0.)  # X-beams
ops.geomTransf('Linear', Staging_Beam_Y_TransfTag,  1,  0,  0.)  # Y-beams
ops.geomTransf('Linear', Tank_Buttom_Beam_X_TransfTag,  0, -1.,  0.)  # X-beams
ops.geomTransf('Linear', Tank_Buttom_Beam_Y_TransfTag,  1,  0,  0.)  # Y-beams
ops.geomTransf('Linear', rigid_TransfTag,      0.,  1.,  0.)  # rigid members

# ─────────────────────────────────────────────────────────────────────────────
# 6.  BEAM INTEGRATIONS
# ─────────────────────────────────────────────────────────────────────────────
Col_IntTag     = 1
Staging_Beam_IntTag = 2
Tank_Buttom_Beam_IntTag = 3

ops.beamIntegration('Lobatto', Col_IntTag, Staging_Col_SecTag, 5)
ops.beamIntegration('Lobatto', Staging_Beam_IntTag, Staging_Beam_SecTag,  5)
ops.beamIntegration('Lobatto', Tank_Buttom_Beam_IntTag, Tank_Buttom_Beam_SecTag, 5)

# ─────────────────────────────────────────────────────────────────────────────
# 7.  DISTRIBUTED MASS (N·s²/mm² = t/mm)
# ─────────────────────────────────────────────────────────────────────────────
Col_mpul     = gamma_conc * (450. * 450.) / g    # t/mm for 450×450 column
Staging_Beam_mpul = gamma_conc * (350. * 500.) / g    # t/mm for 350×500 beam
Tank_Buttom_Beam_mpul = gamma_conc * ((900*250)+(350*250))/g    # t/mm for bf=900 bw=350 hf=250 hw=250mm

# ─────────────────────────────────────────────────────────────────────────────
# 8.  ELEMENTS  (explicit, each element defined individually)
# ─────────────────────────────────────────────────────────────────────────────

# ────────────────────────────────────────────────────────────────────────────
# (A) COLUMNS  —  4 columns × 7 stories = 28 elements
#     Element tag 1..28
#     forceBeamColumn: eleTag, nodeI, nodeJ, transfTag, integTag
# ─── Story 1 (floor0 → floor1) ───────────────────────────────────────────────
ops.element('forceBeamColumn',  111,  1, 11, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)  # col0
ops.element('forceBeamColumn',  212,  2, 12, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)  # col1
ops.element('forceBeamColumn',  313,  3, 13, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)  # col2
ops.element('forceBeamColumn',  414,  4, 14, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)  # col3

# ─── Story 2 (floor1 → floor2) ───────────────────────────────────────────────
ops.element('forceBeamColumn',  1121, 11, 21, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn',  1222, 12, 22, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn',  1323, 13, 23, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn',  1424, 14, 24, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# ─── Story 3 (floor2 → floor3) ───────────────────────────────────────────────
ops.element('forceBeamColumn',  2131, 21, 31, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn',  2232, 22, 32, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn',  2333, 23, 33, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn',  2434, 24, 34, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# ─── Story 4 (floor3 → floor4) ───────────────────────────────────────────────
ops.element('forceBeamColumn', 3141, 31, 41, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 3242, 32, 42, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 3343, 33, 43, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 3444, 34, 44, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# ─── Story 5 (floor4 → floor5) ───────────────────────────────────────────────
ops.element('forceBeamColumn', 4151, 41, 51, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 4252, 42, 52, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 4353, 43, 53, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 4454, 44, 54, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# ─── Story 6 (floor5 → floor6) ───────────────────────────────────────────────
ops.element('forceBeamColumn', 5161, 51, 61, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 5262, 52, 62, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 5363, 53, 63, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 5464, 54, 64, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# ─── Story 7 (floor6 → floor7) ─────────────────────────────────────────
ops.element('forceBeamColumn', 6171, 61, 71, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 6272, 62, 72, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 6373, 63, 73, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 6474, 64, 74, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# ─── Story 8 (floor7 → roof) ─────────────────────────────────────────
ops.element('forceBeamColumn', 7181, 71, 81, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 7282, 72, 82, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 7383, 73, 83, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 7484, 74, 84, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)



# --------------------------------------------------------------------------------
# Column Element Tag Lists
# --------------------------------------------------------------------------------

all_columns = [
    111, 212, 313, 414,
    1121, 1222,1323, 1424,
    2131, 2232,2333, 2434,
    3141, 3242,3343, 3444,
    4151, 4252,4353, 4454,
    5161, 5262,5363, 5464,
    6171, 6272,6373, 6474,
    7181, 7282,7383, 7484]   






# ────────────────────────────────────────────────────────────────────────────
# (B) BRACING BEAMS(staging)  —  4 beams/floor × 6 floors = 24 elements
#     Element tags 29..52
#     X-beams: col0↔col1 (south edge), col3↔col2 (north edge)
#     Y-beams: col1↔col2 (east edge),  col0↔col3 (west edge)
#
# ─── Floor 1 ─────────────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 1112, 11, 12, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)  # X south
ops.element('forceBeamColumn', 1413, 14, 13, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)  # X north
ops.element('forceBeamColumn', 1213, 12, 13, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)  # Y east
ops.element('forceBeamColumn', 1114, 11, 14, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)  # Y west

# ─── Floor 2 ─────────────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 2122, 21, 22, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 2423, 24, 23, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 2223, 22, 23, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 2124, 21, 24, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)

# ─── Floor 3 ─────────────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 3132, 31, 32, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 3433, 34, 33, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 3233, 32, 33, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 3134, 31, 34, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)

# ─── Floor 4 ─────────────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 4142, 41, 42, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 4443, 44, 43, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 4243, 42, 43, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 4144, 41, 44, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)

# ─── Floor 5 ─────────────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 5152, 51, 52, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 5453, 54, 53, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 5253, 52, 53, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 5154, 51, 54, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)

# ─── Floor 6 ─────────────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 6162, 61, 62, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 6463, 64, 63, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 6263, 62, 63, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 6164, 61, 64, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)

# ─── Floor 7 ─────────────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 7172, 71, 72, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 7473, 74, 73, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 7273, 72, 73, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 7174, 71, 74, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)

# --------------------------------------------------------------------------------
# Beam Element Tag Lists
# --------------------------------------------------------------------------------

staging_beams = [
    1112, 1413, 1213, 1114,
    2122, 2423, 2223, 2124,
    3132, 3433, 3233, 3134,
    4142, 4443, 4243, 4144,
    5152, 5453, 5253, 5154,
    6162, 6463, 6263, 6164,
    7172, 7473, 7273, 7174
]


# ────────────────────────────────────────────────────────────────────────────
# (B) Tank_Buttom_Beam  —  4 beams/floor × 1 floors = 4 elements
#     Element tags 53, 54, 55, 56
#     X-beams: col0↔col1 (south edge), col3↔col2 (north edge)
#     Y-beams: col1↔col2 (east edge),  col0↔col3 (west edge)

# ─── Floor 7 (roof) ──────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 8182, 81, 82, Tank_Buttom_Beam_X_TransfTag, Tank_Buttom_Beam_IntTag, '-mass', Tank_Buttom_Beam_mpul)
ops.element('forceBeamColumn', 8483, 84, 83, Tank_Buttom_Beam_X_TransfTag, Tank_Buttom_Beam_IntTag, '-mass', Tank_Buttom_Beam_mpul)
ops.element('forceBeamColumn', 8283, 82, 83, Tank_Buttom_Beam_Y_TransfTag, Tank_Buttom_Beam_IntTag, '-mass', Tank_Buttom_Beam_mpul)
ops.element('forceBeamColumn', 8184, 81, 84, Tank_Buttom_Beam_Y_TransfTag, Tank_Buttom_Beam_IntTag, '-mass', Tank_Buttom_Beam_mpul)

# --------------------------------------------------------------------------------
# Beam Element Tag List for Tank Bottom Beams
# --------------------------------------------------------------------------------

tank_bottom_beams = [8182, 8483, 8283, 8184]


all_beams = staging_beams + tank_bottom_beams




# --------------------------------------------------------------------------------
# Gravity loads
# --------------------------------------------------------------------------------

mass_empty_tank =60655.5 * kg          # Mass of tank in Ns2/mm
mass_impulsive_water = 34626.3 * kg     # Mass of impulsive water in Ns2/mm
mass_convective_water = 61293.9 * kg    # Mass of convective water in Ns2/mm

staging_beam_self_weight = Staging_Beam_mpul * g             # Staging Beam Self Weight N / mm
tank_bottom_beam_self_weight = Tank_Buttom_Beam_mpul * g     # Tank Buttom Beam Self Weight N / mm
Col_self_weight = Col_mpul * g                               # Column Self Weight N/mm

# print(Col_self_weight, tank_bottom_beam_self_weight, staging_beam_self_weight)

# --------------------------------------------------------------------------------
# Nodal Mass Distribution; mass(nodeTag, *massValues)
# --------------------------------------------------------------------------------

ops.mass(9001, mass_empty_tank + mass_impulsive_water, mass_empty_tank + mass_impulsive_water, 0.0, 0.0, 0.0, 0.0)
ops.mass(9003, mass_convective_water, mass_convective_water, 0.0, 0.0, 0.0, 0.0)

# --------------------------------------------------------------------------------
# Application Of UDL in local coordinate axes # eleLoad('-ele', *eleTags, '-range', eleTag1, eleTag2, '-type', '-beamUniform', Wy, <Wz>, Wx=0.0, '-beamPoint', Py, <Pz>, xL, Px=0.0, '-beamThermal', *tempPts)
# --------------------------------------------------------------------------------
ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)

def UDL_applier():
    # UDL Application on Beams
    ops.eleLoad('-ele', *staging_beams, '-type', '-beamUniform', 0.0, -staging_beam_self_weight, 0.0)
    ops.eleLoad('-ele', *tank_bottom_beams, '-type', '-beamUniform', 0.0, -tank_bottom_beam_self_weight, 0.0)

    # UDL Application on Columns
    ops.eleLoad('-ele', *all_columns, '-type', '-beamUniform', 0.0, 0.0, -Col_self_weight)



# --------------------------------------------------------------------------------
# Eigenvalue Analysis 
# --------------------------------------------------------------------------------
numModes = 5
lambdas = ops.eigen(numModes)  # returns a list of eigenvalues
# print(lambdas)

omega = []
frequencies = []
periods = []

for lam in lambdas:
    sqrt_lam = lam ** 0.5
    omega.append(sqrt_lam)
    frequencies.append(sqrt_lam / (2 * np.pi))
    periods.append((2 * np.pi) / sqrt_lam)

print("Initial Time Periods:", [f"{p:.10f}" for p in periods])

UDL_applier()

def Plotter():
    opsv.plot_model(node_labels = 0, element_labels = 0)     # 1 to see, 0 to hide
    plt.title("3D Model")

    # opsv.plot_load(nep=10, sfac= 500, node_supports=True)
    # plt.title("UDL applied")

    # Format all text labels to 2 decimal places
    for text in plt.gca().texts:
        try:
            value = float(text.get_text())
            text.set_text(f"{value:.2f}")
        except ValueError:
            pass  # Skip if not a number

    plt.show()
# Fix for opsvis
ops.getNDM = lambda: [3]
ops.getFixedNodes = lambda: []
Plotter()




# --------------------------------------------------------------------------------
# Gravity Analysis 
# --------------------------------------------------------------------------------
if rigidDiaphragm == 1:
    ops.constraints('Transformation')
else:
    ops.constraints('Plain')

ops.numberer('RCM')
ops.system('BandGen')
ops.test('NormDispIncr', 1e-8, 10)
ops.algorithm('Newton')
ops.integrator('LoadControl', 0.001)
ops.analysis('Static')

ops.analyze(1)

ops.loadConst('-time', 0.0)  # Set the time to zero an hold the loads constant

# --------------------------------------------------------------------------------
# Plotting Mode Shapes and Deformed Shape
# --------------------------------------------------------------------------------
def ModeShapesPlot():
    # opsv.plot_defo()
    # plt.title("Deformed Shape")

    opsv.plot_mode_shape(1)
    plt.title("Mode 1")

    opsv.plot_mode_shape(2)
    plt.title("Mode 2")

    opsv.plot_mode_shape(3)
    plt.title("Mode 3")

    opsv.plot_mode_shape(4)
    plt.title("Mode 4")

    opsv.plot_mode_shape(5)
    plt.title("Mode 5")

    plt.show()

# ModeShapesPlot()



import csv
import os

# Define CSV file path
csv_file = f"C:\\Openseespy\\GM\\D\\results_bare.csv"

file_exists = os.path.isfile(csv_file)

# --------------------------------------------------------------
# Ground Motion
# --------------------------------------------------------------

GM_RSN = 5676

pga = 0.35

original_pga_data = {
    5676: 0.36297,
    5259: 0.34798,
    4199: 0.29655,
    3282: 0.32222,
    2510: 0.33066,
    2476: 0.36627,
    334:  0.28209
}

original_pga = original_pga_data[GM_RSN]
factor = (pga * 9810) / original_pga

direction = 1

print("=====================================================")
if direction == 1:
    print("Time History Analysis in X Direction...")
elif direction == 2:
    print("Time History Analysis in Y Direction...")
else:
    print("ERROR Direction")

GM_input_file = f"C:\\Openseespy\\GM\\D\\RSN_{GM_RSN}.txt"

load_factors = []

with open(GM_input_file, "r") as f:
    lines = f.readlines()

for line in lines:
    if "Time Step" in line:
        dt = float(line.strip().split(":")[1].split()[0])
        break

data_start_index = next(i for i, line in enumerate(lines) if "Time(sec)" in line) + 1

for line in lines[data_start_index:]:
    if line.strip():
        parts = line.strip().split()
        if len(parts) >= 2:
            acc = float(parts[1])
            load_factors.append(acc)

tFinal = dt * len(load_factors)
print(f"RSN: {GM_RSN}, PGA: {pga}, g: {factor}, dt: {dt}, tFinal: {tFinal:.7f}, nPts: {len(load_factors)}")

# --------------------------------------------------------------
# Model
# --------------------------------------------------------------

print("Gravity Analysis Done.")

def EigenValues(nModes):
    lambdas = ops.eigen(nModes)

    omega = []
    frequencies = []
    periods = []

    for lam in lambdas:
        sqrt_lam = lam ** 0.5
        omega.append(sqrt_lam)
        frequencies.append(sqrt_lam / (2 * np.pi))
        periods.append(round(((2 * np.pi) / sqrt_lam), 5))

    return periods



# --------------------------------------------------------------
# RAYLEIGH DAMPING
# Apply 5% damping ONLY to:
#   • staging
#   • impulsive mass
#
# Apply 0.5% damping to:
#   • sloshing mode using viscous dashpot
# --------------------------------------------------------------

xDamp = 0.05

MpropSwitch = 1
KcurrSwitch = 0.0
KcommSwitch = 1.0
KinitSwitch = 0.0

# IMPORTANT:
# Mode 1 and 2 = usually sloshing mode
# Use higher modes for impulsive/staging damping

nEigenI = 3
nEigenJ = 4

lambdaN = ops.eigen(nEigenJ)

lambdaI = lambdaN[nEigenI - 1]
lambdaJ = lambdaN[nEigenJ - 1]

omegaI = lambdaI ** 0.5
omegaJ = lambdaJ ** 0.5

alphaM    = MpropSwitch * xDamp * (2 * omegaI * omegaJ) / (omegaI + omegaJ)
betaKcurr = KcurrSwitch * 2.0 * xDamp / (omegaI + omegaJ)
betaKcomm = KcommSwitch * 2.0 * xDamp / (omegaI + omegaJ)
betaKinit = KinitSwitch * 2.0 * xDamp / (omegaI + omegaJ)

# --------------------------------------------------------------
# APPLY RAYLEIGH DAMPING ONLY TO STAGING + IMPULSIVE SYSTEM
# --------------------------------------------------------------

staging_region_elements = all_columns + all_beams

ops.region(
    1,
    '-ele', *staging_region_elements,
    '-node', 9001,
    '-rayleigh',
    alphaM,
    betaKcurr,
    betaKinit,
    betaKcomm
)

# --------------------------------------------------------------
# 0.5% SLOSHING DAMPING USING VISCOUS DASHPOT
# --------------------------------------------------------------

xi_sloshing = 0.005

# kc = spring stiffness already defined above
kc = Kc

# mc = convective mass already defined above
mc = mass_convective_water

# dashpot coefficient
c_sloshing = 2.0 * xi_sloshing * (kc * mc) ** 0.5

# viscous material
ops.uniaxialMaterial(
    'Viscous',
    7001,
    c_sloshing,
    1.0
)

# dashpot element between convective nodes
# dir 1 = X direction
# dir 2 = Y direction

ops.element(
    'zeroLength',
    7002,
    9002,
    9003,
    '-mat', 7001, 7001,
    '-dir', 1, 2
)

# --------------------------------------------------------------
# IDR setup — 8 stories matching the gravity model
# --------------------------------------------------------------
#
#  Master nodes by elevation:
#    1001 → Z =     0  (base,   fixed)
#    1002 → Z =  4000  (floor 1)
#    1003 → Z =  7500  (floor 2)
#    1004 → Z = 11000  (floor 3)
#    1005 → Z = 14500  (floor 4)
#    1006 → Z = 18000  (floor 5)
#    1007 → Z = 21500  (floor 6)
#    1008 → Z = 25000  (floor 7)
#    1009 → Z = 28425  (roof)
#
#  Story heights (mm):
#    Story 1:  4000 - 0     = 4000
#    Story 2:  7500 - 4000  = 3500
#    Story 3: 11000 - 7500  = 3500
#    Story 4: 14500 - 11000 = 3500
#    Story 5: 18000 - 14500 = 3500
#    Story 6: 21500 - 18000 = 3500
#    Story 7: 25000 - 21500 = 3500
#    Story 8: 28425 - 25000 = 3425

NStories = 8   # was NBayZ = 4

nodes_for_IDR = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009]  # 9 master nodes

story_heights = [4000, 3500, 3500, 3500, 3500, 3500, 3500, 3425]        # mm, one per story

# --------------------------------------------------------------
# Analysis
# --------------------------------------------------------------

ops.wipeAnalysis()


ops.timeSeries('Path', 200, '-dt', dt, '-values', *load_factors, '-factor', factor)
ops.pattern('UniformExcitation', 200, direction, '-accel', 200)

ops.constraints('Transformation')
ops.test('EnergyIncr', 5.0e-4, 50)
ops.algorithm('Newton')
ops.numberer('RCM')
ops.system('BandGen')
ops.integrator('Newmark', 0.5, 0.25)
ops.analysis('Transient')

control_node = 1009   # master node at roof

tCurrent = ops.getTime()
ok = 0

time = []
baseshear = []
control_node_disp = []
drifts_all_floors = [[] for _ in range(NStories)]   # 8 stories

while ok == 0 and tCurrent < tFinal:
    ok = ops.analyze(1, dt)

    if ok != 0:
        print("regular newton failed ... trying ModifiedNewton...")
        ops.test('NormDispIncr', 5.0e-4, 100, 0)
        ops.algorithm('ModifiedNewton')
        ok = ops.analyze(1, 0.0005)
        if ok == 0:
            ops.test('EnergyIncr', 5.0e-4, 50)
            ops.algorithm('Newton')
        else:
            ops.algorithm('Broyden')
            ok = ops.analyze(1, .0001)
        if ok == 0:
            ops.algorithm('Newton')
        else:
            ops.algorithm('NewtonLineSearch')
            ok = ops.analyze(1, .0001)
        if ok == 0:
            ops.algorithm('Newton')
        else:
            ops.algorithm('KrylovNewton')
            ok = ops.analyze(1, .0001)
        if ok == 0:
            ops.algorithm('Newton')
        else:
            print('Analysis Not Successful..')

    tCurrent = ops.getTime()
    time.append(tCurrent)
    ops.reactions()
    basereac = sum(ops.nodeReaction(n, direction) for n in base_nodes)
    baseshear.append(basereac / 1000)
    control_node_disp.append(ops.nodeDisp(control_node, direction))

    for s in range(NStories):
        base_node = nodes_for_IDR[s]
        top_node  = nodes_for_IDR[s + 1]
        base_disp = ops.nodeDisp(base_node, direction)
        top_disp  = ops.nodeDisp(top_node,  direction)
        drift = abs(top_disp - base_disp) / story_heights[s]   # drift ratio
        drifts_all_floors[s].append(drift)

# --------------------------------------------------------------
# Post-processing
# --------------------------------------------------------------

Final_TimePeriods = EigenValues(5)
print("Final Time Periods: ", [f"{p:.10f}" for p in Final_TimePeriods])

max_base_shear = max(np.abs(baseshear))
print(f"Maximum Induced Base Shear = {max_base_shear:.4f} kN")

max_control_node_disp = max(np.abs(control_node_disp))
print(f"Maximum Top Displacement = {max_control_node_disp:.4f} mm")

MIDRs = [max(drifts) for drifts in drifts_all_floors]

for i in range(NStories):
    print(f'MIDR for Story {i+1} = {MIDRs[i] * 100:.4f} %')

MIDRall = max(MIDRs)
print(f'MIDR ALL = {MIDRall * 100:.4f} %')

# --------------------------------------------------------------
# CSV output — expanded to 8 stories
# --------------------------------------------------------------

with open(csv_file, 'a', newline='') as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow([
            'RSN', 'PGA (g)',
            'MIDR Story 1 (%)', 'MIDR Story 2 (%)', 'MIDR Story 3 (%)',
            'MIDR Story 4 (%)', 'MIDR Story 5 (%)', 'MIDR Story 6 (%)',
            'MIDR Story 7 (%)', 'MIDR Story 8 (%)',
            'MIDR ALL (%)'
        ])

    writer.writerow([
        GM_RSN, pga,
        *[f"{MIDRs[i] * 100:.5f}" for i in range(NStories)],
        f"{MIDRall * 100:.5f}"
    ])

ops.loadConst('-time', 0.0)
ops.remove('recorders')