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


scale = 4.0
xmax, xmin = 0, 0
ymax, ymin = 0, 0
cnt = 0
w, l = 0.2, 0.2


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

x_die_max = xmax
y_die_max = ymax

xmax = xmax*scale
ymax = ymax*scale

y = float(r["Y"].strip())*scale/1000.0
# centering
x0, y0 = -(xmax - xmin)/2.0, (ymax - ymin)/2.0


print(x0,y0)
print(xmax,ymax)

with open('./qpix_pinout.csv', mode ='r') as f :
  reader = csv.DictReader(f)
  for r in reader : 
    # print(r)
     
    num  = int(r["Pin"])
    name = r["Name"].strip()
    x    = x0 + float(r["X"].strip())*scale/1000.0
    y    = y0 - float(r["Y"].strip())*scale/1000.0
    side = r["Side"].strip()

    if side == "top" or side == "bottom":
      sz = [w,l]
      angle = math.atan(x/y)*180/math.pi
    else:
      sz = [l,w]
      angle = -math.atan(y/x)*180/math.pi

  

    angle = 0
    kicad_mod.append(Pad(number=num, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                         rotation = angle,
                         at=[x, y], size=sz, drill=0, layers=Pad.LAYERS_SMT))

x_ss, y_ss = 1, 1
# create silscreen
kicad_mod.append(RectLine(start=[x0+xmin-x_ss, y0-ymin+y_ss], end=[x0+xmax+x_ss, y0-ymax-y_ss], layer='F.SilkS'))
kicad_mod.append(RectLine(start=[-x_die_max/2, -y_die_max/2], end=[x_die_max/2, y_die_max/2], layer='F.SilkS'))

x_cy, y_cy = 1.5, 1.5
# create courtyard
kicad_mod.append(RectLine(start=[x0+xmin-x_cy, y0-ymin+y_cy], end=[x0+xmax+x_cy, y0-ymax-y_cy], layer='F.CrtYd'))


# add model
kicad_mod.append(Model(filename="example.3dshapes/example_footprint.wrl",
                       at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

# output kicad model
file_handler = KicadFileHandler(kicad_mod)
file_handler.writeFile('example_footprint.kicad_mod')
