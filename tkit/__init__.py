#from ._version import get_versions

#__version__ = get_versions()['version']
#del get_versions

# Import all classes from modules so that the following psuedo-code
#  will run.

#import wftkit
#...
#self.browse_file = wftkit.BrowseFile(self)
#self.radiobox = wftkit.Radiobox(self)

from browse_entry import *
from file_tree import *
from radiobox import *
from statusbar import *
