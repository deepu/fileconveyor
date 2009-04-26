from transporter import *
from storages.FTPStorage import *


class TransporterFTP(Transporter):


    valid_settings = ImmutableSet(["host", "username", "password", "url", "port", "path"])
    required_settings = ImmutableSet(["host", "username", "password", "url"])


    def __init__(self, settings, callback):
        Transporter.__init__(self, settings, callback)

        # Validate settings.
        configured_settings = Set(self.settings.keys())
        Transporter.validate_settings(self, self.__class__.valid_settings, self.__class__.required_settings, configured_settings)

        # Fill out defaults if necessary.
        if not "port" in configured_settings:
            self.settings["port"] = 21
        if not "path" in configured_settings:
            self.settings["path"] = ""

        # Map the settings to the format expected by FTPStorage.
        location = "ftp://" + self.settings["username"] + ":" + self.settings["password"] + "@" + self.settings["host"] + ":" + str(self.settings["port"]) + self.settings["path"]
        self.storage = FTPStorage(location, self.settings["url"])


if __name__ == "__main__":
    import time

    def callbackfunc(filepath, url):
        print "CALLBACK FIRED: filepath=%s, url=%s" % (filepath, url)

    settings = {
        "host"     : "your ftp host",
        "username" : "your username",
        "password" : "your password",
        "url"      : "your base URL"
    }
    ftp = TransporterFTP(settings, callbackfunc)
    ftp.start()
    ftp.sync_file("transporter.py")
    ftp.sync_file("drupal-5-6.png")
    ftp.sync_file("subdir/bmi-chart.png")
    time.sleep(5)
    ftp.stop()