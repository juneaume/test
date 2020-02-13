import io
import fcntl
import datetime
import time

class atlas_i2c:
    long_timeout = 2.0  ## the timeout needed to query readings and calibrations
    short_timeout = .5  # timeout for regular commands
    default_bus = 1  # the default bus for I2C on the newer Raspberry Pis, certain older boards use bus 0
    default_address = 99  # the default address for the pH sensor
    current_addr = default_address
    read_attempts = 0
            
    def __init__(self, address=default_address, bus=default_bus):
            # open two file streams, one for reading and one for writing the specific I2C channel is selected with bus
            # it is usually 1, except for older revisions where its 0 wb and rb indicate binary read and write
            self.file_read = io.open("/dev/i2c-" + str(bus), "rb", buffering=0)
            self.file_write = io.open("/dev/i2c-" + str(bus), "wb", buffering=0)

            # initializes I2C to either a user specified or default address
            self.set_i2c_address(address)

    def set_i2c_address(self, addr):
            # set the I2C communications to the slave specified by the address The commands for I2C dev using the ioctl functions are specified in
            # the i2c-dev.h file from i2c-tools
            I2C_SLAVE = 0x703
            fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
            fcntl.ioctl(self.file_write, I2C_SLAVE, addr)
            self.current_addr = addr

    def write(self, cmd):
            # appends the null character and sends the string over I2C
            cmd += ""
            self.file_write.write(cmd.encode('UTF-8'))

    def read(self, num_of_bytes=31, read_attempts = read_attempts):
            # reads a specified number of bytes from I2C,then parses and displays the result
            res = self.file_read.read(num_of_bytes)  # read from the board
            # remove the null characters to get the response
            read_attempts += 1
            if read_attempts < 30:
                if type (res[0]) is str:

                        response = [i for i in res if i != '\x00']

                        timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

                        if ord(response[0]) == 1:  # if the response isnt an error
                        # change MSB to 0 for all received characters except the first and get a list of characters
                                char_list = list(map(lambda x: chr(ord(x) & ~0x80), list(response[1:])))
                                # NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, and you shouldn't have to do this!
                                
                                read_attempts = 0
                                
                                return (timestamp + "\t" + ''.join(char_list))
                        else:
                                time.sleep(self.long_timeout)
                                return self.read()
                else:
                        timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

                        if res[0] == 1:
                                char_list = list(map(lambda x: chr(x & ~0x80), list(res[1:])))
                                read_attempts = 0
                                return (str(timestamp) + "\t" + ''.join(char_list))
                        else:
                                time.sleep(self.long_timeout)
                                return self.read()
            else:
                return "Resetting"

    def query(self, string):
    # write a command to the board, wait the correct timeout, and read the response
            self.write(string)

            # the read and calibration commands require a longer timeout
            if((string.upper().startswith("R")) or (string.upper().startswith("CAL"))):
                    time.sleep(self.long_timeout)
            else:
                    time.sleep(self.short_timeout)

            return self.read()

    def close(self):
            self.file_read.close()
            self.file_write.close()