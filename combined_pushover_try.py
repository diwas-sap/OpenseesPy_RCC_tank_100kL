import openseespy.opensees as ops
import numpy as np
import matplotlib.pyplot as plt
import opsvis as opsv


ops.wipe()
ops.model('BasicBuilder', '-ndm', 3, '-ndf', 6)


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

# ── Floor 1  (Z = 4000) ──────────────────────────────────────────────────────
ops.node(11,    0.,    0.,  4000.)   # floor1, col0
ops.node(12, 3850.,    0.,  4000.)   # floor1, col1
ops.node(13, 3850., 3850.,  4000.)   # floor1, col2
ops.node(14,    0., 3850.,  4000.)   # floor1, col3

# ── Floor 2  (Z = 7500) ──────────────────────────────────────────────────────
ops.node(21,    0.,    0.,  7500.)   # floor2, col0
ops.node(22, 3850.,    0.,  7500.)   # floor2, col1
ops.node(23, 3850., 3850.,  7500.)   # floor2, col2
ops.node(24,    0., 3850.,  7500.)   # floor2, col3

# ── Floor 3  (Z = 11000) ─────────────────────────────────────────────────────
ops.node(31,    0.,    0., 11000.)   # floor3, col0
ops.node(32, 3850.,    0., 11000.)   # floor3, col1
ops.node(33, 3850., 3850., 11000.)   # floor3, col2
ops.node(34,    0., 3850., 11000.)   # floor3, col3

# ── Floor 4  (Z = 14500) ─────────────────────────────────────────────────────
ops.node(41,    0.,    0., 14500.)   # floor4, col0
ops.node(42, 3850.,    0., 14500.)   # floor4, col1
ops.node(43, 3850., 3850., 14500.)   # floor4, col2
ops.node(44,    0., 3850., 14500.)   # floor4, col3

# ── Floor 5  (Z = 18000) ─────────────────────────────────────────────────────
ops.node(51,    0.,    0., 18000.)   # floor5, col0
ops.node(52, 3850.,    0., 18000.)   # floor5, col1
ops.node(53, 3850., 3850., 18000.)   # floor5, col2
ops.node(54,    0., 3850., 18000.)   # floor5, col3

# ── Floor 6  (Z = 21500) ─────────────────────────────────────────────────────
ops.node(61,    0.,    0., 21500.)   # floor6, col0
ops.node(62, 3850.,    0., 21500.)   # floor6, col1
ops.node(63, 3850., 3850., 21500.)   # floor6, col2
ops.node(64,    0., 3850., 21500.)   # floor6, col3

# ── Floor 7  (roof, Z = 25000) ───────────────────────────────────────────────
ops.node(71,    0.,    0., 25000.)   # floor7, col0
ops.node(72, 3850.,    0., 25000.)   # floor7, col1
ops.node(73, 3850., 3850., 25000.)   # floor7, col2
ops.node(74,    0., 3850., 25000.)   # floor7, col3

# ── Tank nodes ────────────────────────────────────────────────────────────────
# he = 1238.9 mm  (impulsive CG above tank base)
# hc = 2756.2 mm  (convective CG above tank base)
ops.node(9000, 1925., 1925., 25000.)          # tank base centroid
ops.node(9001, 1925., 1925., 26238.9)         # impulsive node  (25000 + 1238.9)
ops.node(9002, 1925., 1925., 27756.2)         # convective X    (25000 + 2756.2)
ops.node(9003, 1925., 1925., 27756.2)         # convective Y    (co-located with 9002)

# ─────────────────────────────────────────────────────────────────────────────
# 4.  BOUNDARY CONDITIONS
# ─────────────────────────────────────────────────────────────────────────────
# Fixed column bases (floor 0)
ops.fix( 1, 1, 1, 1, 1, 1, 1)
ops.fix( 2, 1, 1, 1, 1, 1, 1)
ops.fix( 3, 1, 1, 1, 1, 1, 1)
ops.fix( 4, 1, 1, 1, 1, 1, 1)

