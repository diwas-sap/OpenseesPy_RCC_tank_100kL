from model_bare import *

# --------------------------------------------------------------------------------
# Gravity Analysis 
# --------------------------------------------------------------------------------
# ------------------------------------------------
# Gravity Analysis
# ------------------------------------------------

if rigidDiaphragm == 1:
    ops.constraints('Transformation')
else:
    ops.constraints('Plain')

ops.numberer('RCM')

ops.system('UmfPack')

ops.test('NormDispIncr', 1e-5, 100)

ops.algorithm('NewtonLineSearch', 0.8)

NstepGravity = 20
DGravity = 1.0 / NstepGravity

ops.integrator('LoadControl', DGravity)

ops.analysis('Static')

ok = ops.analyze(NstepGravity)

if ok != 0:

    print("Gravity analysis failed... trying initial stiffness")

    ops.test('NormDispIncr', 1e-4, 200)

    ops.algorithm('ModifiedNewton', '-initial')

    ok = ops.analyze(NstepGravity)

    if ok != 0:
        print("Gravity analysis still failed")

else:
    print("Gravity analysis completed successfully")


ops.loadConst('-time', 0.0)  # Set the time to zero an hold the loads constant

ops.reactions()
total_Rz = 0.0
print("\n--- Vertical Reactions after Gravity Analysis ---")

for node in Base_nodes:   
    Rz = ops.nodeReaction(node, 3)  # DOF 3 = Z (vertical)
    total_Rz += Rz
    print(f"  Node {node}: Rz = {Rz/1000:+.4f} kN")

print(f"\n  Total Vertical Reaction = {total_Rz/1000:.4f} kN")

# --------------------------------------------------------------------------------
# Plotting Mode Shapes and Deformed Shape
# --------------------------------------------------------------------------------
def ModeShapesPlot():
    opsv.plot_defo()
    plt.title("Deformed Shape")

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