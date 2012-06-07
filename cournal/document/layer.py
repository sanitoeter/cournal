#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of Cournal.
# Copyright (C) 2012 Fabian Henze
# 
# Cournal is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Cournal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Cournal.  If not, see <http://www.gnu.org/licenses/>.

from xojtools import Layer as XojLayer

class Layer(XojLayer):
    def __init__(self, page, number, strokes=None):
        XojLayer.__init__(self, number=number)
        self.page = page
        self.strokes = strokes
        
        if self.strokes is None:
            self.strokes = []
            
    @classmethod
    def fromXojLayer(cls, layer, page):
        number = layer.number
        strokes = layer.strokes
        
        return cls(page, number, strokes=strokes)
