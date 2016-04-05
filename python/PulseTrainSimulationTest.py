##########################################################################
#                                                                        #
# Copyright (C) 2016 Carsten Fortmann-Grote                              #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is free software: you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

""" Test module for the PulseTrainSimulation class.

    @author : CFG
    @institution : XFEL
    @creation 20160405

"""
import h5py
import numpy
import os
import shutil
import unittest


import matplotlib
matplotlib.use('Qt4Agg')

from matplotlib import pyplot

from PulseTrainSimulation import PulseTrain
def testPulseSimulation():
    """ Testing the default construction of the class. """

    pulse_train = PulseTrain( photon_energy = 4.96e3,
                             pulse_duration = 3.0e-15,
                             pulse_separation = 200.0e-9,
                             )

    for i in range(10):
        temporal_shape, spectrum, time_stamp, count = pulse_train.pulse()

        time = temporal_shape[:,0]
        signal = temporal_shape[:,1]

        pyplot.plot( time, signal )
        pyplot.xlabel( 'time - timestamp (fs)')
        pyplot.ylabel( 'signal')

        pyplot.text(0.6*max(time),0.8*max(signal),"timestamp = %3.2e s" % (time_stamp))

        pyplot.show()



if __name__ == '__main__':
    testPulseSimulation()

