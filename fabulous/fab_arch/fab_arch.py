import re
from array import *
import fileinput
import sys
import getopt
import csv


wires = set()
bels = set()
pips = set()
# Create bels

ctx.addBel(name="X0Y0.A", type="Global_Clock",
           loc=Loc(0, 0, 1), gb=False, hidden=False)
bels.add("X0Y0.A")
if "X0Y0_CLK" not in wires:
    wires.add("X0Y0_CLK")
    ctx.addWire(name="X0Y0_CLK", type="CLK", x=0, y=0)
ctx.addBelOutput(bel="X0Y0.A", name="CLK", wire="X0Y0_CLK")

try:
    with open("./bel.txt", 'r') as file:
        bel_lines = file.readlines()
except IOError:
    print("bel.txt not accessible")

for i, line in enumerate(bel_lines):
    if '#' in line:
        continue
    context = line.replace("\n", "").split(',')
    if len(context) < 6:
        continue
    tile = context[0]
    bel_x = int(context[1][1:])
    bel_y = int(context[2][1:])
    bel_z = int(ord(context[3])-64)
    bel_idx = context[3]
    bel_type = context[4]
    bel_ports = context[5:]

    bel_name = tile+'.'+bel_idx

    if bel_name not in bels:
        ctx.addBel(name=bel_name, type=bel_type, loc=Loc(
            bel_x, bel_y, bel_z), gb=False, hidden=False)
        bels.add(bel_name)
    if bel_type == "IO_1_bidirectional_frame_config_pass":
        for port in bel_ports:
            wire_name = tile+'_'+port
            #ctx.addWire(name=tile+'_'+bel_idx+'_CLK', type='IO_CLK', x=bel_x, y=bel_y)
            if wire_name not in wires:
                wires.add(wire_name)
                ctx.addWire(name=wire_name, type='W_IO_' +
                            port, x=bel_x, y=bel_y)
            if port[-1] in ['I', 'T']:
                ctx.addBelInput(bel=bel_name, name=port[-1], wire=wire_name)
            else:
                ctx.addBelOutput(bel=bel_name, name=port[-1], wire=wire_name)
    elif bel_type == "InPass4_frame_config":
        for port in bel_ports:
            wire_name = tile+'_'+port
            if wire_name not in wires:
                wires.add(wire_name)
                ctx.addWire(name=wire_name, type=port, x=bel_x, y=bel_y)
            ctx.addBelOutput(bel=bel_name, name=port[-2:], wire=wire_name)
    elif bel_type == "OutPass4_frame_config":
        for port in bel_ports:
            wire_name = tile+'_'+port
            if wire_name not in wires:
                wires.add(wire_name)
                ctx.addWire(name=wire_name, type=port, x=bel_x, y=bel_y)
            ctx.addBelInput(bel=bel_name, name=port[-2:], wire=wire_name)
    elif bel_type == "RegFile_32x4":
        wire_name = tile+"_CLK"
        if wire_name not in wires:
            wires.add(wire_name)
            ctx.addWire(name=wire_name, type="REG_CLK", x=bel_x, y=bel_y)
        ctx.addBelInput(bel=bel_name, name="CLK", wire=wire_name)
        ctx.addPip(name="X0Y0_CLK"+'_'+wire_name, type="global_clock",
                   srcWire="X0Y0_CLK", dstWire=wire_name,
                   delay=ctx.getDelayFromNS(0.05), loc=Loc(0, 0, 0))
        for port in bel_ports:
            wire_name = tile+'_'+port
            if port[0] == 'D':
                if wire_name not in wires:
                    wires.add(wire_name)
                    ctx.addWire(name=wire_name, type="WRITE_DATA",
                                x=bel_x, y=bel_y)
                ctx.addBelInput(bel=bel_name, name=port, wire=wire_name)
            elif port[0] == 'W':
                if wire_name not in wires:
                    wires.add(wire_name)
                    ctx.addWire(name=wire_name,
                                type="WRITE_ADDRESS", x=bel_x, y=bel_y)
                ctx.addBelInput(bel=bel_name, name=port, wire=wire_name)
            elif port[1] == 'D':
                if wire_name not in wires:
                    wires.add(wire_name)
                    ctx.addWire(name=wire_name, type="READ_DATA",
                                x=bel_x, y=bel_y)
                ctx.addBelOutput(bel=bel_name, name=port, wire=wire_name)
            else:
                if wire_name not in wires:
                    wires.add(wire_name)
                    ctx.addWire(name=wire_name,
                                type="READ_ADDRESS", x=bel_x, y=bel_y)
                ctx.addBelInput(bel=bel_name, name=port, wire=wire_name)
    elif bel_type == "MULADD":
        for port in bel_ports:
            wire_name = tile+'_'+port
            if port[0] == 'Q':
                if wire_name not in wires:
                    wires.add(wire_name)
                    ctx.addWire(name=wire_name,
                                type="DSP_DATA_OUT", x=bel_x, y=bel_y)
                ctx.addBelOutput(bel=bel_name, name=port, wire=wire_name)
            elif port == "clr":
                if wire_name not in wires:
                    wires.add(wire_name)
                    ctx.addWire(name=wire_name, type="DSP_CLR",
                                x=bel_x, y=bel_y)
                ctx.addBelInput(bel=bel_name, name=port, wire=wire_name)
            else:
                if wire_name not in wires:
                    wires.add(wire_name)
                    ctx.addWire(name=wire_name, type="DSP_DATA_IN",
                                x=bel_x, y=bel_y)
                ctx.addBelInput(bel=bel_name, name=port, wire=wire_name)
    elif bel_type == "MUX8LUT_frame_config":
        for port in bel_ports:
            wire_name = tile+'_'+port
            if port[0] == 'M':
                if wire_name not in wires:
                    wires.add(wire_name)
                    ctx.addWire(name=wire_name, type="LUTMUX_" +
                                port, x=bel_x, y=bel_y)
                ctx.addBelOutput(bel=bel_name, name=port, wire=wire_name)
            else:
                if wire_name not in wires:
                    wires.add(wire_name)
                    ctx.addWire(name=wire_name, type="LUTMUX_" +
                                port, x=bel_x, y=bel_y)
                ctx.addBelInput(bel=bel_name, name=port, wire=wire_name)
    elif bel_type == "FABULOUS_LC":
        wire_name = tile+"_L"+bel_idx+"_CLK"
        if wire_name not in wires:
            wires.add(wire_name)
            ctx.addWire(name=wire_name, type="LUT_CLK", x=bel_x, y=bel_y)
        ctx.addBelInput(bel=bel_name, name="CLK", wire=wire_name)
        ctx.addPip(name="X0Y0_CLK"+'_'+wire_name, type="global_clock",
                   srcWire="X0Y0_CLK", dstWire=wire_name,
                   delay=ctx.getDelayFromNS(0.05), loc=Loc(0, 0, 0))
        for port in bel_ports:
            wire_name = tile+'_'+port
            if port[3] == 'S':
                if wire_name not in wires:
                    wires.add(wire_name)
                    ctx.addWire(name=wire_name, type="LUT_" +
                                port, x=bel_x, y=bel_y)
                ctx.addBelInput(bel=bel_name, name=port[3:], wire=wire_name)
            elif port[3] == 'E':
                if wire_name not in wires:
                    wires.add(wire_name)
                    ctx.addWire(name=wire_name, type="LUT_" +
                                port, x=bel_x, y=bel_y)
                ctx.addBelInput(bel=bel_name, name=port[3:], wire=wire_name)
            elif port[3] == 'I':
                if wire_name not in wires:
                    wires.add(wire_name)
                    ctx.addWire(name=wire_name, type="LUT_" +
                                port, x=bel_x, y=bel_y)
                ctx.addBelInput(bel=bel_name, name=port[3:], wire=wire_name)
            elif port[3] == 'O':  # or  port[3] == 'Q':
                if wire_name not in wires:
                    wires.add(wire_name)
                    wires.add(wire_name.replace('_O', '_Q'))
                    ctx.addWire(name=wire_name, type="LUT_" +
                                port, x=bel_x, y=bel_y)
                    ctx.addWire(name=wire_name.replace('_O', '_Q'),
                                type="LUT_"+port, x=bel_x, y=bel_y)
                    # print(wire_name.replace('_O','_Q'))
                ctx.addBelOutput(bel=bel_name, name=port[3], wire=wire_name)
                ctx.addBelOutput(bel=bel_name, name='Q',
                                 wire=wire_name.replace('_O', '_Q'))
            else:
                if port[-1] == 'i':
                    if wire_name not in wires:
                        wires.add(wire_name)
                        ctx.addWire(name=wire_name,
                                    type="carry_in", x=bel_x, y=bel_y)
                    ctx.addBelInput(bel=bel_name, name="Ci", wire=wire_name)
                else:
                    if wire_name not in wires:
                        wires.add(wire_name)
                        ctx.addWire(name=wire_name,
                                    type="carry_out", x=bel_x, y=bel_y)
                    ctx.addBelOutput(bel=bel_name, name="Co", wire=wire_name)

