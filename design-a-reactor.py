#import numpy
#import matplotlib.pyplot as plt

from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize
import openmoc.process as process
from openmoc.options import Options


###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

options = Options()
num_threads = options.getNumThreads()
track_spacing = options.getTrackSpacing()
num_azim = options.getNumAzimAngles()
tolerance = options.getTolerance()
max_iters = options.getMaxIterations()
acceleration = options.getCmfdAcceleration()
relax_factor = options.getCmfdRelaxationFactor()
mesh_level = options.getCmfdMeshLevel()


log.set_log_level('NORMAL')

log.py_printf('TITLE', 'Simulating a Design-a-Critical Reactor Problem...')


###############################################################################
###########################   Creating Materials   ############################
###############################################################################

log.py_printf('NORMAL', 'Importing materials data from HDF5...')

materials = materialize.materialize('design-a-reactor-materials.hdf5')

uo2_id = materials['UO2'].getId()
mox43_id = materials['MOX-4.3%'].getId()
mox7_id = materials['MOX-7%'].getId()
mox87_id = materials['MOX-8.7%'].getId()
guide_tube_id = materials['Guide Tube'].getId()
fiss_id = materials['Fission Chamber'].getId()
water_id = materials['Water'].getId()


###############################################################################
###########################   Creating Surfaces   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating surfaces...')

circles = []
planes = []
planes.append(XPlane(x=-37.8))
planes.append(XPlane(x=37.8))
planes.append(YPlane(y=-37.8))
planes.append(YPlane(y=37.8))
circles.append(Circle(x=0., y=0., radius=0.54))
circles.append(Circle(x=0., y=0., radius=0.58))
circles.append(Circle(x=0., y=0., radius=0.62))
planes[0].setBoundaryType(VACUUM)
planes[1].setBoundaryType(VACUUM)
planes[2].setBoundaryType(VACUUM)
planes[3].setBoundaryType(VACUUM)


###############################################################################
#############################   Creating Cells   ##############################
###############################################################################

log.py_printf('NORMAL', 'Creating cells...')

cells = []

# UO2 pin cells
cells.append(CellBasic(universe=1, material=uo2_id, rings=3, sectors=8))
cells.append(CellBasic(universe=1, material=water_id, sectors=8))
cells.append(CellBasic(universe=1, material=water_id, sectors=8))
cells.append(CellBasic(universe=1, material=water_id, sectors=8))
cells[0].addSurface(-1, circles[0])
cells[1].addSurface(+1, circles[0])
cells[1].addSurface(-1, circles[1])
cells[2].addSurface(+1, circles[1])
cells[2].addSurface(-1, circles[2])
cells[3].addSurface(+1, circles[2])


# 4.3% MOX pin cells
cells.append(CellBasic(universe=2, material=mox43_id, rings=3, sectors=8))
cells.append(CellBasic(universe=2, material=water_id, sectors=8))
cells.append(CellBasic(universe=2, material=water_id, sectors=8))
cells.append(CellBasic(universe=2, material=water_id, sectors=8))
cells[4].addSurface(-1, circles[0])
cells[5].addSurface(+1, circles[0])
cells[5].addSurface(-1, circles[1])
cells[6].addSurface(+1, circles[1])
cells[6].addSurface(-1, circles[2])
cells[7].addSurface(+1, circles[2])


# 7% MOX pin cells
cells.append(CellBasic(universe=3, material=mox7_id, rings=3, sectors=8))
cells.append(CellBasic(universe=3, material=water_id, sectors=8))
cells.append(CellBasic(universe=3, material=water_id, sectors=8))
cells.append(CellBasic(universe=3, material=water_id, sectors=8))
cells[8].addSurface(-1, circles[0])
cells[9].addSurface(+1, circles[0])
cells[9].addSurface(-1, circles[1])
cells[10].addSurface(+1, circles[1])
cells[10].addSurface(-1, circles[2])
cells[11].addSurface(+1, circles[2])


# 8.7% MOX pin cells
cells.append(CellBasic(universe=4, material=mox87_id, rings=3, sectors=8))
cells.append(CellBasic(universe=4, material=water_id, sectors=8))
cells.append(CellBasic(universe=4, material=water_id, sectors=8))
cells.append(CellBasic(universe=4, material=water_id, sectors=8))
cells[12].addSurface(-1, circles[0])
cells[13].addSurface(+1, circles[0])
cells[13].addSurface(-1, circles[1])
cells[14].addSurface(+1, circles[1])
cells[14].addSurface(-1, circles[2])
cells[15].addSurface(+1, circles[2])

