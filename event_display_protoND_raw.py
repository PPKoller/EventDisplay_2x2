import math
import argparse
import numpy as np
import os
import tempfile
import ROOT



#### import the simple module from the paraview
from paraview.simple import *



#### load arguments
parser = argparse.ArgumentParser()
parser.add_argument("root_file")
parser.add_argument("-a", "--animation",    action='store_true',    help="See a 360 deg orbit animation.")
parser.add_argument("-c", "--color",        default="dq",           help="Select the tree entry to use as color. Default: %(default)s.")
parser.add_argument("-l", "--logscale",     action='store_true',    help="Show logarithmic scaled colorbar.")
parser.add_argument("-e", "--event",        default="0",            help="Select the event number. Default: %(default)s.",                       type=int)
parser.add_argument("-ND","--NearDetector", action='store_true',    help="Show DUNE-ND shape.")
parser.add_argument("-FD","--FarDetector",  action='store_true',    help="Show DUNE-FD shape.")
args = parser.parse_args()

if args.NearDetector:
    draw_ND = True
else:
    draw_ND = False

if args.FarDetector:
    draw_FD = True
else:
    draw_FD = False



#### read and store data
root_file = ROOT.TFile(args.root_file, "READ")
data = np.zeros(0)
try:
    tree = root_file.Get("argon")
    tree.SetBranchStatus("*", 1)

    for i in range(tree.GetEntries()):

        tree.GetEntry(i)

        if tree.ev != args.event:
            continue

        if "q" in args.color:
            data =  np.append(data,np.transpose(np.vstack((tree.xq, tree.yq, tree.zq, getattr(tree, args.color)))))
        else:
            data =  np.append(data,np.transpose(np.vstack((tree.xq, tree.yq, tree.zq, np.full(tree.nq, getattr(tree, args.color))))))

    data = np.reshape(data,(-1,4))

finally:
    root_file.Close()



#### load date into paraview
csv_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
try:
    np.savetxt(csv_file, data, delimiter=",", comments="", header="x,y,z,c")
    csv_file.close()
    pv_csv = CSVReader(FileName=[csv_file.name])

    data_table = TableToPoints(Input=pv_csv)
    data_table.XColumn = "x"
    data_table.YColumn = "z"
    data_table.ZColumn = "y"

    render_view = FindViewOrCreate("RenderView", viewtype="RenderView")
    SetActiveView(render_view)
    SetActiveSource(data_table)
    data_display = Show(data_table, render_view)

finally:
    os.remove(csv_file.name)



# Define coloring
#=================
ColorBy(data_display, ("POINTS", "c"))
data_display.RescaleTransferFunctionToDataRange(True, False)
data_display.SetScalarBarVisibility(render_view, True)
color_lut = GetColorTransferFunction("c")

if args.logscale:
    color_lut.UseLogScale = 1
else:
    color_lut.UseLogScale = 0

if args.color == "pidq":

    rgbPoints  = [-321,     000,    000,    255] # K-       Blue
    rgbPoints += [-211,     000,    255,    255] # Pi-      Cyan
    rgbPoints += [-13,      255,    000,    255] # Mu-      Fuchsia
    rgbPoints += [-11,      000,    255,    000] # e+       Lime
    rgbPoints += [ 11,      255,    215,    000] # e-       Gold
    rgbPoints += [ 13,      255,    000,    255] # Mu+      Fuchsia
    rgbPoints += [ 211,     000,    255,    255] # Pi+      Cyan
    rgbPoints += [ 321,     000,    000,    255] # K+       Blue
    rgbPoints += [ 2212,    255,    000,    000] # P        Red
    rgbPoints += [3123,     000,    000,    000] # Nuclei   Black

    #rgbPoints += [22.000,   200.0,  200.0,  200.0]
    #rgbPoints += [111.000,  0.0,    128.0,  128.0]
    #rgbPoints += [311.000,  128.0,  0.0,    128.0]

    color_lut.RGBPoints = rgbPoints

    # Properties modified on scalarsLUT
    color_lut.LockDataRange = 1

    # Properties modified on scalarsLUT
    color_lut.Discretize = 1

    # Properties modified on scalarsLUT
    color_lut.NumberOfTableValues = 10000

