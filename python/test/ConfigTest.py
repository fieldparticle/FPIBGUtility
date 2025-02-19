import os
import sys
import inspect

# Add the shared directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir = os.path.join(os.path.dirname(current_dir), 'shared')
sys.path.append(shared_dir)

# Now import the modules
from FPIBGBase import FPIBGBase
from FPIBGConfig import FPIBGConfig

class ConfigTester:
    """
    Class for testing configuration file functionality
    """
    
    def __init__(self, ObjName):
        """Initialize with object name"""
        self.ObjName = ObjName
        print(f"Created {ObjName}")
    
    def Create(self, gobj):
        """
        Creates the ConfigTester object with logging
        Args:
            gobj: The global logging object
        """
        self.log = gobj
        self.log.log(
            inspect.currentframe().f_lineno,
            __file__,
            inspect.currentframe().f_code.co_name,
            self.ObjName,
            0,
            f"Created {self.ObjName} successfully."
        )
        
        # Create config object for testing
        self.config = FPIBGConfig("TestConfig")
        self.config.Create(self.log, "Particle.cfg")
        return 0
    
    def Open(self):
        """Opens any resources"""
        return 0
    
    def Close(self):
        """Closes any resources"""
        return 0
    
    def testObject(self, modNumber, dbglvl):
        """
        Test function that validates configuration functionality
        Args:
            modNumber: Module number to test
            dbglvl: Debug level (0-5, where 5 is most verbose)
        """
        if modNumber == 1 and dbglvl == 5:
            print(f"Running Mod {modNumber} Test")
            self.log.log(
                inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.ObjName,
                0,
                "Test 1 Success"
            )
            
            # Get configuration
            config = self.config.GetConfig()
            
            try:
                # Print and log each configuration value individually
                # Window settings
                print(f"Window title: {config.application.window.title}")
                print(f"Window width: {config.application.window.size.w}")
                print(f"Window height: {config.application.window.size.h}")
                
                # Basic simulation settings
                print(f"Frame delay: {config.application.frame_delay}")
                print(f"End frame: {config.application.end_frame}")
                print(f"Time step: {config.application.dt}")
                
                # Capture settings
                print(f"Capture name: {config.application.cap_name}")
                print(f"Capture number: {config.application.cap_num}")
                print(f"Capture frames: {config.application.cap_frames}")
                print(f"Frames buffered: {config.application.framesBuffered}")
                
                # Shader settings
                print(f"Shader output: {config.application.shader_out}")
                print(f"Fragment shader: {config.application.frag_kernParticle}")
                print(f"Fragment shader spv: {config.application.frag_kernParticlespv}")
                print(f"Vertex shader: {config.application.vert_kernParticle}")
                print(f"Vertex shader spv: {config.application.vert_kernParticlespv}")
                print(f"Compute shader: {config.application.comp_kernParticle}")
                print(f"Compute shader spv: {config.application.comp_kernParticlespv}")
                
                # Test settings
                print(f"Auto mode: {config.application.doAuto}")
                print(f"Auto wait: {config.application.doAutoWait}")
                print(f"Test file: {config.application.testfile}")
                print(f"Performance test: {config.application.perfTest}")
                
                # Test directories
                print(f"Test dir PQB: {config.application.testdirPQB}")
                print(f"Test dir CFB: {config.application.testdirCFB}")
                print(f"Test dir PCD: {config.application.testdirPCD}")
                print(f"Test dir DUP: {config.application.testdirDUP}")
                
                # Debug settings
                print(f"Compile shaders: {config.application.compileShaders}")
                print(f"Enable validation layers: {config.application.enableValidationLayers}")
                print(f"Stop on data: {config.application.stopondata}")
                print(f"Debug level: {config.application.debugLevel}")
                print(f"Report comp frames less than: {config.application.reportCompFramesLessThan}")
                print(f"Report graph frames less than: {config.application.reportGraphFramesLessThan}")
                print(f"Frames in flight: {config.application.framesInFlight}")
                
                # Print extensions
                print("Device extensions:")
                for ext in config.application.device_extensions:
                    print(f"  {ext}")
                
                print("Instance extensions:")
                for ext in config.application.instance_extensions:
                    print(f"  {ext}")
                
                print("Validation layers:")
                for layer in config.application.validation_layers:
                    print(f"  {layer}")
                
                print(f"Print extension: {config.application.printExtension}")
                print(f"Print dev limits: {config.application.printDevLimtits}")
                print(f"Verbose report: {config.application.verbose_rpt}")
                return 0
            except Exception as e:
                self.log.log(
                    inspect.currentframe().f_lineno,
                    __file__,
                    inspect.currentframe().f_code.co_name,
                    self.ObjName,
                    1,
                    f"Test 1 Failed: {str(e)}"
                )
                return 1
                
        elif modNumber == 2 and dbglvl == 5:
            print(f"Running Mod {modNumber} Test")
            self.log.log(
                inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.ObjName,
                0,
                "Test 2 Success"
            )
            return 0
        else:
            self.log.log(
                inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.ObjName,
                1,
                "Invalid test number"
            )
            return 1


def main():
    # Create base object as required
    gobj = FPIBGBase("GlobalBaseClass")
    gobj.Create("Particle.cfg", "FPIBG.log")
    
    # Create and test config
    tester = ConfigTester("ConfigTester")
    tester.Create(gobj.log)  # Pass just the log object, not the whole base object
    tester.Open()
    
    # Run tests with debug level 5
    print("\n=== Running Config Test 1 ===")
    result1 = tester.testObject(1, 5)
    print(f"Test 1 Result: {'Success' if result1 == 0 else 'Failed'}")
    
    print("\n=== Running Config Test 2 ===")
    result2 = tester.testObject(2, 5)
    print(f"Test 2 Result: {'Success' if result2 == 0 else 'Failed'}")
    
    # Cleanup
    tester.Close()
    gobj.Close()
    
    print("\n=== Testing Complete ===")
    overall = "Success" if result1 == 0 and result2 == 0 else "Failed"
    print(f"Overall Test Result: {overall}")

if __name__ == "__main__":
    main()