# Fission chamber pin cells
cells.append(CellBasic(universe=5, material=fiss_id, rings=3, sectors=8))
cells.append(CellBasic(universe=5, material=water_id, sectors=8))
cells.append(CellBasic(universe=5, material=water_id, sectors=8))
cells.append(CellBasic(universe=5, material=water_id, sectors=8))
cells[16].addSurface(-1, circles[0])
cells[17].addSurface(+1, circles[0])
cells[17].addSurface(-1, circles[1])
cells[18].addSurface(+1, circles[1])
cells[18].addSurface(-1, circles[2])
cells[19].addSurface(+1, circles[2])

# Guide tube pin cells
cells.append(CellBasic(universe=6, material=guide_tube_id, rings=3, sectors=8))
cells.append(CellBasic(universe=6, material=water_id, sectors=8))
cells.append(CellBasic(universe=6, material=water_id, sectors=8))
cells.append(CellBasic(universe=6, material=water_id, sectors=8))
cells[20].addSurface(-1, circles[0])
cells[21].addSurface(+1, circles[0])
cells[21].addSurface(-1, circles[1])
cells[22].addSurface(+1, circles[1])
cells[22].addSurface(-1, circles[2])
cells[23].addSurface(+1, circles[2])

# Moderator cell
cells.append(CellBasic(universe=7, material=water_id))

# Top left, bottom right lattice
cells.append(CellFill(universe=10, universe_fill=30))

# Top right, bottom left lattice
cells.append(CellFill(universe=11, universe_fill=31))

# Moderator lattice - semi-finely spaced
cells.append(CellFill(universe=12, universe_fill=33))

# Moderator lattice - bottom of geometry
cells.append(CellFill(universe=13, universe_fill=34))

# Moderator lattice - top of geometry
cells.append(CellFill(universe=14, universe_fill=35))

# Moderator lattice - right of geometry
cells.append(CellFill(universe=15, universe_fill=36))

# Moderator lattice - left of geometry
cells.append(CellFill(universe=16, universe_fill=37))

# Moderator lattice - bottom right corner of geometry
cells.append(CellFill(universe=17, universe_fill=38))

# Moderator lattice - bottom left corner of geometry
cells.append(CellFill(universe=18, universe_fill=39))

# Moderator lattice - top left corner of geometry
cells.append(CellFill(universe=19, universe_fill=40))

# Moderator lattice - top right corner of geometry
cells.append(CellFill(universe=20, universe_fill=41))

# Full geometry
cells.append(CellFill(universe=0, universe_fill=50))
cells[-1].addSurface(+1, planes[0])
cells[-1].addSurface(-1, planes[1])
cells[-1].addSurface(+1, planes[2])
cells[-1].addSurface(-1, planes[3])


###############################################################################
###########################   Creating Lattices   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating lattices...')

lattices = []

# Top left, bottom right 15 x 15 assemblies
lattices.append(Lattice(id=30, width_x=1.26, width_y=1.26))
lattices[-1].setLatticeCells(
    [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 6, 1, 1, 6, 1, 1, 6, 1, 1, 1, 1],
     [1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 6, 1, 1, 6, 1, 1, 6, 1, 1, 6, 1, 1, 6, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 6, 1, 1, 6, 1, 1, 5, 1, 1, 6, 1, 1, 6, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 6, 1, 1, 6, 1, 1, 6, 1, 1, 6, 1, 1, 6, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1],
     [1, 1, 1, 1, 6, 1, 1, 6, 1, 1, 6, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])


# Top right, bottom left 15 x 15 assemblies 
lattices.append(Lattice(id=31, width_x=1.26, width_y=1.26))
lattices[-1].setLatticeCells(
    [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
     [2, 3, 3, 3, 6, 3, 3, 6, 3, 3, 6, 3, 3, 3, 2],
     [2, 3, 6, 3, 4, 4, 4, 4, 4, 4, 4, 3, 6, 3, 2],
     [2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 2],
     [2, 6, 4, 4, 6, 4, 4, 6, 4, 4, 6, 4, 4, 6, 2],
     [2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2],
     [2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2],
     [2, 6, 4, 4, 6, 4, 4, 5, 4, 4, 6, 4, 4, 6, 2],
     [2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2],
     [2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2],
     [2, 6, 4, 4, 6, 4, 4, 6, 4, 4, 6, 4, 4, 6, 2],
     [2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 2],
     [2, 3, 6, 3, 4, 4, 4, 4, 4, 4, 4, 3, 6, 3, 2],
     [2, 3, 3, 3, 6, 3, 3, 6, 3, 3, 6, 3, 3, 3, 2],
     [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]])