else:
    color_lut.ApplyPreset('jet', True)
    #color_lut.ApplyPreset('Grayscale', True)



# Display settings
#==================
# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# uncomment following to set a specific view size
renderView1.ViewSize = [1920, 1080]

# Properties modified on renderView1
renderView1.Background = [0.4, 0.4, 0.4]



# Draw ArgonCube modules
#========================
cube = []

modules = range(4)

for i in modules:
    # create a new 'Box'
    cube.append(Box())

    # Properties modified on cube
    cube[-1].XLength = 70.0
    cube[-1].YLength = 70.0
    cube[-1].ZLength = 140.0
    cube[-1].Center = [-35.+float(i)%2.*70., -35.+math.floor(float(i)/2.)*70., 0.]

    # show data in view
    acubeDisplay = Show(cube[-1], renderView1)
    # trace defaults for the display properties.
    acubeDisplay.Representation = 'Wireframe'
    acubeDisplay.ColorArrayName = [None, '']
    acubeDisplay.OSPRayScaleArray = 'Normals'
    acubeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    acubeDisplay.SelectOrientationVectors = 'None'
    acubeDisplay.ScaleFactor = 30.0
    acubeDisplay.SelectScaleArray = 'None'
    acubeDisplay.GlyphType = 'Arrow'
    acubeDisplay.GlyphTableIndexArray = 'None'
    acubeDisplay.DataAxesGrid = 'GridAxesRepresentation'
    acubeDisplay.PolarAxes = 'PolarAxesRepresentation'
    acubeDisplay.GaussianRadius = 15.0
    acubeDisplay.SetScaleArray = [None, '']
    acubeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    acubeDisplay.OpacityArray = [None, '']
    acubeDisplay.OpacityTransferFunction = 'PiecewiseFunction'

    # Properties modified on acubeDisplay
    #acubeDisplay.AmbientColor = [0.0, 0.666666666666, 0.0]
    acubeDisplay.AmbientColor = [1.0, 1.0, 1.0]



# Draw ArgonCube TPCs
#=====================
modules = range(8)

for i in modules:
    # create a new 'Box'
    cube.append(Box())

    # Properties modified on cube
    cube[-1].XLength = 33.0
    cube[-1].YLength = 68.0
    cube[-1].ZLength = 138.0
    cube[-1].Center = [-52.5+float(i)%4.*35., -35.+math.floor(float(i)/4.)*70., 0.]

    # show data in view
    acubeDisplay = Show(cube[-1], renderView1)
    # trace defaults for the display properties.
    acubeDisplay.Representation = 'Surface'
    acubeDisplay.ColorArrayName = [None, '']
    acubeDisplay.OSPRayScaleArray = 'Normals'
    acubeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    acubeDisplay.SelectOrientationVectors = 'None'
    acubeDisplay.ScaleFactor = 30.0
    acubeDisplay.SelectScaleArray = 'None'
    acubeDisplay.GlyphType = 'Arrow'
    acubeDisplay.GlyphTableIndexArray = 'None'
    acubeDisplay.DataAxesGrid = 'GridAxesRepresentation'
    acubeDisplay.PolarAxes = 'PolarAxesRepresentation'
    acubeDisplay.GaussianRadius = 15.0
    acubeDisplay.SetScaleArray = [None, '']
    acubeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    acubeDisplay.OpacityArray = [None, '']
    acubeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    acubeDisplay.Opacity = 0.2

    # Properties modified on acubeDisplay
    #acubeDisplay.AmbientColor = [0.0, 0.666666666666, 0.0]
    acubeDisplay.AmbientColor = [1.0, 1.0, 1.0]



# Draw 2x2 inner Cryostat
#=========================
cryo = []

