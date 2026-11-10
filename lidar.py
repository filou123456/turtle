import ydlidar
PORT = "/dev/ttyUSB0"
BAUD = 128000
SAMPLE_RATE = 8
SCAN_FREQ = 7.0
SINGLE_CHANNEL = False
LIDAR_TYPE = ydlidar.TYPE_TRIANGLE


class Lidar:

    def __init__(self, PORT, BAUD, LIDAR_TYPE, SAMPLE_RATE, SCAN_FREQ, SINGLE_CHANNEL):

        ydlidar.os_init()

        self.lidar = ydlidar.CYdLidar()

        self.lidar.setlidaropt(ydlidar.LidarPropSerialPort, PORT)
        self.lidar.setlidaropt(ydlidar.LidarPropSerialBaudrate, BAUD)
        self.lidar.setlidaropt(ydlidar.LidarPropLidarType, LIDAR_TYPE)
        self.lidar.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
        self.lidar.setlidaropt(ydlidar.LidarPropSampleRate, SAMPLE_RATE)
        self.lidar.setlidaropt(ydlidar.LidarPropScanFrequency, SCAN_FREQ)
        self.lidar.setlidaropt(ydlidar.LidarPropSingleChannel, SINGLE_CHANNEL)

        scan = ydlidar.LaserScan()




    def demarrer_scan(self):
        if not self.lidar.initialize():
            raise Exception("Erreur initialize")
        
        if not self.lidar.turnOn():
            raise Exception("Erreur turnOn")

    def arreter_scan(self):
        self.lidar.turnOff()

    def lire_donnees(self):
        if self.lidar.doProcessSimple(self.scan) and len(self.scan.points) > 0:
            return self.scan.points

        return []
