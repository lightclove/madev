# -*- coding: utf-8 -*-
#!/usr/bin/env python2
########################################################################################################################
# Автор: lightclove@internet.ru
# Изменен: 18.04.2018
# Лицензия: MIT
########################################################################################################################
import ConfigParser
import os
import signal
import socket
import threading
import time
from io import open
import datetime
import init_generator
from KThread import KThread
import current_time
########################################################################################################################

print("CJSC \"INSTITUTE OF THE TELECOMMUNICATIONS\""
      "\nMANAGED MODULAR ROUTER DEVELOPMENT PROJECT\nAGENT MANAGEMENT MODULE\'")
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, "agent.conf")
config = ConfigParser.ConfigParser()
config.read(CONFIG_PATH)
#Генерируем ли значение
isWrite = config.get("generator", "isWrite")
if (isWrite == True):
    init_generator.write()  # Generate random values to write into config init.conf'
########################################################################################################################

def readProtoConfig(path="init.conf"):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content
########################################################################################################################

#print("Config file content: " + content)
clientPort = config.get("client", "clientPort")
clientAddress = config.get("client", "clientAddress")
serverAddress = config.get("server", "serverAddress")
serverPort = config.get("server", "serverPort")
delay8 = config.get("agent", "delay8")
delay9 = config.get("agent", "delay9")
delay77 = config.get("agent", "delay77")
command = config.get("agent", "command")
#isRun4ever = config.get("agent", "isRun4ever")
########################################################################################################################
localIP = config.get('ipc', 'localIP')
localPort = config.get('ipc', 'localPort')
dstIP = config.get('ipc', 'dstIP')
dstPort = config.get('ipc', 'dstPort')
fifoname = config.get('ipc', 'fifoname')

####################### DEBUG/TESTING ###############################################
tmplocalIP = "192.168.224.144" # Ubuntu VM host - b/o mkfifo() needs where - dev env
#tmplocalIP = "33.55.77.247" # Ubuntu VM host - b/o mkfifo() needs where - dev env
tmplocalPort = "5335" # Ubuntu VM host - b/o mkfifo() needs - dev env
tmpdstIP = "192.168.13.117" # Fake nihao receiver
#tmpdstIP = "33.55.77.247" # Fake nihao receiver
tmpdstPort = "12345" # Fake nihao receiver
####################### END OF DEBUG TESTING ########################################

def allow_fifo_access(fifoname, password):
    if not os.path.exists(fifoname): print "File \" " + fifoname +" is not exist"
    if os.system("chmod 777 " + fifoname) != 0 or \
            os.system("echo " + password + " sudo -S | chmod 777 " + fifoname) != 0 or\
                os.system("chmod 777 " + fifoname) != 0:
                    print "Access to the " + fifoname + " is ALLOWED"
    else:
        print "Access to the " + fifoname + " is NOT allowed"
########################################################################################################################

def send_HexInt_UDP(isRun4ever, ipaddr, port, command, bytesToSend, sendDelayInSecs):

    while True:
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        UDPClientSocket.bind(('0.0.0.0', int(serverPort)))
        serverAddressPort = (ipaddr, port)

        # если посылаем массив с командой в качестве первого элемента
        if(command != 0 or command != "0"):
            if (bytesToSend == "" or bytesToSend == " "):
                 intArray = []
            else:
                # получаем из строки со значениями hex-int массив(список) строк и конвертируем в массив из hex-int элементов
                intArray = [int(x, 16) for x in bytesToSend.strip().split(" ")]

            intArray.insert(0, int(command, 16))
            ba = bytearray(intArray)
        # посылаем строку, задав код "0"
        else:
            ba = bytesToSend.encode("utf-8")

        UDPClientSocket.sendto(ba, serverAddressPort)
        if command == "8" or command == 8: print "SEND 8 \n"\
                                                 + " with type of the message: " + str(type(ba)) +" "\
                                                 + " to the " + str(ipaddr) + ", "+ str(port) +" "\
                                                 + " at: " + current_time.current_time() + " "\
                                                 + " by the: " + threading.currentThread().getName()+" "
        if command == "9" or command == 9: print "SEND 9\n"\
                                                 + " with type of the message: " + str(type(ba))+" " \
                                                 + " to the " + str(ipaddr) + ", "+ str(port) +" "\
                                                 + " at: " + current_time.current_time() + " "\
                                                 + " by the: " + threading.currentThread().getName()+" "
        if command == "77" or command == 77: print "SEND 77\n"\
                                                 + " with type of the message: " + str(type(ba))+" " \
                                                 + " to the " + str(ipaddr) + ", "+ str(port) +" "\
                                                 + " at: " + current_time.current_time() + " "\
                                                 + " by the: " + threading.currentThread().getName()+" "

        # print(threading.currentThread().getName() + current_time.current_time() + " Data: "
        #      + str(ba) + " with type: " + str(type(ba)) + " sent to the: " + str(ipaddr) + ", "+ str(port))

        time.sleep(sendDelayInSecs)  # replace to 15'
        print "Delay between the sending is " + str(sendDelayInSecs) + " secs."
        print"##########################################################################################################"
        # Это условие для того, чтобы хотя бы один раз выполнились действия в теле цикла.

        if (isRun4ever == False):
            break