if False:
    # create a new 'Cylinder'
    cryo.append(Cylinder())

    # Properties modified on cylinder1
    cryo[-1].Resolution = 1000
    cryo[-1].Height = 140.0
    cryo[-1].Radius = 94.0

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    # uncomment following to set a specific view size
    # renderView1.ViewSize = [1191, 810]

    # show data in view
    acubeDisplay = Show(cryo[-1], renderView1)
    # trace defaults for the display properties.
    acubeDisplay.Representation = 'Wireframe'
    acubeDisplay.ColorArrayName = [None, '']
    acubeDisplay.OSPRayScaleArray = 'Normals'
    acubeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    acubeDisplay.SelectOrientationVectors = 'None'
    acubeDisplay.ScaleFactor = 396.0
    acubeDisplay.SelectScaleArray = 'None'
    acubeDisplay.GlyphType = 'Arrow'
    acubeDisplay.GlyphTableIndexArray = 'None'
    acubeDisplay.DataAxesGrid = 'GridAxesRepresentation'
    acubeDisplay.PolarAxes = 'PolarAxesRepresentation'
    acubeDisplay.GaussianRadius = 198.0
    acubeDisplay.SetScaleArray = [None, '']
    acubeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    acubeDisplay.OpacityArray = [None, '']
    acubeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    acubeDisplay.Opacity = 0.2

    # Properties modified on acubeDisplay
    #acubeDisplay.AmbientColor = [0.0, 0.666666666666, 0.0]
    acubeDisplay.AmbientColor = [1.0, 1.0, 1.0]



# Draw Tracker Modules
#======================
for i in range(12):
    # create a new 'Box'
    cube.append(Box())

    # Properties modified on cube
    cube[-1].XLength = 140.0
    cube[-1].YLength = 4.0
    cube[-1].ZLength = 140.0
#    cube[-1].Center = [0.,107.5+10.5+float(i)*4., 0.]
    cube[-1].Center = [0.,117.5+float(i)*4., 0.]

    # show data in view
    acubeDisplay = Show(cube[-1], renderView1)
    # trace defaults for the display properties.
    acubeDisplay.Representation = 'Surface'
    acubeDisplay.ColorArrayName = [None, '']
    acubeDisplay.OSPRayScaleArray = 'Normals'
    acubeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    acubeDisplay.SelectOrientationVectors = 'None'
    acubeDisplay.ScaleFactor = 30.0
    acubeDisplay.SelectScaleArray = 'None'
    acubeDisplay.GlyphType = 'Arrow'
    acubeDisplay.GlyphTableIndexArray = 'None'
    acubeDisplay.DataAxesGrid = 'GridAxesRepresentation'
    acubeDisplay.PolarAxes = 'PolarAxesRepresentation'
    acubeDisplay.GaussianRadius = 15.0
    acubeDisplay.SetScaleArray = [None, '']
    acubeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    acubeDisplay.OpacityArray = [None, '']
    acubeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    acubeDisplay.Opacity = 0.2

    # Properties modified on acubeDisplay
    #acubeDisplay.AmbientColor = [0.0, 0.666666666666, 0.0]
    acubeDisplay.AmbientColor = [1.0, 1.0, 1.0]



# Draw ECal Modules
#======================
for i in range(20):
    # create a new 'Box'
    cube.append(Box())

    # Properties modified on cube
    cube[-1].XLength = 140.0
    cube[-1].YLength = 0.2
    cube[-1].ZLength = 140.0
    cube[-1].Center = [0.,163.6+float(i)*2.2, 0.]

    # show data in view
    acubeDisplay = Show(cube[-1], renderView1)
    # trace defaults for the display properties.
    acubeDisplay.Representation = 'Surface'
    acubeDisplay.ColorArrayName = [None, '']
    acubeDisplay.OSPRayScaleArray = 'Normals'
    acubeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    acubeDisplay.SelectOrientationVectors = 'None'
    acubeDisplay.ScaleFactor = 30.0
    acubeDisplay.SelectScaleArray = 'None'
    acubeDisplay.GlyphType = 'Arrow'
    acubeDisplay.GlyphTableIndexArray = 'None'
    acubeDisplay.DataAxesGrid = 'GridAxesRepresentation'
    acubeDisplay.PolarAxes = 'PolarAxesRepresentation'
    acubeDisplay.GaussianRadius = 15.0
    acubeDisplay.SetScaleArray = [None, '']
    acubeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    acubeDisplay.OpacityArray = [None, '']
    acubeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    acubeDisplay.Opacity = 0.5

    # Properties modified on acubeDisplay
    #acubeDisplay.AmbientColor = [0.0, 0.666666666666, 0.0]
    acubeDisplay.AmbientColor = [1.0, 1.0, 1.0]

