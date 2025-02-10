import configparser
import os
import libconf
import io

class FPIBGConfig:
    def __init__(self):
        """
        Constructor for the FPIBGConfig object.
        Saves the path of the config as a variable.
        Saves the configuration information as a dictionary.
        """
        self.configPath = os.path.join(get_repo_root(), "Particle.cfg")
        with io.open(self.configPath) as f:
            self.config = libconf.load(f)
    
    def GetConfig(self):
        """
        Function to retreive the config object.
        This object contains all of the data from the configuration file as a dictionary.
        """
        return self.config


def get_repo_root():
    """Gets the absolute path of the project root directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(current_dir, ".git")):
        current_dir = os.path.dirname(current_dir)
        if current_dir == "/":
            raise FileNotFoundError("Could not find .git directory")
    return current_dir