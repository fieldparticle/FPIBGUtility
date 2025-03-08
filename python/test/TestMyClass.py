
#############################################################################################
## Preamble to every script. Will append the shared directory                               #
import sys                                                                                  #  
import os                                                                                   #
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared')))   #
import getpass                                                                              #
print(getpass.getuser())                                                                    #
guser = getpass.getuser()                                                                   #    
# Now do imports                                                                            #
#############################################################################################
from FPIBGBase import *
from MyClass import *

# First instanciate a base class and name it
bc = FPIBGBase("GlobalBaseClass")

# Then call create with your configuration file and log file names. 
bc.Create("ParticleJB.cfg",'JBLog.log')
# instanciate your object and pass it a name. This namewill be used for logging.
myClass = MyClass("ExampleObject")
# Call the create function passing in the base class.
myClass.Create(bc)
# Call the open function if needed.
myClass.Open()
# Perform the object test.
myClass.testObject("Test Get All Config Items")
myClass.testObject("Log an Error")
# Close your class
bc.Close()

