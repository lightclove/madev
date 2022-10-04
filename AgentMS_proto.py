# -*- coding: utf-8 -*-
# !/usr/bin/env python3.8
########################################################################################################################
# Программа реализации прототипа класса агента системы мониторинга - черновой вариант, hardcode, to the wastebin! =)
# реализует клиент-серверное межпроцессное и сетевое взамодействие:
#     - реализацию многопоточного клиент-серверного взаимодействия с системой мониторинга по проприетарному протоколу.
#     - реализацию многопоточного клиент-серверного взаимодействия по протоколу UDP;
#     - реализацию многопоточного клиент-серверного взаимодействия средствами Unix Domain Socket
#     - реализацию многопоточного клиент-серверного взаимодействия через Unix pipes
#     - реализацию многопоточного клиент-серверного взаимодействия с разделяемой памятью
#     - реализацию шифрования передаваемой информации, ее кодировнаие и декодирование
#     - реализацию работы с конфигурационными файлами для настройки параметров функционирования
#       программы агента системы мониторинга средствами ConfigParser и json
# Лицензия: MIT
# email: lightclove@internet.ru

########################################################################################################################
import datetime
import os
import signal
import threading
import time
import socket
import sys
from threading import Thread
import serial

import CKustomThread  # @ToDo Сделать класс управления потоками (чтобы можно было прибивать, в идеале на основе очереди)

########################################################################################################################
"""
    Функция вывода текущего времени.
"""


def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")


########################################################################################################################
"""
   Функция прерывания программы по нажатию сочетаний клавиш.
"""


# CTRLZ.py
# Реализация прерывания по нажатию CTRL + C
def sigint_handler(signum, frame):
    print('CTRL + C kes has been pressed, program is now interrupted!')
    # os.abort()
    # raise SystemExit(1)
    os.kill(os.getpid(), 9)


signal.signal(signal.SIGINT, sigint_handler)
########################################################################################################################

# ToDo реализовать паттерн Singleton для запуска агента в единственном экземпляре, чтобы занимал ресурсы
"""
    Класс агента системы мониторинга. 
    Запускается всегда в единственном экземпляре (паттерн Singleton)
"""


class AgentMS:

    def __init__(self):
        # self.uds_receiver()
        print(current_time() + ' Agent instance has been created.')
        # @ToDo здесь в дальнейшем определить используемые ниже переменные в json-конфиге !
        # @ToDo взять значения из конфига и определить здесь

        self.serverPort = os.getenv("SERVERPORT")
        self.sendDelayInSecs = os.getenv("SENDDELAYINSECS")  # 15
        self.rcvServerPort = os.getenv("RCVSERVERPORT")
        self.delay8 = os.getenv("D5")
        self.delay9 = os.getenv("D9")
        self.delay77 = os.getenv("D77")
        # путь к пайпу межпрограммного взаимодействия в Ос
        self.fifoname = '/tmp/agentFifo0'

    ########################################################################################################################
    # @ ToDo TEST IT !
    """        
        Метод отправки информации средстами протокола UDP. Возможно Будет выполняться в отдельном потоке программы агента СМ
    """

    def send_HexInt_UDP(self, isRun4ever, ipaddr, port, command, bytesToSend, sendDelayInSecs):

        while True:
            UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            UDPClientSocket.bind(('0.0.0.0', int(self.serverPort)))
            serverAddressPort = (ipaddr, port)

            # если посылаем массив с командой в качестве первого элемента
            if (command != 0 or command != "0"):
                if (bytesToSend == "" or bytesToSend == " "):
                    intArray = []
                else:
                    # получаем из строки со значениями hex-int массив(список) строк
                    # и конвертируем в массив из hex-int элементов:
                    intArray = [int(x, 16) for x in bytesToSend.strip().split(" ")]

                intArray.insert(0, int(command, 16))
                ba = bytearray(intArray)
            # посылаем строку, задав код "0"
            else:
                ba = bytesToSend.encode("utf-8")

            UDPClientSocket.sendto(ba, serverAddressPort)
            if command == "8" or command == 8:
                print("SEND 8 \n") \
                + " with type of the message: " + str(type(ba)) + " " \
                + " to the " + str(ipaddr) + ", " + str(port) + " " \
                + " at: " + current_time() + " " \
                + " by the: " + threading.currentThread().getName() + " "
            if command == "9" or command == 9:
                print("SEND 9\n") \
                + " with type of the message: " + str(type(ba)) + " " \
                + " to the " + str(ipaddr) + ", " + str(port) + " " \
                + " at: " + current_time() + " " \
                + " by the: " + threading.currentThread().getName() + " "
            if command == "77" or command == 77:
                print("SEND 77\n" \
                      + " with type of the message: " + str(type(ba)) + " " \
                      + " to the " + str(ipaddr) + ", " + str(port) + " " \
                      + " at: " + current_time() + " " \
                      + " by the: " + threading.currentThread().getName() + " " + time.sleep(
                    15))  # replace to self.sendDelayInSecs'
                print("Delay between the sending is " + str(sendDelayInSecs) + " secs.")
                print(
                    "#####################################################################################################")

            # Это условие для того, чтобы хотя бы один раз выполнились действия в теле цикла.
            if (isRun4ever == False):
                break

