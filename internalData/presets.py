import configparser


def getConfig():
    config = configparser.ConfigParser()
    config.read("internalData/config.ini")
    return config


def setConfig(config: configparser.ConfigParser):
    with open("internalData/config.ini", "w") as configFile:
        config.write(configFile)
