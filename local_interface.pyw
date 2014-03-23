#!/usr/bin/env python

import sys, os, platform, copy, time
import numpy as np
import widgets
import materials
import simulate
from PyQt4.QtCore import *
from PyQt4.QtGui import *

__version__ = "0.1.0"


class MainWindow(QMainWindow):

    def __init__(self, parallel=False, parent=None):
        super(MainWindow, self).__init__(parent)

        self.openmoc_simulator = simulate.LocalSimulator()

        self.uo2_factor = 3.5
        self.mox1_factor = 4.3
        self.mox2_factor = 7.0
        self.mox3_factor = 8.7
        self.poison_factor = 5.0
        self.boron_factor = 1100.0

        self.showMaximized()

        self.setWindowTitle("OpenMOC - Design A Critical Reactor Demo")

        self.coreDisplay = widgets.CoreDisplay(None)

        # Setup Splitters to divide the GUI into quadrants
        self.master_split = QSplitter()
        self.left_split = QSplitter()
        self.right_split = QSplitter()
        self.top_left_split = QSplitter()
        self.top_right_split = QSplitter()
        self.bottom_left_split = QSplitter()
        self.bottom_right_split = QSplitter()

        self.left_split.setOrientation(Qt.Vertical)
        self.right_split.setOrientation(Qt.Vertical)

        # Setup frames
        self.top_left_frame = QFrame()
        self.top_right_frame = QFrame()
        self.bottom_left_frame = QFrame()
        self.bottom_right_frame = QFrame()

        # Set the styling for each frame        
        self.top_left_frame.setFrameShape(QFrame.StyledPanel)
        self.top_right_frame.setFrameShape(QFrame.StyledPanel)
        self.bottom_left_frame.setFrameShape(QFrame.StyledPanel)
        self.bottom_right_frame.setFrameShape(QFrame.StyledPanel)

        # Create layouts to contain widgets inside each frame
        self.top_left_layout = QGridLayout()
        self.top_right_layout = QGridLayout()
        self.bottom_left_layout = QGridLayout()
        self.bottom_right_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.sliders_layout = QHBoxLayout()
        self.mox_sliders_layout = QVBoxLayout()
        self.uo2_sliders_layout = QVBoxLayout()

        # Setup the top left quadrant with a display for the materials
        self.materials_label = QLabel()
        self.materials_label.setMaximumSize(500, 350)
        self.materials_label.setPixmap(QPixmap('simulator_materials.png').scaled(self.materials_label.size(), Qt.KeepAspectRatio))
        self.materials_label.setAlignment(Qt.AlignCenter)
        self.top_left_layout.addWidget(self.materials_label, 0, 1)

        self.materials_legend_label = QLabel()
        self.materials_legend_label.setMaximumSize(325, 225)
        self.materials_legend_label.setPixmap(QPixmap('material_label_trans.png').scaled(self.materials_legend_label.size(), Qt.KeepAspectRatio))
        self.materials_legend_label.setAlignment(Qt.AlignCenter)
        self.top_left_layout.addWidget(self.materials_legend_label, 0, 0)
        self.top_left_frame.setLayout(self.top_left_layout)

        # Setup the bottom right quadrant with a display for keff convergence
        self.keff_label = QLabel()
        self.keff_label.setMaximumSize(1000, 375)
        self.setupLabelPixmap(self.keff_label, 'keff.png', \
                              self.bottom_right_layout, self.bottom_right_frame)

        # Setup the top right quadrant with a display for the fluxes
        self.flux7_label = QLabel()
        self.flux7_title_label = QLabel('Thermal Flux: Low Energy Neutrons')
        self.flux7_label.setMaximumSize(500, 350)
        self.flux7_label.setPixmap(QPixmap('fsr-flux-group-7.png').scaled(self.flux7_label.size(), Qt.KeepAspectRatio))
        self.flux7_label.setAlignment(Qt.AlignCenter)
        self.flux7_title_label.setAlignment(Qt.AlignCenter)
        self.top_right_layout.addWidget(self.flux7_label, 0, 1)
        self.top_right_layout.addWidget(self.flux7_title_label, 1, 1)

        self.flux1_label = QLabel()
        self.flux1_title_label = QLabel('Fast Flux: High Energy Neutrons')
        self.flux1_label.setMaximumSize(500, 350)
        self.flux1_label.setPixmap(QPixmap('fsr-flux-group-1.png').scaled(self.flux1_label.size(), Qt.KeepAspectRatio))
        self.flux1_label.setAlignment(Qt.AlignCenter)
        self.flux1_title_label.setAlignment(Qt.AlignCenter)
        self.top_right_layout.addWidget(self.flux1_label, 0, 0)
        self.top_right_layout.addWidget(self.flux1_title_label, 1, 0)
        self.top_right_frame.setLayout(self.top_right_layout)


        self.coreDisplay.setMaximumSize(600,600)

        # Setup run button and reset button
        self.run_button = QPushButton("Run OpenMOC")
        self.reset_button = QPushButton("Reset")        

        # Setup the sliders for fuel enrichment
        self.uo2_slider = QSlider(Qt.Horizontal)
        self.uo2_slider.label = QLabel('UO2 enrichment: 3.5 %')
        self.uo2_slider.label.setAlignment(Qt.AlignCenter)
        self.uo2_slider.setMinimum(-50)
        self.uo2_slider.setMaximum(50)
        self.uo2_slider.setSliderPosition(0) 

        self.mox1_slider = QSlider(Qt.Horizontal)
        self.mox1_slider.label = QLabel('MOX-1 enrichment: 4.3 %')
        self.mox1_slider.label.setAlignment(Qt.AlignCenter)
        self.mox1_slider.setMinimum(-50)
        self.mox1_slider.setMaximum(50)
        self.mox1_slider.setSliderPosition(0) 

        self.mox2_slider = QSlider(Qt.Horizontal)
        self.mox2_slider.label = QLabel('MOX-2 enrichment: 7.0 %')
        self.mox2_slider.label.setAlignment(Qt.AlignCenter)
        self.mox2_slider.setMinimum(-50)
        self.mox2_slider.setMaximum(50)
        self.mox2_slider.setSliderPosition(0) 

        self.mox3_slider = QSlider(Qt.Horizontal)
        self.mox3_slider.label = QLabel('MOX-3 enrichment: 8.7 %')
        self.mox3_slider.label.setAlignment(Qt.AlignCenter)
        self.mox3_slider.setMinimum(-50)
        self.mox3_slider.setMaximum(50)
        self.mox3_slider.setSliderPosition(0) 

        # Setup the sliders for neutron poison enrichment
        self.poison_slider = QSlider(Qt.Horizontal)
        self.poison_slider.label = QLabel('Neutron poison enrichment $: 5.0 %')
        self.poison_slider.label.setAlignment(Qt.AlignCenter)
        self.poison_slider.setMinimum(-50)
        self.poison_slider.setMaximum(50)
        self.poison_slider.setSliderPosition(0)

        self.boron_slider = QSlider(Qt.Horizontal)
        self.boron_slider.label = QLabel('Soluble boron concentration: 1100.0 ppm')
        self.boron_slider.label.setAlignment(Qt.AlignCenter)
        self.boron_slider.setMinimum(-50)
        self.boron_slider.setMaximum(50)
        self.boron_slider.setSliderPosition(0)

        # Setup layout for bottom left quadrant with buttons and sliders
        self.uo2_sliders_layout.addWidget(self.uo2_slider)
        self.uo2_sliders_layout.addWidget(self.uo2_slider.label)
        self.uo2_sliders_layout.addWidget(self.poison_slider)
        self.uo2_sliders_layout.addWidget(self.poison_slider.label)
        self.uo2_sliders_layout.addWidget(self.boron_slider)
        self.uo2_sliders_layout.addWidget(self.boron_slider.label)
        self.mox_sliders_layout.addWidget(self.mox1_slider)
        self.mox_sliders_layout.addWidget(self.mox1_slider.label)
        self.mox_sliders_layout.addWidget(self.mox2_slider)
        self.mox_sliders_layout.addWidget(self.mox2_slider.label)
        self.mox_sliders_layout.addWidget(self.mox3_slider)
        self.mox_sliders_layout.addWidget(self.mox3_slider.label)
        self.buttons_layout.addWidget(self.run_button)
        self.buttons_layout.addWidget(self.reset_button)

        self.mox_sliders_frame = QFrame()
        self.mox_sliders_frame.setLayout(self.mox_sliders_layout)
        self.uo2_sliders_frame = QFrame()
        self.uo2_sliders_frame.setLayout(self.uo2_sliders_layout)
        self.sliders_layout.addWidget(self.mox_sliders_frame)
        self.sliders_layout.addWidget(self.uo2_sliders_frame)
        self.sliders_frame = QFrame()
        self.sliders_frame.setLayout(self.sliders_layout)

        self.buttons_frame = QFrame()
        self.buttons_frame.setLayout(self.buttons_layout)
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(10)
        self.progress.setValue(10)
        self.progress.label = QLabel('Idle')
        self.progress.setAlignment(Qt.AlignCenter)
        self.bottom_left_layout.addWidget(self.progress, 0,0)
        self.bottom_left_layout.addWidget(self.sliders_frame, 1, 0)
        self.bottom_left_layout.addWidget(self.buttons_frame, 2, 0)
        self.bottom_left_frame.setLayout(self.bottom_left_layout)

        # Connect buttons SIGNALs with actions
        self.connect(self.uo2_slider, SIGNAL('valueChanged(int)'), self.updateSliders)
        self.connect(self.mox1_slider, SIGNAL('valueChanged(int)'), self.updateSliders)
        self.connect(self.mox2_slider, SIGNAL('valueChanged(int)'), self.updateSliders)
        self.connect(self.mox3_slider, SIGNAL('valueChanged(int)'), self.updateSliders)
        self.connect(self.poison_slider, SIGNAL('valueChanged(int)'), self.updateSliders)
        self.connect(self.boron_slider, SIGNAL('valueChanged(int)'), self.updateSliders)
        self.connect(self.run_button, SIGNAL('clicked()'), self.runSimulation)
        self.connect(self.reset_button, SIGNAL('clicked()'), self.reset)

        # Add frames to each splitter
        self.right_split.addWidget(self.top_right_frame)
        self.right_split.addWidget(self.bottom_right_frame)
        self.left_split.addWidget(self.top_left_frame)
        self.left_split.addWidget(self.bottom_left_frame)

        self.master_split.addWidget(self.left_split)
        self.master_split.addWidget(self.right_split)
        self.setCentralWidget(self.master_split)


    def reset(self):
        '''
        Resets the slider positions
        '''
        self.uo2_factor = 3.5
        self.mox1_factor = 4.3
        self.mox2_factor = 7.0
        self.mox3_factor = 8.7
        self.poison_factor = 5.0
        self.boron_factor = 1100.0
        self.uo2_slider.label.setText('UO2 enrichment: ' + \
                                            str(self.uo2_factor) + ' %')
        self.mox1_slider.label.setText('MOX-1 enrichment: ' + \
                                            str(self.mox1_factor) + ' %')
        self.mox2_slider.label.setText('MOX-2 enrichment: ' + \
                                            str(self.mox2_factor) + ' %')
        self.mox3_slider.label.setText('MOX-3 enrichment: ' + \
                                            str(self.mox3_factor) + ' %')
        self.poison_slider.label.setText('Neutron poison enrichment: ' + \
                                            str(self.poison_factor) + ' %')
        self.boron_slider.label.setText('Soluble boron ppm: ' + \
                                            str(self.boron_factor) + ' ppm')
        self.uo2_slider.setSliderPosition(0)
        self.mox1_slider.setSliderPosition(0)
        self.mox2_slider.setSliderPosition(0)
        self.mox3_slider.setSliderPosition(0)
        self.poison_slider.setSliderPosition(0)
        self.boron_slider.setSliderPosition(0)


    def runSimulation(self):
        '''
        Connects to the smithwick, copies a materials HDF5 input file based on
        the user-defined enrichments, runs OpenMOC, copies back thermal flux
        plots and generates a keff convergence plot and finally repaints the GUI
        '''
        self.progress.setValue(0)
        self.progress.update()
        self.progress.repaint()
        self.writeMaterialsFile()

        self.openmoc_simulator.spawnSimulationThread()

        time.sleep(5.)

        # loop over progress update
        while(self.openmoc_simulator.isRunning()):
            self.progress.setValue(self.progress.value()+1)
            self.progress.update()
            self.progress.repaint()
            time.sleep(5.)

        self.setupLabelPixmap(self.keff_label, 'keff.png', \
                            self.bottom_right_layout, self.bottom_right_frame)

        flux1_pixMap = QPixmap('fsr-flux-group-1.png').scaled(self.flux1_label.size(),\
                                                            Qt.KeepAspectRatio)
        flux7_pixMap = QPixmap('fsr-flux-group-7.png').scaled(self.flux7_label.size(),\
                                                            Qt.KeepAspectRatio)
        self.flux1_label.setPixmap(flux1_pixMap)
        self.flux7_label.setPixmap(flux7_pixMap)

        self.flux1_label.setAlignment(Qt.AlignCenter)
        self.flux7_label.setAlignment(Qt.AlignCenter)

        self.top_right_layout.addWidget(self.flux1_label)
        self.top_right_layout.addWidget(self.flux7_label)

        self.top_right_frame.setLayout(self.top_right_layout)
        self.progress.setValue(10)
        self.progress.update()

        print 'finished simulation'


    def writeMaterialsFile(self):
        '''
        Writes a materials HDF5 input file for OpenMOC based on the enrichment
        slider settings. Must cast the slider domain of [-1,1] into a more
        useful range for modifying the enrichments
        '''

        uo2_factor = 0.0 + self.uo2_factor * 0.285714
        mox1_factor = 0.0 + self.mox1_factor * 0.232558
        mox2_factor = 0.0 + self.mox2_factor * 0.142857
        mox3_factor = 0.0 + self.mox3_factor * 0.114943
        poison_factor = 0.0 + self.poison_factor * 0.2
        boron_factor = 0.0 + self.boron_factor * 0.000909
        materials.writeMaterialsFile(uo2_factor, mox1_factor, mox2_factor, \
                                     mox3_factor, poison_factor, boron_factor)


    def updateSliders(self):
        '''
        Updates the slider label text with the current enrichment values
        '''

        self.convertSliderValues()

        self.uo2_slider.label.setText('UO2 enrichment: ' + \
                                            str(self.uo2_factor) + ' %')
        self.mox1_slider.label.setText('MOX-1 enrichment: ' + \
                                            str(self.mox1_factor) + ' %')
        self.mox2_slider.label.setText('MOX-2 enrichment: ' + \
                                            str(self.mox2_factor) + ' %')
        self.mox3_slider.label.setText('MOX-3 enrichment: ' + \
                                            str(self.mox3_factor) + ' %')
        self.poison_slider.label.setText('Neutron poison enrichment: ' + \
                                            str(self.poison_factor) + ' %')
        self.boron_slider.label.setText('Soluble boron ppm: ' + \
                                            str(self.boron_factor) + ' ppm')

    def convertSliderValues(self):
        '''
        Converts the location of the slider into an enrichment value.
        '''

        position = float(self.uo2_slider.sliderPosition())
        self.uo2_factor = 3.5 + 0.07 * position

        position = float(self.mox1_slider.sliderPosition())
        self.mox1_factor = 4.3 + 0.086 * position

        position = float(self.mox2_slider.sliderPosition())
        self.mox2_factor = 7.0 + 0.14 * position

        position = float(self.mox3_slider.sliderPosition())
        self.mox3_factor = 8.7 + 0.174 * position

        position = float(self.poison_slider.sliderPosition())
        self.poison_factor = 5.0 + 0.1 * position

        position = float(self.boron_slider.sliderPosition())
        self.boron_factor = 1100.0 + 22.0 * position


    def setupLabelPixmap(self, label, filename, layout, frame):
        '''
        Used to paint and repaint labels with new images, load them
        into a layout, and load that into a frame.
        '''

        pixMap = QPixmap(filename).scaled(label.size(), Qt.KeepAspectRatio)
        label.setPixmap(pixMap)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        frame.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()
