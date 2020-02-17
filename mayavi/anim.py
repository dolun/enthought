#!/home/adonis/anaconda3/bin/python3		
# -*- coding: utf-8 -*-

from mayavi import mlab
from scipy import sin, ogrid, array
from pylab import plot, show 

# prepare data, hence test scipy elements
x , y = ogrid[-3:3:100j , -3:3:100j]
z = sin(x**2 + y**2)

# test matplotlib
# plot(x, sin(x**2)); show()

#now mayavi2
obj = mlab.surf(x,y,z)
P = mlab.pipeline
scalar_cut_plane = P.scalar_cut_plane(obj, plane_orientation='y_axes')
scalar_cut_plane.enable_contours = True
scalar_cut_plane.contour.filled_contours = True
scalar_cut_plane.implicit_plane.widget.origin = array([  0.00000000e+00,   1.46059210e+00,  -2.02655792e-06])

scalar_cut_plane.warp_scalar.filter.normal = array([ 0.,  1.,  0.])
scalar_cut_plane.implicit_plane.widget.normal = array([ 0.,  1.,  0.])
f = mlab.gcf()
f.scene.camera.azimuth(10)

f.scene.show_axes = True
f.scene.magnification = 4 # or 4
mlab.axes()

# Now animate the data.
dt = 0.01; N = 40
ms = obj.mlab_source
for k in range(N):
    x = x + k*dt
    scalars = sin(x**2 + y**2)
    ms.set(x=x, scalars=scalars)