########################################################################################################################
    """
        Метод получения и обработки информации средстами протокола UDP. Будет выполняться в отдельном потоке программы агента СМ
    """

    # @ ToDo TEST IT ! UNDER CONSTRUCTION
    def receivePackets(self, rcvServerPort):
        UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        UDPClientSocket.bind(('0.0.0.0', int(rcvServerPort)))
        # UDPClientSocket.listen(2)'
        print()
        print(current_time() + threading.currentThread().getName()
              + ": Server accepting data on: " + UDPClientSocket.getsockname())
        print()

        while True:
            data, addr = UDPClientSocket.recvfrom(1024)

            if int(data[0].encode('hex'), 16) == 9:
                print(current_time() + threading.currentThread().getName())
                print(current_time() + "Code 9 Accepted!")
                print("STOP SENDING INIT REQUEST")
                print(current_time() + "Initialization Accepted...")
                print(current_time() + "Test requesting...")
                print(time.sleep(int(self.delay9)))
                # Реализация сценария остановки потока отсылки init()
                try:
                    pass
                    # sendPackets_thread.kill() #@ToDo sendPackets_thread
                except NameError:
                    print("NameError caught")
                finally:
                    print(current_time() + "TEST PASSED..OK")
                    # Чтение буффера(файл "udevice_out_data", сформированного pipeReceiver и отсылка ПМ-КУ обратно ответа
                    # Отсылаем ПМ-КУ содержимое файла "udevice_out_data" в который пишет модуль udevice через pipe
                    # send_HexInt_UDP(True, tmpdstIP, int(tmpdstPort), "9", readProtoConfig("udevice_out_data"), int(delay9)) #@ToDO sendPackets_thread
                    print(current_time() + "Stop sending code 9 result...")  # set flag_test, 9 send test'
                print()
                continue

            elif int(data[0].encode('hex'), 10) == 77:
                print(current_time() + threading.currentThread().getName())
                print(current_time() + "Code 77 Accepted!")
                print(current_time() + "Switching to WORKING MODE")
                # Реализация сценария остановки потока отсылки init()
                try:
                    pass
                    # sendPackets_thread.kill()#@ToDo sendPackets_thread
                except NameError:
                    print("NameError caught")
                finally:
                    print()
                    # Чтение буффера, сформированного pipeReceiver и отсылка ПМ-КУ обратно ответа
                    # #senderPipe(True, fifoname, readProtoConfig("Protocol"),5, 10)
                    print()
                    current_time() + " TEST PASSED..OK"
                    time.sleep(int(self.delay77))
                    # Чтение буффера(файл "udevice_out_data", сформированного pipeReceiver и отсылка ПМ-КУ обратно ответа
                    # Отсылаем ПМ-КУ содержимое файла "udevice_out_data" в который пишет модуль udevice через pipe
                    # send_HexInt_UDP(True, tmpdstIP, int(tmpdstPort), "9", readProtoConfig("udevice_out_data"), int(delay77))#@ToDO sendPackets_thread
                    pass
                    print(current_time() + "Stop sending code 77 result...")  # set flag_test, 9 send test')
                    print()
                    continue
            else:
                print("INVALID RECEIVED PACKET. DROPPING IT AWAY ")
                continue
        print(current_time() + threading.currentThread().getName() + ": From address: " + str(
            addr[0]) + " on port: " +
              str(rcvServerPort) + " received udp-datagram data: " + str(data[0]).decode()) + " with type: " \
        + str(type(data[0]))
        print("Press \"CTRL + C \ CTRL + Z\" to stop program...")
        print()

