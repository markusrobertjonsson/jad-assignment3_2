"""
This file (test_models.py) contains the unit tests for the model XYData3.
"""
import unittest

from application import XYData3


class TestBasic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_new():
        """
        GIVEN a XYData3 database model
        WHEN a new XYData3 is created
        THEN check the description, owner, x, and y fields are defined correctly
        """
        xydata = XYData3(description='Descr', owner='MJ', x='1,2,3', y='4,5,6')
        assert xydata.description == 'Descr'
        assert xydata.owner == 'MJ'
        assert xydata.x == '1,2,3'
        assert xydata.y == '4,5,6'
