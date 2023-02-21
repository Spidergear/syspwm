#!/usr/bin/env python
import os.path


class SysPWMException(Exception):
        pass

class SysPWM(object):

        chippath = "/sys/class/pwm/pwmchip0"

        def __init__(self,pwm):
                self.pwm=pwm
                self.pwmdir="{chippath}/pwm{pwm}".format(chippath=self.chippath,pwm=self.pwm)
                if not self.overlay_loaded():
                        raise SysPWMException("Need to add 'dtoverlay=pwm-2chan' to /boot/config.txt and reboot")
                if not self.export_writable():
                        raise SysPWMException("Need write access to files in '{chippath}'".format(chippath=self.chippath))
                if not self.pwmX_exists():
                        self.create_pwmX()
                return

        def overlay_loaded(self):
                return os.path.isdir(self.chippath)

        def export_writable(self):
                return os.access("{chippath}/export".format(chippath=self.chippath), os.W_OK)

        def pwmX_exists(self):
                return os.path.isdir(self.pwmdir)

        def echo(self,m,fil):
                #print "echo {m} > {fil}".format(m=m,fil=fil)
                with open(fil,'w') as f:
                        f.write("{m}\n".format(m=m))

        def create_pwmX(self):
                pwmexport = "{chippath}/export".format(chippath=self.chippath)
                self.echo(self.pwm,pwmexport)

        def enable(self,disable=False):
                enable = "{pwmdir}/enable".format(pwmdir=self.pwmdir)
                num = 1
                if disable:
                        num = 0
                self.echo(num,enable)

        def disable(self):
                return self.enable(disable=True)

        def set_duty_cycle(self,dc):
                # /sys/ iface, 2ms is 2000000
                # gpio cmd,    2ms is 200
                dc = dc * 10000
                duty_cycle = "{pwmdir}/duty_cycle".format(pwmdir=self.pwmdir)
                self.echo(dc,duty_cycle)

        def set_frequency(self,hz):
                #per = (1 / float(hz))
                #per *= 1000    # now in milliseconds
                #per *= 1000000 # now in.. whatever
                #per = int(per)
                period = "{pwmdir}/period".format(pwmdir=self.pwmdir)

if __name__ == "__main__":
        from time import sleep
        #SysPWM(1) is pin 7 on Banana Pi
        pwm1 = SysPWM(1)
        pwm1.set_frequency(1000000)
        #Duty cycle is set in %; 0 - 100%
        pwm1.set_duty_cycle(10)
        pwm1.enable()
        SLEE=5

        #SysPWM(2) is pin 26 on Banana Pi
        pwm2 = SysPWM(2)
        pwm2.set_frequency(1000000)
        #Duty cycle is set in %; 0 - 100%
        pwm2.set_duty_cycle(10)
        pwm2.enable()
        exit()

             