# Convective node 9002: free in X only
ops.fix(9002, 0, 1, 1, 1, 1, 1)
# Convective node 9003: free in Y only
ops.fix(9003, 1, 0, 1, 1, 1, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 1.  MATERIAL CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
import math

gamma_conc    = 2.5e-5   # N/mm³
g             = 9.81e3   # mm/s²

unconfined_concrete_tag = 1
confined_concrete_tag   = 2
steel_tag               = 3
spring_X_tag            = 11
spring_Y_tag            = 12
rigid_mat_tag           = 10

fc     = -20.
Ec     = 5000 * (-fc)**0.5
Kfc    = 1.20
Kres   = 0.1
lam    = 0.1

fc1U   = fc
eps1U  = -0.002
fc2U   = Kres * fc1U
eps2U  = -0.02

fc1C   = Kfc * fc1U
eps1C  = max(eps1U * (1 + 5 * (Kfc - 1)), -0.006)
fc2C   = Kres * fc1C
eps2C  = 10 * eps1C

ftC    = -0.1 * fc1C
ftU    = -0.1 * fc1U
Ets    = ftU / 0.002

Fy_steel    = 415.
E0_steel    = 2.0e5
Bs          = 0.01
params_steel = [20, 0.925, 0.15]

ops.uniaxialMaterial('Concrete02', unconfined_concrete_tag, fc1U, eps1U, fc2U, eps2U, lam, ftU, Ets)
ops.uniaxialMaterial('Concrete02', confined_concrete_tag,   fc1C, eps1C, fc2C, eps2C, lam, ftC, Ets)
ops.uniaxialMaterial('Steel02',    steel_tag, Fy_steel, E0_steel, Bs, *params_steel)

Kc = 234.374   # N/mm
ops.uniaxialMaterial('Elastic', spring_X_tag,   Kc)
ops.uniaxialMaterial('Elastic', spring_Y_tag,   Kc)
ops.uniaxialMaterial('Elastic', rigid_mat_tag,  1.0e10)



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


# ─────────────────────────────────────────────────────────────────────────────
# 5.  GEOMETRIC TRANSFORMATIONS
# ─────────────────────────────────────────────────────────────────────────────
Staging_Beam_X_TransfTag = 1   # beams along X
Staging_Beam_Y_TransfTag = 2   # beams along Y
Tank_Buttom_Beam_X_TransfTag = 3   # beams along X
Tank_Buttom_Beam_Y_TransfTag = 4   # beams along Y
Col_TransfTag       = 5   # vertical columns
rigid_TransfTag     = 6   # rigid links & tank verticals

ops.geomTransf('PDelta', Col_TransfTag,       -1.,  0.,  1.)  # columns (Z-axis, vecxz=Y)
ops.geomTransf('Linear', Staging_Beam_X_TransfTag,  1., -1.,  0.)  # X-beams
ops.geomTransf('Linear', Staging_Beam_Y_TransfTag,  1.,  1.,  0.)  # Y-beams
ops.geomTransf('Linear', Tank_Buttom_Beam_X_TransfTag,  1., -1.,  0.)  # X-beams
ops.geomTransf('Linear', Tank_Buttom_Beam_Y_TransfTag,  1.,  1.,  0.)  # Y-beams
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
ops.element('forceBeamColumn',  1,  1, 11, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)  # col0
ops.element('forceBeamColumn',  2,  2, 12, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)  # col1
ops.element('forceBeamColumn',  3,  3, 13, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)  # col2
ops.element('forceBeamColumn',  4,  4, 14, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)  # col3

# ─── Story 2 (floor1 → floor2) ───────────────────────────────────────────────
ops.element('forceBeamColumn',  5, 11, 21, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn',  6, 12, 22, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn',  7, 13, 23, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn',  8, 14, 24, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# ─── Story 3 (floor2 → floor3) ───────────────────────────────────────────────
ops.element('forceBeamColumn',  9, 21, 31, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 10, 22, 32, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 11, 23, 33, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 12, 24, 34, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# ─── Story 4 (floor3 → floor4) ───────────────────────────────────────────────
ops.element('forceBeamColumn', 13, 31, 41, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 14, 32, 42, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 15, 33, 43, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 16, 34, 44, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# ─── Story 5 (floor4 → floor5) ───────────────────────────────────────────────
ops.element('forceBeamColumn', 17, 41, 51, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 18, 42, 52, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 19, 43, 53, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 20, 44, 54, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# ─── Story 6 (floor5 → floor6) ───────────────────────────────────────────────
ops.element('forceBeamColumn', 21, 51, 61, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 22, 52, 62, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 23, 53, 63, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 24, 54, 64, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# ─── Story 7 (floor6 → floor7/roof) ─────────────────────────────────────────
ops.element('forceBeamColumn', 25, 61, 71, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 26, 62, 72, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 27, 63, 73, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 28, 64, 74, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# ────────────────────────────────────────────────────────────────────────────
# (B) BRACING BEAMS(staging)  —  4 beams/floor × 6 floors = 24 elements
#     Element tags 29..52
#     X-beams: col0↔col1 (south edge), col3↔col2 (north edge)
#     Y-beams: col1↔col2 (east edge),  col0↔col3 (west edge)
#
# ─── Floor 1 ─────────────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 29, 11, 12, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)  # X south
ops.element('forceBeamColumn', 30, 14, 13, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)  # X north
ops.element('forceBeamColumn', 31, 12, 13, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)  # Y east
ops.element('forceBeamColumn', 32, 11, 14, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)  # Y west

# ─── Floor 2 ─────────────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 33, 21, 22, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 34, 24, 23, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 35, 22, 23, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 36, 21, 24, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)

# ─── Floor 3 ─────────────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 37, 31, 32, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 38, 34, 33, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 39, 32, 33, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 40, 31, 34, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)

# ─── Floor 4 ─────────────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 41, 41, 42, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 42, 44, 43, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 43, 42, 43, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 44, 41, 44, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)

# ─── Floor 5 ─────────────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 45, 51, 52, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 46, 54, 53, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 47, 52, 53, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 48, 51, 54, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)

# ─── Floor 6 ─────────────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 49, 61, 62, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 50, 64, 63, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 51, 62, 63, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
ops.element('forceBeamColumn', 52, 61, 64, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)

# ────────────────────────────────────────────────────────────────────────────
# (B) Tank_Buttom_Beam  —  4 beams/floor × 1 floors = 4 elements
#     Element tags 53, 54, 55, 56
#     X-beams: col0↔col1 (south edge), col3↔col2 (north edge)
#     Y-beams: col1↔col2 (east edge),  col0↔col3 (west edge)

# ─── Floor 7 (roof) ──────────────────────────────────────────────────────────
ops.element('forceBeamColumn', 53, 71, 72, Tank_Buttom_Beam_X_TransfTag, Tank_Buttom_Beam_IntTag, '-mass', Tank_Buttom_Beam_mpul)
ops.element('forceBeamColumn', 54, 74, 73, Tank_Buttom_Beam_X_TransfTag, Tank_Buttom_Beam_IntTag, '-mass', Tank_Buttom_Beam_mpul)
ops.element('forceBeamColumn', 55, 72, 73, Tank_Buttom_Beam_Y_TransfTag, Tank_Buttom_Beam_IntTag, '-mass', Tank_Buttom_Beam_mpul)
ops.element('forceBeamColumn', 56, 71, 74, Tank_Buttom_Beam_Y_TransfTag, Tank_Buttom_Beam_IntTag, '-mass', Tank_Buttom_Beam_mpul)

# ────────────────────────────────────────────────────────────────────────────
# (C) RIGID DIAPHRAGMS  —  equalDOF at each floor (X, Y, Rz coupled)
#     Master = col0 node at each floor; slaves = col1, col2, col3
# ─── Floor 1 ─────────────────────────────────────────────────────────────────
ops.equalDOF(11, 12, 1, 2, 6)
ops.equalDOF(11, 13, 1, 2, 6)
ops.equalDOF(11, 14, 1, 2, 6)

# ─── Floor 2 ─────────────────────────────────────────────────────────────────
ops.equalDOF(21, 22, 1, 2, 6)
ops.equalDOF(21, 23, 1, 2, 6)
ops.equalDOF(21, 24, 1, 2, 6)

# ─── Floor 3 ─────────────────────────────────────────────────────────────────
ops.equalDOF(31, 32, 1, 2, 6)
ops.equalDOF(31, 33, 1, 2, 6)
ops.equalDOF(31, 34, 1, 2, 6)

# ─── Floor 4 ─────────────────────────────────────────────────────────────────
ops.equalDOF(41, 42, 1, 2, 6)
ops.equalDOF(41, 43, 1, 2, 6)
ops.equalDOF(41, 44, 1, 2, 6)

# ─── Floor 5 ─────────────────────────────────────────────────────────────────
ops.equalDOF(51, 52, 1, 2, 6)
ops.equalDOF(51, 53, 1, 2, 6)
ops.equalDOF(51, 54, 1, 2, 6)

# ─── Floor 6 ─────────────────────────────────────────────────────────────────
ops.equalDOF(61, 62, 1, 2, 6)
ops.equalDOF(61, 63, 1, 2, 6)
ops.equalDOF(61, 64, 1, 2, 6)

# ─── Floor 7 (roof) ──────────────────────────────────────────────────────────
ops.equalDOF(71, 72, 1, 2, 6)
ops.equalDOF(71, 73, 1, 2, 6)
ops.equalDOF(71, 74, 1, 2, 6)

# ────────────────────────────────────────────────────────────────────────────
# (D) RIGID LINKS — roof column tops → tank base node 9000
#     Element tags 57..60
# ─────────────────────────────────────────────────────────────────────────────
E_r = 1.0e12;  A_r = 1.0e6;  I_r = 1.0e12;  G_r = 1.0e12;  J_r = 1.0e12

ops.element('elasticBeamColumn', 57, 71, 9000, A_r, E_r, G_r, J_r, I_r, I_r, rigid_TransfTag)  # col0→base
ops.element('elasticBeamColumn', 58, 72, 9000, A_r, E_r, G_r, J_r, I_r, I_r, rigid_TransfTag)  # col1→base
ops.element('elasticBeamColumn', 59, 73, 9000, A_r, E_r, G_r, J_r, I_r, I_r, rigid_TransfTag)  # col2→base
ops.element('elasticBeamColumn', 60, 74, 9000, A_r, E_r, G_r, J_r, I_r, I_r, rigid_TransfTag)  # col3→base

# ────────────────────────────────────────────────────────────────────────────
# (E) RIGID LINK: tank base → impulsive node
#     Element tag 61
# ─────────────────────────────────────────────────────────────────────────────
ops.element('elasticBeamColumn', 61, 9000, 9001, A_r, E_r, G_r, J_r, I_r, I_r, rigid_TransfTag)

# ────────────────────────────────────────────────────────────────────────────
# (F) CONVECTIVE SPRINGS: impulsive node 9001 → convective nodes
#     Element tag 62 (X-spring), 63 (Y-spring)
# ─────────────────────────────────────────────────────────────────────────────
ops.element('zeroLength', 62,
            9001, 9002,
            '-mat', spring_X_tag, rigid_mat_tag, rigid_mat_tag,
            '-dir', 1, 2, 3)   # spring in X, rigid in Y and Z

ops.element('zeroLength', 63,
            9001, 9003,
            '-mat', rigid_mat_tag, spring_Y_tag, rigid_mat_tag,
            '-dir', 1, 2, 3)   # rigid in X, spring in Y, rigid in Z


# ─────────────────────────────────────────────────────────────────────────────
# 9.  LUMPED MASSES AT TANK NODES
# ─────────────────────────────────────────────────────────────────────────────
# Convert kg → tonne (N·s²/mm)
Mc   = 61293.9 / 1000.   # t  convective liquid
Ms   = 60655.4 / 1000.   # t  impulsive liquid
Mc_  = 34626.3 / 1000.   # t  tank container

m_imp  = Ms + Mc_   # impulsive + container at node 9001
m_conv = Mc         # convective at nodes 9002 (X) and 9003 (Y)

ops.mass(9001,  m_imp,  m_imp,  m_imp,  0., 0., 0.)
ops.mass(9002, m_conv,     0.,     0.,  0., 0., 0.)   # X only
ops.mass(9003,     0., m_conv,     0.,  0., 0., 0.)   # Y only

# ─────────────────────────────────────────────────────────────────────────────
# 10.  GRAVITY ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
ops.system('BandGeneral')
ops.numberer('RCM')
ops.constraints('Transformation')
ops.integrator('LoadControl', 1.0 / 10)
ops.algorithm('Newton')
ops.analysis('Static')
ops.analyze(10)
ops.loadConst('-time', 0.0)
print("✓ Gravity analysis complete")

# ─────────────────────────────────────────────────────────────────────────────
# 11.  MODAL ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
n_modes    = 6
eigenvalues = ops.eigen(n_modes)
omega      = np.sqrt(np.array(eigenvalues))
freq       = omega / (2 * np.pi)
periods    = 1.0 / freq

print("\n═══════════════════════════════════════════")
print("  MODAL ANALYSIS RESULTS")
print("═══════════════════════════════════════════")
print(f"{'Mode':>5}  {'ω (rad/s)':>12}  {'f (Hz)':>10}  {'T (s)':>10}")
print("─" * 45)
for i in range(n_modes):
    print(f"  {i+1:>3}  {omega[i]:>12.4f}  {freq[i]:>10.4f}  {periods[i]:>10.4f}")
print("═══════════════════════════════════════════\n")

# ─────────────────────────────────────────────────────────────────────────────
# 12.  PLOT MODEL
# ─────────────────────────────────────────────────────────────────────────────
ops.getNDM        = lambda: [3]
ops.getFixedNodes = lambda: []

opsv.plot_model(node_labels=0, element_labels=0)
plt.title("3D Model — 7-Story Braced Frame (Explicit Coordinates)")
plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# 13.  PUSHOVER ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
#
#  Staging nodes only (col0 master node at each floor, Z = 4000 to 25000):
#    Floor 1 → node 11   (Z =  4000)
#    Floor 2 → node 21   (Z =  7500)
#    Floor 3 → node 31   (Z = 11000)
#    Floor 4 → node 41   (Z = 14500)
#    Floor 5 → node 51   (Z = 18000)
#    Floor 6 → node 61   (Z = 21500)
#    Floor 7 → node 71   (Z = 25000) 
#    impulsive lumped node  9001 ← control node 
#
#  Base nodes (for reaction summation):
#    nodes 1, 2, 3, 4  (Z = 0, all fixed)
#
#  Total staging height for drift: 25000 mm
# ─────────────────────────────────────────────────────────────────────────────

import csv

# ── Node lists ───────────────────────────────────────────────────────────────
master_nodes  = [11, 21, 31, 41, 51, 61, 71, 9002]   # col0 at each staging floor (lateral load targets)
floor_1_nodes = [1, 2, 3, 4]                    # fixed base nodes (reaction read-out)

# ── Pushover settings ────────────────────────────────────────────────────────
refLoad       = 1000.0   # N  (reference lateral load per floor node)
push_direction = 1       # 1 = X-direction, 2 = Y-direction
control_node  = 9002     # roof node (col0, floor 7) — displacement is tracked here
total_height  = 25000.   # mm  (total staging height, floor 0 → floor 7)

# ── Analysis parameters ──────────────────────────────────────────────────────
dU     = 0.05            # mm  per step displacement increment
maxDisp = 0.01 * total_height   # mm  = 4 % drift limit

# ─────────────────────────────────────────────────────────────────────────────

print("---------------------------")
print("Gravity Analysis Done.")
print("---------------------------")

ops.timeSeries('Linear', 11)
ops.pattern('Plain', 11, 11)

if push_direction == 2:
    print("Starting Pushover Analysis In Y Direction....")
    control_DOF = 2
elif push_direction == 1:
    print("Starting Pushover Analysis In X Direction....")
    control_DOF = 1
else:
    print("ERROR: Invalid Pushover Direction.")

# Apply uniform lateral load to every staging floor master node
if push_direction == 2:
    for tag in master_nodes:
        ops.load(tag, 0.0, refLoad, 0.0, 0.0, 0.0, 0.0)
else:
    for tag in master_nodes:
        ops.load(tag, refLoad, 0.0, 0.0, 0.0, 0.0, 0.0)

# ── Analysis objects ─────────────────────────────────────────────────────────
ops.system('BandGeneral')
ops.numberer('RCM')
ops.constraints('Transformation')
ops.test('NormDispIncr', 1.0e-6, 1000)
ops.algorithm('Newton')
ops.analysis('Static')

# integrator('DisplacementControl', nodeTag, dof, incr, numIter=1, dUmin=incr, dUmax=incr)
ops.integrator('DisplacementControl', control_node, control_DOF, dU, 1, dU, dU)

# ── Storage ──────────────────────────────────────────────────────────────────
controlNode_disp = []
base_shear       = []
ok               = 0
currentDisp      = 0.0
temp             = 1

# ── Step loop ────────────────────────────────────────────────────────────────
while ok == 0 and currentDisp < maxDisp:

    ok = ops.analyze(1)

    if ok != 0:
        print("Newton failed. Trying different algorithms...")
        algorithms = [
            ('ModifiedNewton', ['-initial']),
            ('NewtonLineSearch', []),
            ('KrylovNewton', []),
            ('BFGS', [])
        ]
        for alg, args in algorithms:
            ops.algorithm(alg, *args)
            if ops.analyze(1) == 0:
                print(f"Succeeded with {alg}. Back to regular Newton.")
                ok = 0
                break
        ops.algorithm('Newton')

    currentDisp = ops.nodeDisp(control_node, control_DOF)
    controlNode_disp.append(currentDisp)

    ops.reactions()
    bShear = 0.0
    for node in floor_1_nodes:
        bShear += -ops.nodeReaction(node, control_DOF)
    base_shear.append(bShear / 1.0e3)   # N → kN

    if temp % 20 == 0:
        print(f"Disp : Node {control_node} : {currentDisp:.3f} mm, "
              f"Base Shear : {(bShear / 1000):.3f} kN")
    temp += 1

# ── Summary ──────────────────────────────────────────────────────────────────
print(f"\nMaximum Base Shear = {max(base_shear):.2f} kN")
max_index = base_shear.index(max(base_shear))
disp_at_max_base_shear = controlNode_disp[max_index]
print(f"Displacement at Maximum Base Shear = {disp_at_max_base_shear:.2f} mm")
drift_at_max = (disp_at_max_base_shear / total_height) * 100
print(f"Drift at Maximum Base Shear = {drift_at_max:.2f} %")

drift = [(d / total_height) * 100 for d in controlNode_disp]

# ── CSV export ───────────────────────────────────────────────────────────────
csv_filename = "pushover_results.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Drift (%)", "Base Shear (kN)"])   # Header
    for d, bs in zip(drift, base_shear):
        writer.writerow([d, bs])
print(f"\n✓ Results written to {csv_filename}")

# ── Pushover curve ───────────────────────────────────────────────────────────
plt.figure()
plt.plot(drift, base_shear, label='Control Node (roof, node 71)')
plt.title("Pushover Curve — Water Tank Staging Structure")
plt.xlabel("Drift (%)")
plt.xlim(-0.05, 4.05)
plt.ylim(-5, 1.1 * max(base_shear))
plt.ylabel("Base Shear (kN)")
plt.tick_params(direction='in', top=True, right=True)
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()