import sys
import os

# Add your app directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application