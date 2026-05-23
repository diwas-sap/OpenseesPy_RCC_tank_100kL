
from Section import *

# --------------------------------------------------------------------------------
# Rigid Link and Elastic Link Elements  # rigidLink(type, rNodeTag, cNodeTag)
# --------------------------------------------------------------------------------

ops.rigidLink('beam', 1009, 9001)
ops.rigidLink('beam', 1009, 9002)
ops.element('zeroLength', 90029003, 9002, 9003, '-mat', parallel_material_tag, parallel_material_tag, '-dir', 1, 2, '-doRayleigh', 0)

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
# ops.element('forceBeamColumn', 8182, 81, 82, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
# ops.element('forceBeamColumn', 8483, 84, 83, Staging_Beam_X_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
# ops.element('forceBeamColumn', 8283, 82, 83, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)
# ops.element('forceBeamColumn', 8184, 81, 84, Staging_Beam_Y_TransfTag, Staging_Beam_IntTag, '-mass', Staging_Beam_mpul)

# --------------------------------------------------------------------------------
# Beam Element Tag List for Tank Bottom Beams
# --------------------------------------------------------------------------------

tank_bottom_beams = [8182, 8483, 8283, 8184]


all_beams = staging_beams + tank_bottom_beams

all_elements = all_columns + all_beams



