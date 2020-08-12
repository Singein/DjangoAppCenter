#!/usr/bin/env python
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.getcwd()))
from DjangoAppCenter.cli import entry

entry()
