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

from twisted.spread import pb
from twisted.internet import reactor
from twisted.cred import credentials

# 0 - none
# 1 - minimal
# 2 - medium
# 3 - maximal
DEBUGLEVEL = 3

HOSTNAME = "127.0.0.1"
PORT = 6524
USERNAME = "test"
PASSWORD = "testpw"

class Network(pb.Referenceable):
    def __init__(self):
        pb.Referenceable.__init__(self)
        self.document = None
    
    def set_document(self, document):
        self.document = document
        
    def connect(self):
        factory = pb.PBClientFactory()
        reactor.connectTCP(HOSTNAME, PORT, factory)
        def1 = factory.login(credentials.UsernamePassword(USERNAME, PASSWORD),
                             client=self)
        def1.addCallbacks(self.connected, self.connection_failed)

    def connected(self, perspective):
        debug(1, "Connected")
        # This perspective is a reference to our User object.  Save a reference
        # to it here, otherwise it will get garbage collected after this call,
        # and the server will think we logged out.
        self.perspective = perspective
        d = perspective.callRemote("joinDocument", "document1")
        d.addCallbacks(self.gotDocument, callbackArgs=["document1"])

    def connection_failed(self, reason):
        debug(0, "Connection failed due to:", reason.getErrorMessage())
        reactor.stop()

    def gotDocument(self, document, name):
        debug(2, "Started editing", name)
        self.remote_doc = document

    def remote_add_stroke(self, pagenum, stroke):
        self.document.pages[pagenum].strokes.append(stroke)
        self.document.pages[pagenum].somecallback(stroke)
        #debug(3, "I know the following strokes:\n", self.strokeList)
    
    def local_new_stroke(self, pagenum, stroke):
        d = self.remote_doc.callRemote("new_stroke", pagenum, stroke)
#        d.addCallbacks(self.local_testing_strokes_cb, callbackArgs=stroke1)

    def shutdown(self, result):
        reactor.stop()

def debug(level, *args):
    if level <= DEBUGLEVEL:
        print(*args)