#coding=utf-8

import serial
import os
import stat
import time


def configure():

    try :
        os.chmod("/dev/ttyUSB0",stat.S_IRWXO | stat.S_IRWXG |stat.S_IRWXU)
    except EnvironmentError as e :
        print(e)

    ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=60) # 使用USB连接串行口


    # #查询版本
    # ser.write(b'$PASHQ,VERSION\r\n')
    #
    # while True:
    #     print(ser.readline())




    if ser :
        print("串口打开成功")

        print("开始发送复位指令")

        # ser.write(b'$PASHS,NME,GGA,A,ON,0.1\r\n')
        # ser.write(b'$PASHS,NME,AVR,A,ON,0.1\r\n')
        # while True:
        #     print(ser.readline())
        #
        # return


        ser.read_all()
        ser.write("$PASHS,RST\r\n".encode("utf-8"))

        print("发送成功")

        print("开始查询结果")

        res = ""
        res = ser.readline()

        print(res)


        if res == b'$PMGNGO*1C\r\n' :
            print("复位成功")

        #    ser.write(b'$PASHQ,OPTION,EXP\r\n')



            # return
            print("配置板卡为DUO模式")

            ser.read_all()
            ser.write("$PASHS,SNS,DUO\r\n".encode("utf-8"))

            res = ser.readline()

            print(res)

            if res == b'$PASHR,ACK*3D\r\n' :
                print("配置成功")

                print("查询板卡DUO模式")

                for i in range(10) :
                    ser.read_all()
                    ser.write("$PASHQ,SNS\r\n".encode("utf-8"))

                    xx = ser.readline()

                    print(xx)

                    if xx == b'$PASHR,SNS,DUO,0*54\r\n' :
                        print("配置成功")

                        print("设置GGA数据输出")
                        ser.write(b'\r\n')
                        ser.write(b'$PASHS,NME,GGA,A,ON,0.1\r\n')

                        while True :
                            res = ser.readline()
                            print(res)

                            res = res.decode()
                            print(res)

                            if res.startswith('$GPGGA') :
                                print(res)
                                print("配置成功")

                                print("设置AVR数据输出")
                                ser.write(b'\r\n')
                                ser.write(b'$PASHS,NME,AVR,A,ON,0.1\r\n')

                                while True:
                                    res = ser.readline()
                                    # print(res)

                                    res = res.decode()
                                    print(res)

                                    if res.startswith('$PTNL,AVR'):
                                        print(res)
                                        print("配置成功")

                                        print("保存配置")
                                        ser.write(b'\r\n')
                                        ser.write(b'$PASHS,PWR,OFF*43\r\n')

                                        print(res)
                                        if ser.readline() == b'$PASHR,ACK*3D\r\n' :
                                            print("保存成功  请重新上电后输入任意键")
                                            a = input("input:")

                                            gga = 0
                                            avr = 0

                                            ser.read_all()

                                            while True:
                                                data = ser.readline()

                                                print(data)

                                                if data.decode().startswith("$GPGGA") :
                                                    gga = 1
                                                if data.decode().startswith("$PTNL,AVR") :
                                                    avr = 1

                                                if gga == 1 and avr == 1 :
                                                    print("成功---------------")
                                                    return

                                        else:
                                            print("保存失败")



                    time.sleep(1)

                print("配置失败")


            else :
                print("配置失败")

        else :
            print("复位失败")


    else :
        print("串口打开失败")







if __name__ == "__main__" :

    print("mb2 ....")

    configure()







