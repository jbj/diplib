import PyDIP as dip

a = dip.Image((10,20),1)
a.Fill(3)
b = a[0:4,4:-1]
b.Fill(55)
a[:3,:10] = 100
a[5:7,10:15] = 200
a.Show('normal')

m = a>=100
m.Show()

a[m].Show('normal')

a[m] = 176
a.Show('normal')

###

import PyDIP as dip
from scipy import misc

f = misc.face()
a = dip.Image(f)
a.Show()

b = dip.Uniform(a,15)
b.Convert("UINT8")
b.Show()

###

import PyDIP as dip
import numpy as np
from scipy import misc
import matplotlib.pyplot as pp
img = dip.Image(misc.face()[:,:,0])
grad = dip.GradientMagnitude(img,[5]) # TODO: fix syntax: allow scalar as sigma
grad.Show()

a = dip.Watershed(grad)
a.Show()

seeds = dip.Image(np.random.random(list(reversed(img.Sizes()))))>0.99
b = dip.SeededWatershed(grad,seeds)
b.Show()

h,b = dip.Histogram(img)
pp.clf()
pp.plot(b[0],h)
pp.show(block=False)

###

import PyDIP as dip
from scipy import misc
img = dip.Image(misc.face())
x = dip.Gradient(dip.Norm(img))
x.Show()

y = x*dip.Transpose(x)
y.Show()

###

import PyDIP as dip
a = dip.Image((20,10),3)
dip.FillXCoordinate(a.TensorElement(0))
dip.FillYCoordinate(a.TensorElement(1))
dip.FillColoredNoise(a.TensorElement(2))
a.Show()

a.SetColorSpace('rgb')
b = dip.ColorSpaceManager.Convert(a,'Lab')
b.Show()

b.TensorElement(1).Show()

b,c = dip.Histogram(a)
len(c)
b.Dimensionality() == len(c)

a = dip.Image((250,260),3)
a.Fill(0)
import random
color = list([1.0,1.5,0.5])
for ii in range(0,1000):
   random.shuffle(color)
   dip.DrawGaussianBlob(a,[random.uniform(1,3),random.uniform(1,3)],[random.uniform(-2,252),random.uniform(-2,262)],color)
a.Show()

###

import PyDIP as dip
a = dip.ImageReadICS('../../../examples/cermet')
a.SetPixelSize(dip.PixelSize(dip.PhysicalQuantity(1,"um")))
b = dip.Label(a < 120)
dip.MeasurementTool.Features()
m = dip.MeasurementTool.Measure(b,a,['Size','Feret','Convexity','Statistics'])
print(m)
m['Feret'][50][2]
dip.WriteCSV(m,'test.csv')
dip.WriteCSV(m,'test2.csv',{'unicode','simple'})

b = dip.EuclideanSkeleton(a > 120)
dip.GetEndPixels(b).Show()
dip.GetLinkPixels(b).Show()
dip.GetBranchPixels(b).Show()

###

import PyDIP as dip
a=dip.ImageReadICS('../../../examples/cermet')
b=dip.Label(a < 120)
b.Show('labels')
dip.GetObjectLabels(b)
c=dip.SmallObjectsRemove(b, 150)
c.Show('labels')
dip.GetObjectLabels(c)
d=dip.Relabel(c)
d.Show('labels')
dip.GetObjectLabels(d)
