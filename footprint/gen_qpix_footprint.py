from KicadModTree import *
import csv
import math

footprint_name = "qpix-digi"

# init kicad footprint
kicad_mod = Footprint(footprint_name)
kicad_mod.setDescription("A example footprint")
kicad_mod.setTags("q-pix")

# set general values
kicad_mod.append(Text(type='reference', text='REF**', at=[0, -3], layer='F.SilkS'))
kicad_mod.append(Text(type='value', text=footprint_name, at=[1.5, 3], layer='F.Fab'))


scale = 3.0
xmax, xmin = 0, 0
ymax, ymin = 0, 0
cnt = 0
w, l = 0.2, 0.8


with open('./qpix_pinout.csv', mode ='r') as f :
  reader = csv.DictReader(f)
  for r in reader : 
    x    = float(r["X"].strip())/1000.0
    y    = float(r["Y"].strip())/1000.0
    if cnt == 0 : 
      xmin, ymin= x,y
    else : 
      if x < xmin : xmin = x
      if y < ymin : ymin = y
      if x > xmax : xmax = x
      if y > ymax : ymax = y
    cnt += 1

x_die_max, y_die_max = xmax, ymax
x_die_min, y_die_min = xmin, ymin
# centering
x0, y0 = (xmax - xmin)/2.0, (ymax - ymin)/2.0

xmax, ymax = (xmax-x0)*scale, (ymax-y0)*scale
xmin, ymin = (xmin-x0)*scale, (ymin-y0)*scale



print(x0,y0)
print(xmax,ymax)
print(xmin,ymin)

with open('./qpix_pinout.csv', mode ='r') as f :
  reader = csv.DictReader(f)
  for r in reader : 
    # print(r)
     
    num  = int(r["Pin"])
    name = r["Name"].strip()
    xchip = -x0 + float(r["X"].strip())/1000.0
    ychip = -y0 + float(r["Y"].strip())/1000.0
    xpad  = (-x0 + float(r["X"].strip())/1000.0)*scale
    ypad  = (-y0 + float(r["Y"].strip())/1000.0)*scale
    side  = r["Side"].strip()

    angle = -math.atan((ypad-ychip)/(xpad-xchip))*180/math.pi
    sz = [l,w]
    # if side == "top" or side == "bottom":
      # sz = [w,l]
      # # angle = math.atan((xpad-xchip)/(ypad-ychip))*180/math.pi
    # else:
      # sz = [l,w]
      # # angle = -math.atan(y/x)*180/math.pi

  

    # angle = 0
    kicad_mod.append(Pad(number=num, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                         rotation = angle,
                         at=[xpad, ypad], size=sz, drill=0, layers=Pad.LAYERS_SMT))

    kicad_mod.append(Line(start=[xchip, ychip], 
                              end=[xpad, ypad], 
                              width = 0.05, layer='F.SilkS'))

x_ss, y_ss = 1, 1
# create silscreen
kicad_mod.append(RectLine(start=[xmin-x_ss, ymin-y_ss], end=[xmax+x_ss, ymax+y_ss], layer='F.SilkS'))
kicad_mod.append(RectLine(start=[-x_die_max/2, -y_die_max/2], end=[x_die_max/2, y_die_max/2], layer='F.SilkS'))

x_cy, y_cy = 1.5, 1.5
# create courtyard
kicad_mod.append(RectLine(start=[xmin-x_cy, ymin-y_cy], end=[xmax+x_cy, ymax+y_cy], layer='F.CrtYd'))


# add model
kicad_mod.append(Model(filename="example.3dshapes/example_footprint.wrl",
                       at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

# output kicad model
file_handler = KicadFileHandler(kicad_mod)
file_handler.writeFile('example_footprint.kicad_mod')
