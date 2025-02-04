import configparser
import os

class FPIBGConfig:
      def __init__(self):
            """
            Constructor for the FPIBGConfig object.
            Saves the path of the config as a variable.
            """
            self.configPath = os.path.join(get_repo_root(), "Particle.cfg")
      
      def GetStringField(self, field):
            print(find_line_with_substring(self.configPath, field))


def get_repo_root():
    """Gets the absolute path of the project root directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(current_dir, ".git")):
        current_dir = os.path.dirname(current_dir)
        if current_dir == "/":
            raise FileNotFoundError("Could not find .git directory")
    return current_dir

def find_line_with_substring(file_path, substring):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(substring):
                return line.strip()
    return None

def main():
      myConfig = FPIBGConfig()
      myConfig.GetStringField("name")

if __name__=="__main__":
    main()