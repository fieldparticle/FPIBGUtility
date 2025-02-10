# Here are the things I need for Monday
# We cant use python test for local testing since I need to see the 
# output from each module local test when I review the code.
# So everyone needs to have test code in the test directory.
# It is important for my planning that we produce the output requested in the 
# module.

# In each test files, first thing, create the global base object as here:
from FPIBGBase import FPIBGBase
bc = FPIBGBase("FPIBGFrontEnd")
bc.Create()

# The in each of you classes you need a Create() method that takes
# the base class as in input as so
import inspect
def Create(self,FPIBGBase):
    self.bs = FPIBGBase
    self.bs.log.log(   inspect.currentframe().f_lineno,
                        __file__,
                        inspect.currentframe().f_code.co_name,
                        0,
                        "Created [my class name]")
    
# You should see a log file named FPIBGFrontEnd.log in the FPIBGUility directory
# With the output from that call.
    
# All classes also have the following functions. Just pass if they do nothing yet.
def Open():
    pass
def Close():
    pass


# For the TCPIP create a batch file that runs the server
# And wrap the client in a class.    