########################################################################################################################
    """
        Метод Unix Domain Socket receiver - реализация UDS-сервера. 
        По данной функции будет запускаться отдельный процесс/поток
        @param server_address - файл UDS-сокета
    """

    def uds_receiver(self, uds_socket_file):
        # uds_socket_file = './echo.socket'

        if os.path.exists(uds_socket_file):
            os.remove(uds_socket_file)

        print(current_time() + " Открываем UNIX сокет...")
        server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        server.bind(uds_socket_file)

        print(current_time() + " Слушаем входящие сообщения от клиента в сокет-файле: \"{}\"".format(uds_socket_file))
        while True:
            datagram = server.recv(1024)
            if not datagram:
                break
            else:
                print("-" * 20)
            print(datagram)
            if b"DONE" == datagram:
                break
        print(current_time() + " -" * 20)
        print(current_time() + "Выключение...")
        server.close()
        os.remove(uds_socket_file)
        print(current_time() + " Серверный процесс с использованием UNIX domain socket завершен.")

########################################################################################################################

    # @ToDo Метод заглушка, воможно будет выполняться в отдельном потоке
    def uds_receiver_handler(self, inputUDsinfo):
        pass
        # Какие-то действия по обработке
        # self.uds_sender(...parsedUDSInfo...)
        # или вызов
        # self.udp_sender(...parsedUDSInfo...)
        # или вызов
        # self.pipe_sender(...parsedUDSInfo...)
        # или вызов
        # uds_sender(...parsedUDSInfo...) # as a static method
        # return parsedUDSInfo

    """ 
        Создает клиент UNIX domain socket и отсылает сообщение uds_message 
        на сокет uds_address для взаиодействия с UDS-сервером 
    """

########################################################################################################################
    """
        Метод отправки информации на UNIX domain socket 
    """

    def uds_sender(self, manual_input, uds_message, uds_socket_file):
        # SOCKET_FILE = '/tmp/uds_socket'
        print(current_time() + " Подключение...")
        if os.path.exists(uds_socket_file):
            client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            client.connect(uds_socket_file)
            print(current_time() + " Процесс передачиз авершен")
            print(current_time() + " Нажмите Ctrl + C чтобы выйти.")
            print(current_time() + " Отправьте 'DONE' чтобы завершить серверный процесс UNIX domain socket.")
            while True:
                if manual_input == True:
                    try:
                        uds_message = input("> ")  #
                        if "" != uds_message:
                            print(current_time() + " ОТПРАВЛЕНО: %s" % uds_message)
                            client.send(uds_message.encode('utf-8'))
                            if "DONE" == uds_message:
                                print(current_time() + " Выключение клиентского процесса.")
                                break
                    except KeyboardInterrupt as k:
                        print(current_time() + " Выключение клиентского процесса.")
                        break
                else:
                    print(current_time() + " ОТПРАВЛЕНО сообщение на uds-сервер: %s" % uds_message)
                    client.send(uds_message.encode('utf-8'))
            client.close()
        else:
            print(current_time() + " Не могу соединиться c uds-сервером!")
        print(current_time() + " Выполнено")


