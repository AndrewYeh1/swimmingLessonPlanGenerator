import configparser


def getConfig():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def setConfig(config: configparser.ConfigParser):
    with open("config.ini", "w") as configFile:
        config.write(configFile)
