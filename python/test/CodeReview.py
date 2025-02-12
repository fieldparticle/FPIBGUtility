# Here are our MOD 3 tasks
# The configuration file test needs to show the rest of us how to address
# each and every individual configuration item. I have updated the config 


# Even though we use Python test for local testing, I still need to see the 
# output from each module local test when I review the code.
# Test methods are contained in the class.
# It is important for my planning and the education of others 
# that we produce the output requested in the module.

# First include the FPIBGBase class in your test file.
from FPIBGBase import FPIBGBase
# Then create the global base object.
gobj = FPIBGBase("GlobalBaseClass")

# When you create a new class the constructor should take the name of the object.
# It can be like "DataObject", "ConfigObject", "tcpServ", or "tcpClient"
# Don't open files or do anything in the constructor except set the object name and call any
# superclasses.

# For example
myObj = MyClass("MyObject")

# and in the class
class MyClass
    def __init__ (self,ObjName):
         self.ObjName = ObjName


# Notice above that the name of the class is MyClass and the name of the 
# object is "MyObject"

# All classes also have the following functions. You can pass on open and close if they do nothing yet.
def Create(self, gobj):
    self.gobj = gobj;
    pass
def Open():
    pass
def Close():
    pass
def testObject(self,modNumber,DebugLevel):

# In the create method pass in the global object all of the data for you specific needs. 
myObj.Create(gobj,...)

# The open methid is where you open/create any files or communications.
myObj.Open()

# The close method closes all files or comuncations ports and does
# what ever cleanup there might be.
myObj.Close()

# In each of your classes Create() function, write to the log as shown below.
import inspect
def Create(self,gobj):
    self.log = gobj
    self.log.log(   inspect.currentframe().f_lineno,         # This is the line number 
                        __file__,                               # This is the file name
                        inspect.currentframe().f_code.co_name,  # This is the classs name
                        self.ObjName,                           # This is the object name
                        0,                                      # This is the return code
                        "Created [my class name] successfully.")# This is the code string
    
# You should see a log file named FPIBG.log in the FPIBGUility directory
# Look there to insure that you line was written

# The test object member should look like this.
# It has two parameters, the module number you are testing,
# and the debug level. The debug level is 0-5. Where 0 is silent and 5 is the most verbose.
# Your testing modules should be a five.
def testObject(self,modNumber,DebugLevel):
       def testObject(self,modNumber,dbglvl):
        if modNumber == 1 and dbglvl == 5:
            print(f"Running Mod" , modNumber , " Test")
            self.log.log(   inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            self.ObjName,
                            0,
                            "Test 1 Success")
            return 0
        elif modNumber == 2 and dbglvl == 5:
            print(f"Running Mod" , modNumber , " Test")
            self.log.log(   inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            self.ObjName,
                            0,
                            "Test 2 Success")
            return 0
        
    
        self.gobj.log(   inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            self.Moniker,
                            1,
                            "Invalid test number")

    
   