########################################################################################################################
################################################ РАБОТА С UNIX-pipes ###################################################
########################################################################################################################
    # @ToDo Test it and check !
    """ 
        Метод предоставления доступа к пайпам или uds сокетам
    """

    def allow_fifo_access(self, fifoname, password):
        if not os.path.exists(fifoname): print("File \" " + fifoname + " is not exist")
        if os.system("chmod 777 " + fifoname) != 0 or \
                os.system("echo " + password + " sudo -S | chmod 777 " + fifoname) != 0 or \
                os.system("chmod 777 " + fifoname) != 0:
            print("Access to the " + fifoname + " is ALLOWED")
        else:
            print("Access to the " + fifoname + " is NOT allowed")

########################################################################################################################

    """ 
        Метод получения информации через Unix-pipe, запускается в отдельном потоке программы 
    """

    def pipe_receiver(self, fifoname):

        while not os.path.exists(fifoname):
            # Cоздаем именованный канал системной утилитой mkfifo:
            os.mkfifo(fifoname)
            print("Named pipe file doesn't exist at \"" + fifoname + "\" waiting for creation and data sending")
            time.sleep(1)

        print(current_time() + threading.currentThread().getName())
        print("### " + threading.currentThread().getName() + " ###")
        print("Starting receiving of the data process ...")
        print(str(datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S") + " Waiting for the incoming messages at: \"" + fifoname + "\""))
        print()

        while True:
            time.sleep(1)
            # блокируется до отправки данных в pipe, как только сообщение от клиента поступает в файл выводим его.
            pipein = open(fifoname, 'r')
            line = pipein.readline()

            print('Pipe receiver with pid = %d has got message: "%s" at %s') \
            % (os.getpid(), line, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            print("Press \"CTRL + C \ CTRL + Z\" to stop program...")
            print()
            return line

########################################################################################################################

    def pipe_receiver_handler(self, inputUDsinfo):
        pass
        # Какие-то действия по обработке
        # self.uds_sender(...parsedPipeInfo...)
        # или вызов
        # self.udp_sender(...parsedPipeInfo...)
        # или вызов
        # self.pipe_sender(...parsedPipeInfo...)
        # или вызов
        # uds_sender(...parsedPipeInfo...) # as a static method
        # return parsedPipeInfo

########################################################################################################################

    """ 
        Метод отправки информации через Unix-pipe 
    """

    def pipe_sender(self, path2pipe, message2send):
        os.write(path2pipe, message2send)
        print(current_time() + ' Message \"'
              + message2send + '\" has been sent to the pipe with the name: \"' + '\"' + message2send)


########################################################################################################################
########################################### Работа с разделяемой памятью ###############################################
########################################################################################################################
    # https://docs.python.org/3/extending/extending.html
    """
        Метод-обертка над Си-функцией создания сегмента памяти.
    """
    def create_shared_memory_segment(self):
        print("Shared memory segment were created at:")
        print("Вызов Cи-функции с созданием общего буффера памяти")
########################################################################################################################
    """
        Метод-обертка над Си-функцией чтения из сегмента памяти.
    """
    def read_from_shared_memory_segment(self):
        print("Reading from shared memory information about: ")
        print('Вызов Си-функции printf("Process read from segment: %s\n", shmem);')

########################################################################################################################
    """
        Метод-обертка над Си-функцией записи в сегмент памяти.
    """
    def write_to_shared_memory_segment(self):
        print("Вызов Cи-функции записи в общий буффер памяти memcpy(shmem, message2write, sizeof(message2write));")
        print("Information about were written to the shared memory at:")

########################################################################################################################
####################################### РАБОТА c UART. Сбор параметров мониторинга #####################################
########################################################################################################################
    # @ ToDo TEST IT !
    def testTransmitUART(self):
        ser = serial.Serial("/dev/ttyS0", 9600)  # Open port with baud rate
        while True:
            received_data = ser.read()  # read serial port
            time.sleep(0.03)
            data_left = ser.inWaiting()  # check for remaining byte
            received_data += ser.read(data_left)
            print(received_data)  # print received data
            ser.write(received_data)  # transmit data serially

########################################################################################################################
    # @ ToDo TEST IT !
    def readUART(self, ifaceFromRead, baudrate, quantChars2Read):
        # ser = serial.Serial("/dev/ttyAMA0")  # Open named port
        ser = serial.Serial(ifaceFromRead)  # Open named port
        # ser.baudrate = 9600  # Set baud rate to 9600
        ser.baudrate = baudrate  # Set baud rate to 9600
        # data = ser.read(10)  # Read ten characters from serial port to data #     ser.write(data)  # Send back the received data
        data = ser.read(
            quantChars2Read)  # Read specified quantity characters from serial port to data #     ser.write(data)  # Send back the received data
        ser.close()
        return data

########################################################################################################################
    # @ ToDo TEST IT !
    def writeUART(self, ifaceToWrite, baudrate, quantChars2Read, data2write):
        ser = serial.Serial("/dev/ttyAMA0")  # Open named port
        ser.baudrate = baudrate  # Set baud rate to 9600
        ser.write(data2write)  # Send back the received data
        ser.close()
########################################################################################################################
####################################### РАБОТА c procfs. Сбор параметров мониторинга ###################################
########################################################################################################################
    """
        Метод чтения инфы из procfs
    """

    def readProcfsData(self, procfs_input_parameter_to_monitor, ein):

        from procfs import Proc
        proc = Proc()
        # print(type(proc.loadavg)) # <class 'procfs.proc.loadavg'>
        # print(type(proc.net.dev.wlp2s0.receive.bytes)) # <class 'int'>
        # print(type(proc.meminfo.MemFree)) # <class 'int'>
        # print(type(proc.net.snmp.Udp)) # <class 'procfs.core.Dict'>

        if procfs_input_parameter_to_monitor == 'loadavg':
            print("Average processor's load: " + str(proc.loadavg))

        if procfs_input_parameter_to_monitor == 'eth_info':
            #ein = input("Enter your network interface's name: ")

            print("Specified network interface's usage, received bytes: ")
            #print(proc.net.dev)
            print(proc.net.dev.wlp2s0.receive.bytes)
            #print(proc.net.dev.ein.receive.bytes) #@ToDo !!! Подстановка ключа ein для поиска в словаре

        if procfs_input_parameter_to_monitor == 'mem_free_info':
            print('Free memory info: '+ str(proc.meminfo.MemFree))

        if procfs_input_parameter_to_monitor == 'udp_info':
            print('UDP usage statistics info: '+ str(proc.net.snmp.Udp))

########################################################################################################################
####################################### РАБОТА c sysfs. Сбор параметров мониторинга ####################################
########################################################################################################################
"""
Упрощенный интерфейс Python SysFS. 
"""
# @ ToDo TEST IT !
__all__ = ['sys', 'Node']

from os import listdir
from os.path import isdir, isfile, join, realpath, basename

class Node(object):
    __slots__ = ['_path_', '__dict__']

########################################################################################################################
    def __init__(self, path='/sys'):
        self._path_ = realpath(path)
        if not self._path_.startswith('/sys/') and not '/sys' == self._path_:
            raise RuntimeError('Using this on non-sysfs files is dangerous!')

        self.__dict__.update(dict.fromkeys(listdir(self._path_)))

########################################################################################################################
    def __repr__(self):
        return '<sysfs.Node "%s">' % self._path_

########################################################################################################################

    def __str__(self):
        return basename(self._path_)

########################################################################################################################
    def __setattr__(self, name, val):
        if name.startswith('_'):
            return object.__setattr__(self, name, val)

        path = realpath(join(self._path_, name))
        if isfile(path):
            with open(path, 'w') as fp:
                fp.write(val)
        else:
            raise RuntimeError('Cannot write to non-files.')

########################################################################################################################

    def __getattribute__(self, name):
        if name.startswith('_'):
            return object.__getattribute__(self, name)

        path = realpath(join(self._path_, name))
        if isfile(path):
            with open(path, 'r') as fp:
                return fp.read().strip()
        elif isdir(path):
            return Node(path)

########################################################################################################################

    def __setitem__(self, name, val):
        return setattr(self, name, val)

    def __getitem__(self, name):
        return getattr(self, name)

########################################################################################################################

    def __iter__(self):
        return iter(getattr(self, name) for name in listdir(self._path_))

#######################################################################################################################
################################################# Запуск программы #####################################################
########################################################################################################################

if __name__ == '__main__':
    print()
    print(current_time() + ' Program has been started...')
########################################################################################################################
# Создаем объект Агента мониторинга
    Agent_object = AgentMS()
########################################################################################################################
    Agent_object.testTransmitUART()                                           #@ToDo Test it ! Configure UART
    Agent_object.writeUART('/dev/ttyS0', 9600, 10, 'Hello beautiful world !') #@ToDo Test it ! Configure UART
    Agent_object.readUART('/dev/ttyS0', 9600, 10)                             #@ToDo Test it ! Configure UART
########################################################################################################################
    # ТЕСТИРУЕМ работу с sysfs, класс Node()
    sys = Node()
    print(sys.__dir__())
    print(sys.__dict__)
    # from sysfs import sys
    #
    # for bdev in sys.block:
    #     print('Information about logical drive:')
    #     print(bdev, str(int(bdev.size) / 1024 / 1024) + 'M') # TEST OK !
########################################################################################################################
    # ТЕСТИРУЕМ метод readProcfsData()
    Agent_object.readProcfsData('loadavg','wlp2s0') # TEST OK
    Agent_object.readProcfsData('eth_info','wlp2s0') # TEST OK
    Agent_object.readProcfsData('mem_free_info','wlp2s0') # TEST OK
    Agent_object.readProcfsData('udp_info','wlp2s0') # TEST OK
    Agent_object.readProcfsData('abracaddabra','wlp2s0') # TEST OK
########################################################################################################################
    # ТЕСТИРУЕМ метод uds_sender(self, uds_message, uds_address):
    # Для реализации метода uds_sender(self, uds_message, uds_address)
    # необходимо существование файла UDS-сокета, по пути, указанному в параметре uds_address
    # Если UDS-сервер не запущен, получим ошибку "[Errno 111] Connection refused"
    # Поэтому UDS-сервер необходимо запустить в отдельном потоке, ждущем подключение UDS клиента
    # Создаем поток подпрограммы для получения информации через UDS сокет
    # Данный поток будет обрабатывать/парсить информацию возможно появление @ToDo отдельных потоковых функций обработки
    receiverUDS_thread = Thread(target=Agent_object.uds_receiver, args=(['/tmp/uds_socket']))
    receiverUDS_thread.setName("UDS RECEIVER\'S THREAD:")
    receiverUDS_thread.start()
########################################################################################################################
    # Возможно появление @ToDo отдельных потоковых функций обработки:
    # uds_receiver_handler_thread = Thread(target=agent.uds_receiver_handler(), args=(['someInputUDSInfo']))
    # ----------------------------------- TESTING IN PROGRESS !!! -----------------------------------
    # тестирование функции передачи потока в сокет UDS:
    # agent.uds_sender(True, 'message to send', '/tmp/uds_socket') #
    # agent.uds_sender(True, 'message to send', '/tmp/uds_socket') #
    # agent.uds_sender(True, 'message to send', '/tmp/uds_socket') # @ToDo !
    # тестирование функции передачи потока в сокет UDS в отдельном потоке:
    # senderUDS_thread = (Thread(target=agent.uds_sender, args = ([False, 'message to send', '/tmp/uds_socket'])))
    # senderUDS_thread.setName("UDS SENDER\'S THREAD:")
    # senderUDS_thread.start()
    # ----------------------------------- TESTING IS DONE !!! ----------------------------------------
########################################################################################################################
    # Создаем поток подпрограммы для получения информации через pipe
    # Данный поток будет обрабатывать/парсить информацию возможно появление @ToDo отдельных потоковых функций обработки
    pipeReceiver_thread = (Thread(target=Agent_object.pipe_receiver, args=([Agent_object.fifoname])))
    pipeReceiver_thread.setName("PIPE RECEIVER\'s THREAD")
    pipeReceiver_thread.start()
########################################################################################################################