for i in range(20):
    # create a new 'Box'
    cube.append(Box())

    # Properties modified on cube
    cube[-1].XLength = 140.0
    cube[-1].YLength = 2.0
    cube[-1].ZLength = 140.0
    cube[-1].Center = [0.,164.7+float(i)*2.2, 0.]

    # show data in view
    acubeDisplay = Show(cube[-1], renderView1)
    # trace defaults for the display properties.
    acubeDisplay.Representation = 'Surface'
    acubeDisplay.ColorArrayName = [None, '']
    acubeDisplay.OSPRayScaleArray = 'Normals'
    acubeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    acubeDisplay.SelectOrientationVectors = 'None'
    acubeDisplay.ScaleFactor = 30.0
    acubeDisplay.SelectScaleArray = 'None'
    acubeDisplay.GlyphType = 'Arrow'
    acubeDisplay.GlyphTableIndexArray = 'None'
    acubeDisplay.DataAxesGrid = 'GridAxesRepresentation'
    acubeDisplay.PolarAxes = 'PolarAxesRepresentation'
    acubeDisplay.GaussianRadius = 15.0
    acubeDisplay.SetScaleArray = [None, '']
    acubeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    acubeDisplay.OpacityArray = [None, '']
    acubeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    acubeDisplay.Opacity = 0.2

    # Properties modified on acubeDisplay
    #acubeDisplay.AmbientColor = [0.0, 0.666666666666, 0.0]
    acubeDisplay.AmbientColor = [1.0, 1.0, 1.0]



# Draw HCal Modules
#======================
for i in range(20):
    # create a new 'Box'
    cube.append(Box())

    # Properties modified on cube
    cube[-1].XLength = 140.0
    cube[-1].YLength = 2.54
    cube[-1].ZLength = 140.0
    cube[-1].Center = [0.,208.77+float(i)*4.54, 0.]

    # show data in view
    acubeDisplay = Show(cube[-1], renderView1)
    # trace defaults for the display properties.
    acubeDisplay.Representation = 'Surface'
    acubeDisplay.ColorArrayName = [None, '']
    acubeDisplay.OSPRayScaleArray = 'Normals'
    acubeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    acubeDisplay.SelectOrientationVectors = 'None'
    acubeDisplay.ScaleFactor = 30.0
    acubeDisplay.SelectScaleArray = 'None'
    acubeDisplay.GlyphType = 'Arrow'
    acubeDisplay.GlyphTableIndexArray = 'None'
    acubeDisplay.DataAxesGrid = 'GridAxesRepresentation'
    acubeDisplay.PolarAxes = 'PolarAxesRepresentation'
    acubeDisplay.GaussianRadius = 15.0
    acubeDisplay.SetScaleArray = [None, '']
    acubeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    acubeDisplay.OpacityArray = [None, '']
    acubeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    acubeDisplay.Opacity = 0.5

    # Properties modified on acubeDisplay
    #acubeDisplay.AmbientColor = [0.0, 0.666666666666, 0.0]
    acubeDisplay.AmbientColor = [1.0, 1.0, 1.0]

