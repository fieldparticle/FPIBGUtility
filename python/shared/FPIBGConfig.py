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
            lineString = find_line_with_substring(self.configPath, field)
            if lineString is None:
                  print("Error: element not found")
                  return None
            else:
                  fieldString = get_substring(lineString, '=', '\n')
                  print(fieldString)


def get_repo_root():
    """Gets the absolute path of the project root directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(current_dir, ".git")):
        current_dir = os.path.dirname(current_dir)
        if current_dir == "/":
            raise FileNotFoundError("Could not find .git directory")
    return current_dir

def find_line_with_substring(file_path, substring):
    """Helper Function to locate the field being requested by finding the line in the config file that begins with that field"""
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith(substring):
                return line.strip()
    return None

def get_substring(text, start_char, end_char):
    start_index = text.find(start_char) + 1
    end_index = len(text) - 1

    if start_index != -1 and end_index != -1:
        return text[start_index:end_index].strip()
    else:
        return None

def main():
      myConfig = FPIBGConfig()
      myConfig.GetStringField("cap_name")

if __name__=="__main__":
    main()