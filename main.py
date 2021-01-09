# -*- coding: utf-8 -*-

import serial
import json

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph.opengl as gl
import numpy as np
import pyqtgraph as pg


f_s = 1.0/0.02
t_span = 5.0
N_values = int(t_span*f_s)


# nicer colors
seaborn_deep = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
                "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]
color_bg = pg.mkColor("#eaeaf2")
color_curves = []
for color in seaborn_deep:
    color_curves.append(pg.mkColor(color))

################################################################################

# set-up Qt plot window
app = QtGui.QApplication([])

win = pg.GraphicsWindow(title='Position Estimation Demo')
win.resize(800,600)
win.move(100,100)
win.setWindowTitle('pyqtgraph example: Plotting')
win.setBackground('w')

pg.setConfigOptions(antialias=True)
pg.setConfigOption('foreground', 'k')

################################################################################

def update_plots():
    global acc_curve, acc_data, gyro_curve, gyro_data, origin, cube, view
    try:
        ser_line = ser.readline()
        message = json.loads(bytes(ser_line).decode())
    except Exception as e:
        if hasattr(e, 'message'):
            print('plot:', e.message)
        else:
            print('plot:', e)
        return

    if message.get('meas') == 'acc':
        val = message.get('values')
        new_data = np.array([val.get('x'), val.get('y'), val.get('z')])
        acc_data[:-1, :] = acc_data[1:, :]
        acc_data[-1, :] = new_data
        for i, curve in enumerate(acc_curve):
            curve.setData(acc_data[:, i])
    elif message.get('meas') == 'gyro':
        val = message.get('values')
        new_data = np.array([val.get('x'), val.get('y'), val.get('z')])
        gyro_data[:-1, :] = gyro_data[1:, :]
        gyro_data[-1, :] = new_data
        for i, curve in enumerate(gyro_curve):
            curve.setData(gyro_data[:, i])
    elif message.get('meas') == 'angle':
        val = message.get('values')
        view.removeItem(origin)
        view.removeItem(cube)
        origin = gl.GLLinePlotItem(pos=origin_coord, mode='lines', color=origin_colors, width=8, antialias=True)
        origin.rotate(val.get('x'), 1, 0, 0)
        origin.rotate(val.get('y'), 0, 1, 0)
        origin.rotate(val.get('z'), 0, 0, 1)
        cube = gl.GLLinePlotItem(pos=cube_coord, mode='line_strip', width=2, antialias=True)
        cube.rotate(val.get('x'), 1, 0, 0)
        cube.rotate(val.get('y'), 0, 1, 0)
        cube.rotate(val.get('z'), 0, 0, 1)
        view.addItem(cube)
        view.addItem(origin)

################################################################################

view = gl.GLViewWidget()
view.setGeometry(1000, 100, 800, 600)
view.setWindowTitle('3D Position Visualization')
view.opts['distance'] = 10
view.show()

zgrid = gl.GLGridItem()
view.addItem(zgrid)
zgrid.translate(0, 0, -2)
zgrid.scale(2,2,2)

cube_coord = np.array([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,-1],
                 [-1,-1,1],[1,-1,1],[1,-1,-1],[1,-1,1],[1,1,1],
                 [1,1,-1],[1,1,1],[-1,1,1],[-1,1,-1],[-1,1,1],
                 [-1,-1,1]])

origin_coord = np.array([[0,0,0],[2,0,0],[0,0,0],[0,2,0],[0,0,0],[0,0,2]])
origin_colors = np.array((pg.glColor(color_curves[0]), pg.glColor(color_curves[0]), pg.glColor(color_curves[1]), pg.glColor(color_curves[1]), pg.glColor(color_curves[2]), pg.glColor(color_curves[2])))

cube = gl.GLLinePlotItem(pos=cube_coord, mode='line_strip', width=2, antialias=True)
origin = gl.GLLinePlotItem(pos=origin_coord, mode='lines', color=origin_colors, width=8, antialias=True)

view.addItem(cube)
view.addItem(origin)
angle_prev = [0, 0, 0]

#origin.rotate(69, 1, 1, 1)

################################################################################

p_acc = win.addPlot(title="Acceleration vs Time")
#p_acc.getViewBox().setBackgroundColor(color_bg)
#p_acc.getAxis('bottom').setPen('k')
p_acc.showGrid(True, True, 0.5)
p_acc.setLabel('left', 'a', 'g')
p_acc.setLabel('bottom', 't', 's')

ticks = np.linspace(0, N_values, int(t_span+1))
p_acc.getAxis('bottom').setTicks([[],[(v, str(-(N_values - v)/f_s)) for v in ticks ]])

p_acc.addLegend()
acc_curve = []
acc_curve.append(p_acc.plot(pen=pg.mkPen(color_curves[0], width=2)))
acc_curve.append(p_acc.plot(pen=pg.mkPen(color_curves[1], width=2)))
acc_curve.append(p_acc.plot(pen=pg.mkPen(color_curves[2], width=2)))

vb_acc = win.addViewBox()
vb_acc.setMaximumWidth(100)
legend_acc = pg.LegendItem()
legend_acc.setParentItem(vb_acc)
legend_acc.anchor((0, 0), (0.1, 0.1))
legend_acc.addItem(acc_curve[0], 'x')
legend_acc.addItem(acc_curve[1], 'y')
legend_acc.addItem(acc_curve[2], 'z')

acc_data = np.linspace((0, 0, 0), (0, 0, 0), N_values)

################################################################################
win.nextRow()

p_gyro = win.addPlot(title="Angular Velocity vs Time")
p_gyro.showGrid(True, True, 0.5)
p_gyro.setLabel('left', '<font>&Omega;</font>', '°/s')
p_gyro.setLabel('bottom', 't', 's')

ticks = np.linspace(0, N_values, int(t_span+1))
p_gyro.getAxis('bottom').setTicks([[],[(v, str(-(N_values - v)/f_s)) for v in ticks ]])

gyro_curve = []
gyro_curve.append(p_gyro.plot(pen=pg.mkPen(color_curves[0], width=2)))
gyro_curve.append(p_gyro.plot(pen=pg.mkPen(color_curves[1], width=2)))
gyro_curve.append(p_gyro.plot(pen=pg.mkPen(color_curves[2], width=2)))

vb_gyro = win.addViewBox()
vb_gyro.setMaximumWidth(100)
legend = pg.LegendItem()
legend.setParentItem(vb_gyro)
legend_acc.anchor((0, 0), (0.1, 0.1))
legend.addItem(gyro_curve[0], 'x')
legend.addItem(gyro_curve[1], 'y')
legend.addItem(gyro_curve[2], 'z')

gyro_data = np.linspace((0, 0, 0), (0, 0, 0), N_values)

################################################################################

timer = QtCore.QTimer()
timer.timeout.connect(update_plots)
timer.start(20)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        ser = serial.serial_for_url(sys.argv[1], timeout=1, baudrate=115200)
    else:
        ser = serial.serial_for_url('/dev/ttyACM0', timeout=1, baudrate=115200)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
