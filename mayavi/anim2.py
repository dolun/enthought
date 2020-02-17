#!/home/adonis/anaconda3/bin/python3		
# -*- coding: utf-8 -*-

from numpy import linspace, meshgrid, array, sin, cos, pi, abs
from scipy.special import sph_harm 
from mayavi import mlab

theta_1d = linspace(0,   pi,  91) 
phi_1d   = linspace(0, 2*pi, 181)

theta_2d, phi_2d = meshgrid(theta_1d, phi_1d)
xyz_2d = array([sin(theta_2d) * sin(phi_2d),
                sin(theta_2d) * cos(phi_2d),
                cos(theta_2d)]) 
l=3
m=0

Y_lm = sph_harm(m,l, phi_2d, theta_2d)
r = abs(Y_lm.real)*xyz_2d
    
mlab.figure(size=(700,830))
mlab.mesh(r[0], r[1], r[2], scalars=Y_lm.real, colormap="cool")
mlab.view(azimuth=0, elevation=75, distance=2.4, roll=-50)
mlab.savefig("Y_%i_%i.jpg" % (l,m))
mlab.show()
exit()

from numpy import mgrid, zeros, sin, pi, array
from mayavi import mlab

Lx = 4
Ly = 4

S = 10
dx = 0.05
dy = 0.05

# A mesh grid
X,Y = mgrid[-S:S:dx, -S:S:dy]

# The initial function:
#Z = zeros(X.shape)
#Z = sin(pi*X/Lx)*sin(pi*Y/Ly)
#Z[Z>0] = 1
#Z[Z<0] = -1

# The Fourier series:
W = zeros(X.shape)
m = 10
for i in range(1,m,2):
    for j in range(1,m,2):
        W += 1.0 / (i*j) * sin(i * pi * X / Lx) * sin(j * pi * Y / Ly)
W *= pi / 4.0


# prepare scene
scene = mlab.gcf()
# next two lines came at the very end of the design
scene.scene.magnification = 4

# plot the object
obj = mlab.mesh(X, Y, W)
P = mlab.pipeline

# first scalar_cut_plane
scalar_cut_plane = P.scalar_cut_plane(obj, plane_orientation='z_axes')
scalar_cut_plane.enable_contours = True
scalar_cut_plane.contour.filled_contours = True
scalar_cut_plane.implicit_plane.widget.origin = array([-0.025, -0.025,  0.48])
scalar_cut_plane.warp_scalar.filter.normal = array([ 0.,  0.,  1.])
scalar_cut_plane.implicit_plane.widget.normal = array([ 0.,  0.,  1.])
scalar_cut_plane.implicit_plane.widget.enabled = False # do not show the widget

# second scalar_cut-plane
scalar_cut_plane_2 = P.scalar_cut_plane(obj, plane_orientation='z_axes')
scalar_cut_plane_2.enable_contours = True
scalar_cut_plane_2.contour.filled_contours = True
scalar_cut_plane_2.implicit_plane.widget.origin = array([-0.025, -0.025,  -0.48])
scalar_cut_plane_2.warp_scalar.filter.normal = array([ 0.,  0.,  1.])
scalar_cut_plane_2.implicit_plane.widget.normal = array([ 0.,  0.,  1.])
scalar_cut_plane_2.implicit_plane.widget.enabled = False # do not show the widget

# see it from a closer view point
scene.scene.camera.position = [-31.339891336951567, 14.405281950904936, -27.156389988308661]
scene.scene.camera.focal_point = [-0.025000095367431641, -0.025000095367431641, 0.0]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.63072643330371414, -0.083217283169475589, -0.77153033000256477]
scene.scene.camera.clipping_range = [4.7116394000124906, 93.313165745624019]
scene.scene.camera.compute_view_plane_normal()

scene.scene.render()
