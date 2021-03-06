############################################################################
# This file is part of LImA, a Library for Image Acquisition
#
# Copyright (C) : 2009-2011
# European Synchrotron Radiation Facility
# BP 220, Grenoble 38043
# FRANCE
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
############################################################################
#=============================================================================
#
# file :        Lambda.py
#
# description : Python source for the Roper Scientific and its commands.
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                Pilatus are implemented in this file.
#
# project :     TANGO Device Server
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#         (c) - Bliss - ESRF
#=============================================================================
#
import PyTango
from Lima import Core
from Lima import Lambda as LambdaAcq
from Lima.Server import AttrHelper

class Lambda(PyTango.Device_4Impl):

    Core.DEB_CLASS(Core.DebModApplication, 'LimaCCDs')


#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    def __init__(self,*args) :
        PyTango.Device_4Impl.__init__(self,*args)
        #self.__Attribute2FunctionBase = {'distortion_correction': 'DistortionCorrection',
        #                                 }
        
        self.init_device()

#------------------------------------------------------------------
#    Device destructor
#------------------------------------------------------------------
    def delete_device(self):
        pass

#------------------------------------------------------------------
#    Device initialization
#------------------------------------------------------------------
    @Core.DEB_MEMBER_FUNCT
    def init_device(self):
        self.set_state(PyTango.DevState.ON)
        self.get_device_properties(self.get_device_class())

    @Core.DEB_MEMBER_FUNCT
    def getAttrStringValueList(self, attr_name):
        return AttrHelper.get_attr_string_value_list(self, attr_name)

    def __getattr__(self,name) :
        return AttrHelper.get_attr_4u(self, name, _LambdaCam)

class LambdaClass(PyTango.DeviceClass):

    class_property_list = {}

    device_property_list = {
        'config_path':
        [PyTango.DevString,
         "Path of the configuration file",[]],
        }

    cmd_list = {}

    attr_list = {
        'distortion_correction':
        [[PyTango.DevBoolean,
          PyTango.SCALAR,
          PyTango.READ]],
        'temperature':
        [[PyTango.DevDouble,
          PyTango.SCALAR,
          PyTango.READ]],
        'humidity':
        [[PyTango.DevDouble,
          PyTango.SCALAR,
          PyTango.READ]],
        'energy_threshold':
        [[PyTango.DevDouble,
          PyTango.SCALAR,
          PyTango.READ_WRITE]],        
        'high_voltage':
        [[PyTango.DevDouble,
          PyTango.SCALAR,
          PyTango.READ_WRITE]],        
        }

    def __init__(self,name) :
        PyTango.DeviceClass.__init__(self,name)
        self.set_type(name)

#----------------------------------------------------------------------------
# Plugins
#----------------------------------------------------------------------------
_LambdaCam = None
_LambdaInterface = None

def get_control(config_path = "",**keys) :
    global _LambdaCam
    global _LambdaInterface
    if _LambdaCam is None:
        _LambdaCam = LambdaAcq.Camera(config_path)
        _LambdaInterface = LambdaAcq.Interface(_LambdaCam)
    return Core.CtControl(_LambdaInterface)

def get_tango_specific_class_n_device():
    return LambdaClass,Lambda
