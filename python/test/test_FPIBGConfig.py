from shared import FPIBGConfig

def test_name():
    cObj = FPIBGConfig()
    cDict = cObj.GetConfig()
    assert cDict.name == "particleOnly"