for i in range(20):
    # create a new 'Box'
    cube.append(Box())

    # Properties modified on cube
    cube[-1].XLength = 140.0
    cube[-1].YLength = 2.0
    cube[-1].ZLength = 140.0
    cube[-1].Center = [0.,211.04+float(i)*4.54, 0.]

    # show data in view
    acubeDisplay = Show(cube[-1], renderView1)
    # trace defaults for the display properties.
    acubeDisplay.Representation = 'Surface'
    acubeDisplay.ColorArrayName = [None, '']
    acubeDisplay.OSPRayScaleArray = 'Normals'
    acubeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    acubeDisplay.SelectOrientationVectors = 'None'
    acubeDisplay.ScaleFactor = 30.0
    acubeDisplay.SelectScaleArray = 'None'
    acubeDisplay.GlyphType = 'Arrow'
    acubeDisplay.GlyphTableIndexArray = 'None'
    acubeDisplay.DataAxesGrid = 'GridAxesRepresentation'
    acubeDisplay.PolarAxes = 'PolarAxesRepresentation'
    acubeDisplay.GaussianRadius = 15.0
    acubeDisplay.SetScaleArray = [None, '']
    acubeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    acubeDisplay.OpacityArray = [None, '']
    acubeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    acubeDisplay.Opacity = 0.2

    # Properties modified on acubeDisplay
    #acubeDisplay.AmbientColor = [0.0, 0.666666666666, 0.0]
    acubeDisplay.AmbientColor = [1.0, 1.0, 1.0]



# Draw DUNE ND shape
#====================
if draw_ND:
    # create a new 'Box'
    cube.append(Box())

    # Properties modified on cube
    cube[-1].XLength = 700.0
    cube[-1].YLength = 500.0
    cube[-1].ZLength = 300.0
    cube[-1].Center = [0., 250.-70., 0.]

    # show data in view
    acubeDisplay = Show(cube[-1], renderView1)
    # trace defaults for the display properties.
    acubeDisplay.Representation = 'Wireframe'
    acubeDisplay.ColorArrayName = [None, '']
    acubeDisplay.OSPRayScaleArray = 'Normals'
    acubeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    acubeDisplay.SelectOrientationVectors = 'None'
    acubeDisplay.ScaleFactor = 30.0
    acubeDisplay.SelectScaleArray = 'None'
    acubeDisplay.GlyphType = 'Arrow'
    acubeDisplay.GlyphTableIndexArray = 'None'
    acubeDisplay.DataAxesGrid = 'GridAxesRepresentation'
    acubeDisplay.PolarAxes = 'PolarAxesRepresentation'
    acubeDisplay.GaussianRadius = 15.0
    acubeDisplay.SetScaleArray = [None, '']
    acubeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    acubeDisplay.OpacityArray = [None, '']
    acubeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    acubeDisplay.Opacity = 1.0

    # Properties modified on acubeDisplay
    #acubeDisplay.AmbientColor = [0.0, 0.666666666666, 0.0]
    acubeDisplay.AmbientColor = [1.0, 1.0, 1.0]



