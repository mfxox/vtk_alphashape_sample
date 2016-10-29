# sample for alpha_shape_with_vtk
import vtk
import numpy as np

# The points to be triangulated are generated randomly in the unit
# cube located at the origin. The points are then associated with a
# vtkPolyData.
pcd_file = "./test_10.pcd"
pcd_arr = np.genfromtxt(pcd_file, delimiter=" ", skip_header=11)[:, :3]
points = vtk.vtkPoints()
lines = vtk.vtkCellArray()
polygon = vtk.vtkPolyData()
polygonMapper = vtk.vtkPolyDataMapper()
polygonActor = vtk.vtkActor()

points_num = pcd_arr.shape[0]
points.SetNumberOfPoints(points_num)
lines.InsertNextCell(points_num)
for i in xrange(points_num):
    points.SetPoint(i, pcd_arr[i][0], pcd_arr[i][1], pcd_arr[i][2])
polygon.SetPoints(points)

delaunay = vtk.vtkDelaunay3D()
delaunay.SetInputData(polygon)
delaunay.SetAlpha(1)
delaunay.AlphaLinesOff()
delaunay.AlphaVertsOff()
delaunay.Update()

# Shrink the result to help see it better.
shrink = vtk.vtkShrinkFilter()
shrink.SetInputConnection(delaunay.GetOutputPort())
shrink.SetShrinkFactor(0.9)

map = vtk.vtkDataSetMapper()
map.SetInputConnection(shrink.GetOutputPort())

triangulation = vtk.vtkActor()
triangulation.SetMapper(map)
triangulation.GetProperty().SetColor(1, 0, 0)

# Create graphics stuff
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the renderer, set the background and size
ren.AddActor(triangulation)
ren.SetBackground(1, 1, 1)
renWin.SetSize(250, 250)
renWin.Render()

iren.Initialize()
renWin.Render()
iren.Start()