########################################################################################################################
def receivePackets(serverPort):
    UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    UDPClientSocket.bind(('0.0.0.0', int(serverPort)))
     # UDPClientSocket.listen(2)'
    print
    print(current_time.current_time() + threading.currentThread().getName()
          + ": Server accepting data on: " + unicode(UDPClientSocket.getsockname()))
    print

    while True:
        data, addr = UDPClientSocket.recvfrom(1024)

        if int(data[0].encode('hex'), 16) == 9:

            print current_time.current_time() + threading.currentThread().getName()
            print current_time.current_time() + "Code 9 Accepted!"
            print "STOP SENDING INIT REQUEST"

            print current_time.current_time() + "Initialization Accepted..."
            print current_time.current_time() + "Test requesting..."
            print
            time.sleep(int(delay9))
            # Реализация сценария остановки потока отсылки init()
            try:
                sendPackets_thread.kill()
            except NameError:
                print "NameError caught"
            finally:
                print current_time.current_time() + "TEST PASSED..OK"
                # Чтение буффера(файл "udevice_out_data", сформированного pipeReceiver и отсылка СУ обратно ответа
                # Отсылаем СУ содержимое файла "udevice_out_data" в который пишет модуль udevice через pipe
                send_HexInt_UDP(True, tmpdstIP, int(tmpdstPort), "9", readProtoConfig("udevice_out_data"), int(delay9))
                print current_time.current_time() + "Stop sending code 9 result..."  # set flag_test, 9 send test'
            print
            continue


        elif int(data[0].encode('hex'), 10) == 77:

            print current_time.current_time() + threading.currentThread().getName()
            print current_time.current_time() + "Code 77 Accepted!"
            print current_time.current_time() + "Switching to WORKING MODE"
            # Реализация сценария остановки потока отсылки init()
            try:
                sendPackets_thread.kill()
            except NameError:
                print "NameError caught"
            finally:
                print
                # Чтение буффера, сформированного pipeReceiver и отсылка ПМ-КУ обратно ответа
                # #senderPipe(True, fifoname, readProtoConfig("Protocol"),5, 10)
                print current_time.current_time() + " TEST PASSED..OK"
                time.sleep(int(delay77))
                # Чтение буффера(файл "udevice_out_data", сформированного pipeReceiver и отсылка ПМ-КУ обратно ответа
                # Отсылаем ПМ-КУ содержимое файла "udevice_out_data" в который пишет модуль udevice через pipe
                send_HexInt_UDP(True, tmpdstIP, int(tmpdstPort), "9", readProtoConfig("udevice_out_data"), int(delay77))

                print current_time.current_time() + "Stop sending code 77 result..."  # set flag_test, 9 send test'
            print
            continue

        #elif  int(data[0].encode('hex'), 16) == 8:
        #     print current_time.current_time() + threading.currentThread().getName()
        #     print current_time.current_time() + "Code 8 Accepted!"
        #     print current_time.current_time() + "Initialization..."
        #     time.sleep(int(delay8))  # 5'
        #     print "INITIALIZATION DELAY = " + delay8 + " secs"
        # try:
        #     sendPackets_thread.kill()
        # except NameError:
        #     print "NameError caught"
        # finally:
        # print
        else:
            print "INVALID RECEIVED PACKET. DROPPING IT AWAY "
            continue

        print(current_time.current_time() + threading.currentThread().getName() + ": From address: " + str(addr[0]) + " on port: " +
              str(serverPort) + " received udp-datagram data: " + str(data[0]).decode()) + " with type: " + str(type(data[0]))
                
        print "Press \"CTRL + C \ CTRL + Z\" to stop program..."
        print
        #rdata = data.strip().split(" ")
