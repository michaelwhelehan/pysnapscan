'''
Created on 22 Oct 2015

@author: michaelwhelehan
'''
from .api import SnapScan


def get_snapscan(snapcode, api_key=None):
    """
    Utility function to return a SnapScan instance.
    """
    return SnapScan(snapcode, api_key)