# Sliced up water cells - semi finely spaced
lattices.append(Lattice(id=33, width_x=0.126, width_y=0.126))
lattices[-1].setLatticeCells(
    [[7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7]])


# Sliced up water cells for bottom of geometry
lattices.append(Lattice(id=34, width_x=1.26, width_y=1.26))
lattices[-1].setLatticeCells(
    [[12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]])


# Sliced up water cells for top of geometry
lattices.append(Lattice(id=35, width_x=1.26, width_y=1.26))
lattices[-1].setLatticeCells(
    [[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]])


# Sliced up water cells - right side of geometry
lattices.append(Lattice(id=36, width_x=1.26, width_y=1.26))
lattices[-1].setLatticeCells(
    [[12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7]])


# Sliced up water cells - left side of geometry
lattices.append(Lattice(id=37, width_x=1.26, width_y=1.26))
lattices[-1].setLatticeCells(
    [[7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12]])


# Sliced up water cells for bottom right corner of geometry
lattices.append(Lattice(id=38, width_x=1.26, width_y=1.26))
lattices[-1].setLatticeCells(
    [[12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]])

# Sliced up water cells for bottom left corner of geometry
lattices.append(Lattice(id=39, width_x=1.26, width_y=1.26))
lattices[-1].setLatticeCells(
    [[7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]])


# Sliced up water cells for top left corner of geometry
lattices.append(Lattice(id=40, width_x=1.26, width_y=1.26))
lattices[-1].setLatticeCells(
    [[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12],
     [7, 7, 7, 7, 7, 7, 7, 12, 12, 12, 12, 12, 12, 12, 12]])


# Sliced up water cells for top right corner of geometry
lattices.append(Lattice(id=41, width_x=1.26, width_y=1.26))
lattices[-1].setLatticeCells(
    [[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7],
     [12, 12, 12, 12, 12, 12, 12, 12, 7, 7, 7, 7, 7, 7, 7]])



# 4 x 4 core to represent two bundles and water
lattices.append(Lattice(id=50, width_x=18.9, width_y=18.9))
lattices[-1].setLatticeCells([[19, 14, 14, 20],
                              [16, 10, 11, 15],
                              [16, 11, 10, 15],
                              [18, 13, 13, 17]])


###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

mesh = Mesh(MOC, acceleration, relax_factor, mesh_level)

geometry = Geometry(mesh)
for material in materials.values(): geometry.addMaterial(material)
for cell in cells: geometry.addCell(cell)
for lattice in lattices: geometry.addLattice(lattice)

geometry.initializeFlatSourceRegions()

cmfd = Cmfd(geometry)
cmfd.setOmega(1.5)


###############################################################################
########################   Creating the TrackGenerator   ######################
###############################################################################

log.py_printf('NORMAL', 'Initializing the track generator...')

track_generator = TrackGenerator(geometry, num_azim, track_spacing)
track_generator.generateTracks()


###############################################################################
###########################   Running a Simulation   ##########################
###############################################################################

# Use a CUDA solver for GPUs if the openmoc.cuda module exists
try:
    import openmoc.cuda as cuda

    # Check whether or not the machine contains a GPU
    if cuda.machineContainsGPU():
        solver = cuda.GPUSolver(geometry, track_generator)
    else:
        solver = ThreadPrivateSolver(geometry, track_generator)
        solver.setNumThreads(num_threads)

# If the openmoc.cuda module has not been built, use the standard solver
except:
    solver = ThreadPrivateSolver(geometry, track_generator, cmfd)
    solver.setNumThreads(num_threads)

solver.setSourceConvergenceThreshold(tolerance)
solver.convergeSource(max_iters)
solver.printTimerReport()


###############################################################################
##############################   Plotting Data   ##############################
###############################################################################


log.py_printf('NORMAL', 'Plotting data...')

plotter.plot_fluxes(geometry, solver, energy_groups=[1,7], gridsize=400)

log.py_printf('TITLE', 'Finished')
