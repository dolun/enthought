#!/home/adonis/anaconda3/bin/python3		
# -*- coding: iso-8859-1 -*-   
import pylab as np
from mayavi import mlab
x, y = np.mgrid[0:3:1,0:3:1]
s = mlab.surf(x, y, np.asarray(x*0.1, 'd'),
              representation='wireframe')
# Animate the data.
fig = mlab.gcf()
ms = s.mlab_source
for i in range(5000):
	i=(i%12)+5
	x, y = np.mgrid[0:3:1.0/(i+2),0:3:1.0/(i+2)]
	sc = np.asarray(x*x*0.05*(i+1), 'd')
	ms.reset(x=x, y=y, scalars=sc)
	fig.scene.reset_zoom()
