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

# 13.95
# 21.84

wire_length = 5.8
xmax, xmin = 0, 0
ymax, ymin = 0, 0
cnt = 0
# pads width and length
pad_width, pad_length = 0.11, 0.5
len_width = 0.05
len1 = 1.5
pad_length_a = 1.0
i_delta = 0.04
# asic pad sizes
d_x = 0.09
d_y = 0.09

pad_step_y = 0.4
pad_step_x = 0.4



n_y = 46
n_x = 26

oangle = math.pi/2.5

# x_cy, y_cy = 13.95/2, 21.84/2
x_cy, y_cy = 19/2, 20/2
x_ss, y_ss = wire_length + 2, wire_length + 4 
sz = [pad_length,pad_width]


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





with open('./qpix_pinout.csv', mode ='r') as f :
  reader = csv.DictReader(f)
  for r in reader : 
    # print(r)
     
    num  = int(r["Pin"])
    name = r["Name"].strip()
    xraw = float(r["X"].strip())/1000.0
    yraw = float(r["Y"].strip())/1000.0
    i_pad = int(r["i"])
    xchip = -x0 + xraw
    ychip = -y0 + yraw
    side  = r["Side"].strip()
    
    i_y = int(ychip/d_y)
    i_x = int(xchip/d_x)

    if side == "left" :
      # phi = math.pi - oangle/2 + (n_y-yraw/d_y)*oangle/n_y 
      phi = math.pi - (ychip/d_y)*oangle/n_y
      print(math.fabs(ychip/d_y)*2)
    elif side == "right": 
      phi = ychip/d_y*oangle/n_y
    else:
      phi = math.atan(ychip/xchip) 
      if xchip < 0 : phi += math.pi
      # phi = math.fabs(xchip/d_x) * math.pi/n_x



    x_wire_end = xchip + wire_length*math.cos(phi)
    y_wire_end = - (ychip + wire_length*math.sin(phi))
    x_pad_end = x_wire_end + pad_length/2.0*math.cos(phi)
    y_pad_end = y_wire_end - pad_length/2.0*math.sin(phi)
    ychip = -ychip

    xpad_c = x_wire_end
    ypad_c = y_wire_end
    angle = -math.atan((ypad_c-ychip)/(xpad_c-xchip))*180/math.pi


      # x_l1_end = x_wire_end + pad_length_a*math.cos(phi)
      # y_l1_end = y_wire_end - pad_length_a*math.sin(phi)

    if side == "left" :
      x_l1_end = -x0 - len1 - i_delta*(n_y/2-abs(i_y))
      y_l1_end = y_wire_end - (x_wire_end-x_l1_end)*math.tan(math.pi-phi)
      x_l2_end = -x_cy + pad_length
      y_l2_end = (i_pad-n_y/2 - 1) * pad_step_y -0.2
      # xpad_c   = x_l2_end - pad_length/2 +0.03
      # ypad_c   = y_l2_end
      # angle = 180
    elif side == "right": 
      x_l1_end = x0 + len1 + i_delta*(n_y/2-abs(i_y))
      y_l1_end = y_wire_end - (x_wire_end-x_l1_end)*math.tan(math.pi-phi)
      x_l2_end = x_cy - pad_length
      y_l2_end = (i_pad-n_y/2 - 1) * pad_step_y -0.2
      # xpad_c = x_l2_end + pad_length/2
      # ypad_c = y_l2_end
      # # angle = 0
    elif side == "top":
      x_l1_end = x_wire_end + pad_length_a*math.cos(phi)
      y_l1_end = y_wire_end - pad_length_a*math.sin(phi)
      x_l2_end = (i_pad-n_x/2 - 1) * pad_step_x + 0.2
      y_l2_end = -y_cy  + pad_length
      # xpad_c = x_l2_end
      # ypad_c = y_l2_end - pad_length/2
      # angle = -90
    elif side == "bottom":
      x_l1_end = x_wire_end + pad_length_a*math.cos(phi)
      y_l1_end = y_wire_end - pad_length_a*math.sin(phi)
      x_l2_end = (i_pad-n_x/2 - 1) * pad_step_x +0.2
      y_l2_end = y_cy - pad_length
      # xpad_c = x_l2_end 
      # ypad_c = y_l2_end + pad_length/2
      # angle = 90


  
    # bond wires
    kicad_mod.append(Line(start=[xchip, ychip], 
                              end=[x_wire_end, y_wire_end], 
                              width = 0.025, layer='User.1'))

    kicad_mod.append(Pad(number=num, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                         rotation = angle,
                         at=[xpad_c, ypad_c], size=sz, drill=0, layers=Pad.LAYERS_SMT))

    kicad_mod.append(Line(start=[x_pad_end, y_pad_end], 
                              end=[x_l2_end, y_l2_end], 
                              width = len_width, layer='User.2'))

    # kicad_mod.append(Line(start=[x_l1_end, y_l1_end], 
                              # end=[x_l2_end, y_l2_end], 
                              # width = len_width, layer='User.2'))



# create silscreen
# kicad_mod.append(RectLine(start=[-x_ss, -y_ss], end=[x_ss, y_ss], layer='F.SilkS'))
kicad_mod.append(RectLine(start=[-x_die_max/2, -y_die_max/2], end=[x_die_max/2, y_die_max/2], layer='F.SilkS', width = 0.05))

# create courtyard
kicad_mod.append(RectLine(start=[-x_cy, -y_cy], end=[x_cy, y_cy], layer='F.CrtYd'))


# add model
kicad_mod.append(Model(filename="example.3dshapes/qpix_digi_footprint.wrl",
                       at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

# output kicad model
file_handler = KicadFileHandler(kicad_mod)
file_handler.writeFile('qpix_digi_footprint.kicad_mod')