########################################################################################################################

def pipeReceiver(fifoname):

    while not os.path.exists(fifoname):
        # Cоздаем именованный канал системной утилитой mkfifo:
        os.mkfifo(fifoname)
        print "Named pipe file doesn't exist at \"" + fifoname + "\" waiting for creation and data sending"
        time.sleep(1)

    print current_time.current_time() + threading.currentThread().getName()
    print "### " + threading.currentThread().getName() + " ###"
    print "Starting receiving of the data process ..."   print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
          + " Waiting for the incoming messages at: \"" + fifoname + "\"")
    print

    while True:
        time.sleep(1)
        # блокируется до отправки данных в pipe, как только сообщение от клиента поступает в файл выводим его.
        pipein = open(fifoname, 'r')
        line = pipein.readline()

        print 'Receiver with pid = %d has got message: "%s" at %s' \
              % (os.getpid(), line, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        print "Press \"CTRL + C \ CTRL + Z\" to stop program..."
        print
        return line
########################################################################################################################
# CTRLZ.py
# Реализация прерывания по нажатию CTRL + C
def sigint_handler(signum, frame):
    print current_time.current_time() + 'CTRL + C Pressed, program is now stopped!'
    #os.abort() # Плохое решение, но работает в нашем случае, поскольку процесс уходит в фон и его иначе не завершить.
    #raise SystemExit(1)
    os.kill(os.getpid(),9)
signal.signal(signal.SIGINT, sigint_handler)
########################################################################################################################

if __name__ == '__main__':
    print
    print(u"Program started...")
    # Доступ к файлу "/tmp/agentfifo"
    allow_fifo_access("/tmp/agentfifo", "5")
    #
    pipeReceiver_thread = (KThread(target=pipeReceiver, args=([fifoname])))
    pipeReceiver_thread.setName("PIPE RECEIVER\'s THREAD")
    # #pipeReceiver_thread.setDaemon(True)
    pipeReceiver_thread.start()
    #
    receivePackets_thread = (KThread(target=receivePackets, args=([localPort])))
    receivePackets_thread.setName("UDP RECEIVER\'S THREAD:")
    #receivePackets_thread.setDaemon(True)
    receivePackets_thread.start()
    time.sleep(1)
    # Цикличная отправка пакета инициализации прерываемая флагом init8
    # Создали кастомный класс потока с функцией kill() для того чтобы можно было по нашему сценарию прервать поток отсылки пакета init
    # Выполняется это при получении "9" в методе receivePackets в
    sendPackets_thread = (KThread(target=  send_HexInt_UDP, args=([True, tmpdstIP, int(tmpdstPort), "8", readProtoConfig("init.conf"), 1])))
    sendPackets_thread.setName("UDP SENDER\'S THREAD:")
    sendPackets_thread.start()
    #def send_HexInt_UDP(isRun4ever, ipaddr, port, command, bytesToSend, sendDelayInSecs):
    #send_HexInt_UDP(True, tmpdstIP, int(tmpdstPort), "8", readProtoConfig("init.conf"), 1)
#######################################################################################################################################
    sendPackets_thread = (KThread(target=send_UDS())
    sendPackets_thread.setName("UDS SENDER\'S THREAD:")
    sendPacketsUDS_thread.start()
    sendPackets_thread = (KThread(target=receive_UDS())
    receivePacketsuds_thread.setName("UDS RECEIVER\'S THREAD:")
    sendPackets_thread.start()

