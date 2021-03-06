#-******************************************************************************
#
# Copyright (c) 2016,
#  Sony Pictures Imageworks Inc. and
#  Industrial Light & Magic, a division of Lucasfilm Entertainment Company Ltd.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# *       Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# *       Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
# *       Neither the name of Sony Pictures Imageworks, nor
# Industrial Light & Magic, nor the names of their contributors may be used
# to endorse or promote products derived from this software without specific
# prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#-******************************************************************************

import unittest
from alembic.Abc import *
from alembic.AbcCoreAbstract import *

class LayerTest(unittest.TestCase):
    def testObjExport(self):
        """write a few oarchives to test layering on objects"""

        # writing the boring base
        layerA = OArchive( 'layerObjA.abc' )
        objAA = OObject( layerA.getTop(), "A" )
        objAAA = OObject( objAA, "A" )

        objAB = OObject( layerA.getTop(), "B" )
        objABA = OObject( objAB, "A" )
        objABB = OObject( objAB, "B" )

        objAC = OObject( layerA.getTop(), "C" )
        objACA = OObject( objAC, "A" )
        objACB = OObject( objAC, "B" )

        # writing the more exciting layer
        layerB = OArchive( 'layerObjB.abc' )
        objBA = OObject( layerB.getTop(), "A" )
        objBAA = OObject( objBA, "A" )
        objBAAB = OObject( objBAA, "B" )  # newly added
        objBAB = OObject( objBA, "B" ) # newly added

        md = MetaData()
        SetReplace(md, True)
        objBB = OObject( layerB.getTop(), "B", md)
        objBBC = OObject( objBB, "C" ) # with replace A and B will be gone

        md = MetaData()
        SetPrune(md, True)
        objBC = OObject( layerB.getTop(), "C", md )

    def testObjImport(self):
        """read the archives as layered to test layering on objects"""

        arch = IArchive(['layerObjB.abc', 'layerObjA.abc'])
        obj = arch.getTop()
        self.assertEqual(obj.getNumChildren(), 2)

        objA = IObject(obj, 'A')
        self.assertEqual(objA.getNumChildren(), 2)

        objAA = IObject(objA, 'A')
        self.assertEqual(objAA.getNumChildren(), 1)

        objAAB = IObject(objAA, 'B')
        self.assertEqual(objAAB.getNumChildren() == 0, objAAB.valid())

        objAB = IObject(objA, 'B')
        self.assertTrue(objAB.valid() and objAB.getNumChildren() == 0)

        objB = IObject(obj, 'B')
        self.assertTrue(objB.getNumChildren() == 1 and IObject(objB, 'C').valid())

    def testPropExport(self):
        """write a few oarchives to test property layering"""

        # writing the boring base
        layerA = OArchive( 'layerPropA.abc' )
        propAA = OCompoundProperty( layerA.getTop().getProperties(), "A" )
        propAAA = OCompoundProperty( propAA, "A" )

        propAB = OCompoundProperty( layerA.getTop().getProperties(), "B" )
        propABA = OCompoundProperty( propAB, "A" )
        propABB = OCompoundProperty( propAB, "B" )

        propAC = OCompoundProperty( layerA.getTop().getProperties(), "C" )
        propACA = OCompoundProperty( propAC, "A" )
        propACB = OCompoundProperty( propAC, "B" )

        # writing the more exciting layer
        layerB = OArchive( 'layerPropB.abc' )
        propBA = OCompoundProperty( layerB.getTop().getProperties(), "A" )
        propBAA = OCompoundProperty( propBA, "A" )
        propBAAB = OCompoundProperty( propBAA, "B" )  # newly added
        propBAB = OCompoundProperty( propBA, "B" ) # newly added

        md = MetaData()
        SetReplace(md, True)
        propBB = OCompoundProperty( layerB.getTop().getProperties(), "B", md)
        propBBC = OCompoundProperty( propBB, "C" )

        md = MetaData()
        SetPrune(md, True)
        propBC = OCompoundProperty( layerB.getTop().getProperties(), "C", md )

    def testPropImport(self):
        """read the archives as layered to test property layering"""

        arch = IArchive(['layerPropB.abc', 'layerPropA.abc'])
        prop = arch.getTop().getProperties()
        self.assertEqual(prop.getNumProperties(), 2)

        propA = ICompoundProperty(prop, 'A')
        self.assertEqual(propA.getNumProperties(), 2)

        propAA = ICompoundProperty(propA, 'A')
        self.assertEqual(propAA.getNumProperties(), 1)

        propAAB = ICompoundProperty(propAA, 'B')
        self.assertTrue(propAAB.getNumProperties() == 0 and propAAB.valid())

        propAB = ICompoundProperty(propA, 'B')
        self.assertTrue(propAB.valid() and propAB.getNumProperties() == 0)

        propB = ICompoundProperty(prop, 'B')
        self.assertTrue(propB.getNumProperties() == 1 and ICompoundProperty(propB, 'C').valid())