# Draw DUNE FD shape
#====================
if draw_FD:
    # create a new 'Box'
    cube.append(Box())

    # Properties modified on cube
    cube[-1].XLength = 1400.0
    cube[-1].YLength = 6200.0
    cube[-1].ZLength = 1400.0
    cube[-1].Center = [-1550., 3100.-70., 0.]

    # show data in view
    acubeDisplay = Show(cube[-1], renderView1)
    # trace defaults for the display properties.
    acubeDisplay.Representation = 'Wireframe'
    acubeDisplay.ColorArrayName = [None, '']
    acubeDisplay.OSPRayScaleArray = 'Normals'
    acubeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    acubeDisplay.SelectOrientationVectors = 'None'
    acubeDisplay.ScaleFactor = 30.0
    acubeDisplay.SelectScaleArray = 'None'
    acubeDisplay.GlyphType = 'Arrow'
    acubeDisplay.GlyphTableIndexArray = 'None'
    acubeDisplay.DataAxesGrid = 'GridAxesRepresentation'
    acubeDisplay.PolarAxes = 'PolarAxesRepresentation'
    acubeDisplay.GaussianRadius = 15.0
    acubeDisplay.SetScaleArray = [None, '']
    acubeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    acubeDisplay.OpacityArray = [None, '']
    acubeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    acubeDisplay.Opacity = 1.0

    # Properties modified on acubeDisplay
    #acubeDisplay.AmbientColor = [0.0, 0.666666666666, 0.0]
    acubeDisplay.AmbientColor = [1.0, 1.0, 1.0]

    # create a new 'Box'
    cube.append(Box())

    # Properties modified on cube
    cube[-1].XLength = 1400.0
    cube[-1].YLength = 6200.0
    cube[-1].ZLength = 1400.0
    cube[-1].Center = [1550., 3100.-70., 0.]

    # show data in view
    acubeDisplay = Show(cube[-1], renderView1)
    # trace defaults for the display properties.
    acubeDisplay.Representation = 'Wireframe'
    acubeDisplay.ColorArrayName = [None, '']
    acubeDisplay.OSPRayScaleArray = 'Normals'
    acubeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    acubeDisplay.SelectOrientationVectors = 'None'
    acubeDisplay.ScaleFactor = 30.0
    acubeDisplay.SelectScaleArray = 'None'
    acubeDisplay.GlyphType = 'Arrow'
    acubeDisplay.GlyphTableIndexArray = 'None'
    acubeDisplay.DataAxesGrid = 'GridAxesRepresentation'
    acubeDisplay.PolarAxes = 'PolarAxesRepresentation'
    acubeDisplay.GaussianRadius = 15.0
    acubeDisplay.SetScaleArray = [None, '']
    acubeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    acubeDisplay.OpacityArray = [None, '']
    acubeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    acubeDisplay.Opacity = 1.0

    # Properties modified on acubeDisplay
    #acubeDisplay.AmbientColor = [0.0, 0.666666666666, 0.0]
    acubeDisplay.AmbientColor = [1.0, 1.0, 1.0]

    # create a new 'Box'
    cube.append(Box())

    # Properties modified on cube
    cube[-1].XLength = 1400.0
    cube[-1].YLength = 6200.0
    cube[-1].ZLength = 1400.0
    cube[-1].Center = [-1550., 10000., 0.]

    # show data in view
    acubeDisplay = Show(cube[-1], renderView1)
    # trace defaults for the display properties.
    acubeDisplay.Representation = 'Wireframe'
    acubeDisplay.ColorArrayName = [None, '']
    acubeDisplay.OSPRayScaleArray = 'Normals'
    acubeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    acubeDisplay.SelectOrientationVectors = 'None'
    acubeDisplay.ScaleFactor = 30.0
    acubeDisplay.SelectScaleArray = 'None'
    acubeDisplay.GlyphType = 'Arrow'
    acubeDisplay.GlyphTableIndexArray = 'None'
    acubeDisplay.DataAxesGrid = 'GridAxesRepresentation'
    acubeDisplay.PolarAxes = 'PolarAxesRepresentation'
    acubeDisplay.GaussianRadius = 15.0
    acubeDisplay.SetScaleArray = [None, '']
    acubeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    acubeDisplay.OpacityArray = [None, '']
    acubeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    acubeDisplay.Opacity = 1.0

    # Properties modified on acubeDisplay
    #acubeDisplay.AmbientColor = [0.0, 0.666666666666, 0.0]
    acubeDisplay.AmbientColor = [1.0, 1.0, 1.0]

    # create a new 'Box'
    cube.append(Box())

    # Properties modified on cube
    cube[-1].XLength = 1400.0
    cube[-1].YLength = 6200.0
    cube[-1].ZLength = 1400.0
    cube[-1].Center = [1550., 10000., 0.]

    # show data in view
    acubeDisplay = Show(cube[-1], renderView1)
    # trace defaults for the display properties.
    acubeDisplay.Representation = 'Wireframe'
    acubeDisplay.ColorArrayName = [None, '']
    acubeDisplay.OSPRayScaleArray = 'Normals'
    acubeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    acubeDisplay.SelectOrientationVectors = 'None'
    acubeDisplay.ScaleFactor = 30.0
    acubeDisplay.SelectScaleArray = 'None'
    acubeDisplay.GlyphType = 'Arrow'
    acubeDisplay.GlyphTableIndexArray = 'None'
    acubeDisplay.DataAxesGrid = 'GridAxesRepresentation'
    acubeDisplay.PolarAxes = 'PolarAxesRepresentation'
    acubeDisplay.GaussianRadius = 15.0
    acubeDisplay.SetScaleArray = [None, '']
    acubeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    acubeDisplay.OpacityArray = [None, '']
    acubeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    acubeDisplay.Opacity = 1.0

    # Properties modified on acubeDisplay
    #acubeDisplay.AmbientColor = [0.0, 0.666666666666, 0.0]
    acubeDisplay.AmbientColor = [1.0, 1.0, 1.0]