print('reading bels finish\n')

# Pips
try:
    with open("./pips.txt", 'r') as file:
        pip_lines = file.readlines()
except IOError:
    print("pips.txt not accessible")

for i, line in enumerate(pip_lines):
    if '#' in line:
        continue
    context = line.split(',')
    src_tile = context[0]
    src_loc = context[0].replace('X', '').split('Y')
    src_x = int(src_loc[0])
    src_y = int(src_loc[1])
    src_port = context[1]
    dst_tile = context[2]
    dst_loc = context[2].replace('X', '').split('Y')
    dst_x = int(dst_loc[0])
    dst_y = int(dst_loc[1])
    dst_port = context[3]
    src_wire_name = src_tile+'_'+src_port
    dst_wire_name = dst_tile+'_'+dst_port
    pip_delay = int(context[4])
    pip_name = src_tile+'.'+context[5]
    pip_type = context[5]

    if src_wire_name not in wires:
        wires.add(src_wire_name)
        #ctx.addWire(name=src_wire_name, type="interconnect", x=src_x, y=src_y)
        ctx.addWire(name=src_wire_name, type=src_port, x=src_x, y=src_y)
    if dst_wire_name not in wires:
        wires.add(dst_wire_name)
        #ctx.addWire(name=dst_wire_name, type="interconnect", x=dst_x, y=dst_y)
        ctx.addWire(name=dst_wire_name, type=dst_port, x=dst_x, y=dst_y)
    # ctx.addPip(name=pip_name, type="interconnect",
    ctx.addPip(name=pip_name, type=pip_name,
               srcWire=src_wire_name, dstWire=dst_wire_name,
               delay=ctx.getDelayFromNS(0.05), loc=Loc(src_x, src_y, 0))
    lco_str = ['LA_O', 'LB_O', 'LC_O', 'LD_O', 'LE_O', 'LF_O', 'LG_O', 'LH_O']
    if any(lco in src_wire_name+dst_wire_name for lco in lco_str):
        # ctx.addPip(name=pip_name.replace('_O','_Q'), type="interconnect",
        ctx.addPip(name=pip_name.replace('_O', '_Q'), type=pip_type,
                   srcWire=src_wire_name.replace('_O', '_Q'), dstWire=dst_wire_name.replace('_O', '_Q'),
                   delay=ctx.getDelayFromNS(0.05), loc=Loc(src_x, src_y, 0))

print('reading pips finish\n')