#### create/store 360 deg orbit animation
#=========================================
if args.animation:
    # get animation scene
    animationScene1 = GetAnimationScene()

    # Properties modified on animationScene1
    animationScene1.PlayMode = 'Real Time'

    # Properties modified on animationScene1
    animationScene1.Duration = 20

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    # uncomment following to set a specific view size
    # renderView1.ViewSize = [1555, 563]

    # get camera animation track for the view
    cameraAnimationCue1 = GetCameraTrack(view=renderView1)

    # create keyframes for this animation track

    # create a key frame
    keyFrame5304 = CameraKeyFrame()
    keyFrame5304.Position = [2732.0508075688776, 0.0, 0.0]
    keyFrame5304.FocalPoint = [-1e-20, 0.0, 0.0]
    keyFrame5304.ViewUp = [0.0, 0.0, 1.0]
    keyFrame5304.ParallelScale = 1.
    keyFrame5304.PositionPathPoints = [1500.0, 0.0, 0.0, 943.9805865747562, 1165.7189421854564, 0.0, -311.867536226639, 1467.2214011007086, 0.0, -1336.5097862825519, 680.9857496093204, 0.0, -1370.3181864639016, -610.1049646137003, 0.0, -388.22856765378134, -1448.8887394336025, 0.0, 881.6778784387096, -1213.5254915624214, 0.0]
    keyFrame5304.FocalPathPoints = [0.0, 0.0, 0.0]
    keyFrame5304.ClosedPositionPath = 1

    # create a key frame
    keyFrame5305 = CameraKeyFrame()
    keyFrame5305.KeyTime = 1.0
    keyFrame5305.Position = [2732.0508075688776, 0.0, 0.0]
    keyFrame5305.FocalPoint = [-1e-20, 0.0, 0.0]
    keyFrame5305.ViewUp = [0.0, 0.0, 1.0]
    keyFrame5305.ParallelScale = 1.

    # initialize the animation track
    cameraAnimationCue1.Mode = 'Path-based'
    cameraAnimationCue1.KeyFrames = [keyFrame5304, keyFrame5305]

    # current camera placement for renderView1
    renderView1.CameraPosition = [2732.0508075688776, 0.0, 0.0]
    renderView1.CameraFocalPoint = [-1e-20, 0.0, 0.0]
    renderView1.CameraViewUp = [0.0, 0.0, 1.0]
    renderView1.CameraParallelScale = 1.

if False:
    # save animation
    SaveAnimation('/home/pkoller/Desktop/test.avi', renderView1, ImageResolution=[1600, 800],
        FrameRate=30,
        FrameWindow=[0, 600])

# get animation scene
animationScene1 = GetAnimationScene()

animationScene1.Play()



#### saving camera placements for all active views
# current camera placement for renderView1
renderView1.CameraPosition = [1500.0, 250.0, 0.0]
renderView1.CameraFocalPoint = [0.0, 250.0, 0.0]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 1.



#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).

Interact(view=renderView1)
