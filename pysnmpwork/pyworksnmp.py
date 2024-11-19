import re
import os
from typing import Union
import datetime

from pysnmpwork.data import *


class ConnectionSnmpSwitch:
    """
    Документация:
        Функция инициализации __init__():
            1. port -> udp port
            2. ip -> ip адрес коммутатора для подключения;
            3. community -> комьюнити доступа к snmp либо для чтения или записи;
    """
    DT_NOW = datetime.datetime.now()

    def __init__(self, port: int = None, ip: str = None, community: str = None):
        """

        :param port:
        :param ip:
        :param community:
        """
        if port is not None and ip is not None and community is not None:
            self.port: int = int(port)
            self.ip: str = str(ip)
            self.comm: str = str(community)

        else:
            raise Exception(
                f'Error:\n'
                f'port -> {port}\n'
                f'ip -> {ip}\n'
                f'community -> {community}'
            )

    # ======================= Функции проверок ==================================

    def __logged_ex(self, name_file: str = None, path_write: str = None):

        """
        :param name_file:
        :param path_write:
        :return:
        """

        if name_file is not None and path_write is not None:

            if os.path.exists(path_write):

                return f'{path_write}/{name_file}.txt'
            else:
                os.mkdir(path_write)
                return f'{path_write}/{name_file}.txt'

        elif name_file is None and path_write is None:

            return f'./logged.txt'

        elif name_file is not None and path_write is None:

            return f'./{name_file}.txt'

        elif name_file is None and path_write is not None:

            if os.path.exists(path_write):

                return f'{path_write}/logged.txt'
            else:

                os.mkdir(path_write)
                return f'{path_write}/logged.txt'

    def __return_type_ex(self, objects, result):

        if objects is None:
            return result
        else:
            return objects(result)
    # ======================= Конец функций ======================================

    # ======================= Запись логов ======================================
    def __logged(self, data_ex: str, name_file: str = None, path_write: str = None):

        file = self.__logged_ex(name_file, path_write)

        with open(file, 'a', encoding='UTF-8') as files:
            files.write(f'{self.DT_NOW.day}.{self.DT_NOW.month}.{self.DT_NOW.year} {self.DT_NOW.hour}:{self.DT_NOW.minute}'
                        f' - {data_ex}\n')

    # ======================= Конец записи ======================================

    # ======================= Запрос getcmd =====================================

    def snmp_requests(self, return_type: str = None, name_logged: str = None, path_logged: str = None, *args: tuple[str]) -> Union[list[list[str, str]], dict[str, str], tuple[list[str, str]]]:

        """
        :param return_type:
            Нужно указать тип данных в котором вы хотите получить результат:
                Доступные типы данных:
                    list, dict, tuple
                По умолчанию используется тип данных list
        :param name_logged:
             Название лога
        :param path_logged:
             Путь где будет хранится лог
        :param args:
             кортеж с элементами oid
        :return:
            list or dict or tuple
        """

        if len(args) > 0:

            result: list[list[str, str]] = list()
            auth = cmdgen.CommunityData(self.comm)
            gen = cmdgen.CommandGenerator()

            try:

                errorIndication, errorStatus, errorIndex, varTable = gen.nextCmd(
                    auth,
                    cmdgen.UdpTransportTarget((self.ip, 161)),
                    *[cmdgen.MibVariable(oid) for oid in args],
                    lookupMib=False,
                )
                try:
                    print(varTable)
                    for varBinds in varTable:
                        for oid, val in varBinds:
                            result.append([str(oid.prettyPrint()), str(val.prettyPrint())])

                    self.__logged(str('Success'), name_logged, path_logged)

                    return self.__return_type_ex(return_type, result)

                except Exception as e:
                    self.__logged(str(e), name_logged, path_logged)

            except Exception as e:
                self.__logged(str(e), name_logged, path_logged)

        else:
            raise Exception(
                f'Error:'
                f'Параметр args - {args} -> являeтся пустым поместите туда нужные аиды'
            )
    # ======================= Конец запроса getcmd =============================

    # =========================== Запросы getСmd ===============================

    def __generation_get(self, params: list):

        """
        :param params:
        :return:
        """

        result = list()

        for i in params:

            result.append(ObjectType(ObjectIdentity(str(i))))

        return result

    def __inter_get(self, params: list):

        """
        :param params:
        :return:
        """

        try:
           return getCmd(
                SnmpEngine(),
                CommunityData(self.comm, mpModel=1),
                UdpTransportTarget((self.ip, self.port)),
                ContextData(),
                *self.__generation_get(params)
            )
        except Exception as e:
            return e

    def __request_get(self, return_type, name_logged: str, path_logged: str, params: list) -> Union[list[list[str, str]], dict[str, str], tuple[list[str, str]]]:

        try:
            result: list[list[str, str]] = list()

            errorIndication, errorStatus, errorIndex, varBinds = next(self.__inter_get(params))

            for oid, val in varBinds:
                result.append([oid.prettyPrint(), val.prettyPrint()])

            return self.__return_type_ex(return_type, result)

        except Exception as e:
            self.__logged(str(e), name_logged, path_logged)

    # noinspection PyMethodMayBeStatic
    def user_request_get(self, return_type: str = None, name_logged: str = None, path_logged: str = None, params: list[str] = None):

        """
        :param path_logged:
        :param name_logged:
        :param return_type:
        :param params:
            Принимает значение словарь list[str]
        :return:
        """
        if params is not None:
            return self.__request_get(return_type, name_logged, path_logged, params)

        else:
            raise Exception('Error:\n'
                            'В функцию  user_request_get нужно передать параметр list[str]')

    # =========================== Конец  getСmd ===============================

    # =========================== Запросы setСmd ===============================

    def __generation_set(self, params: dict):

        """
        :param params:
        :return:
        """

        result = list()

        for i in params.values():

            s = re.findall(r'\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}', str(i[1]))

            if str(i[1]) not in s and type(i[1]) == str:
                result.append(ObjectType(ObjectIdentity(str(i[0])), OctetString(str(i[1]))))

            elif type(i[1]) == int:
                result.append(ObjectType(ObjectIdentity(str(i[0])), Integer(int(i[1]))))

            elif re.findall(r'\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}', str(i[1])):
                result.append(ObjectType(ObjectIdentity(str(i[0])), IpAddress(i[1])))
        return result

    def __inter_set(self, params: dict):

        """
        :param parms:
        :return:
        """

        try:
           return setCmd(
                SnmpEngine(),
                CommunityData(self.comm, mpModel=1),
                UdpTransportTarget((self.ip, self.port)),
                ContextData(),
                *self.__generation_set(params)
            )
        except Exception as e:
            return e

    def __request_set(self, name_logged: str, path_logged: str, params: dict):

        try:
            errorIndication, errorStatus, errorIndex, varBinds = next(self.__inter_set(params))

            for oid, val in varBinds:
                print(f'{oid.prettyPrint()} = {val.prettyPrint()}')

        except Exception as e:
            self.__logged(str(e), name_logged, path_logged)

    def user_request_set(self, name_logged: str = None, path_logged: str = None, params: dict[str: [str, Union[str, int]]] = None):

        """
        :param path_logged:
        :param name_logged:
        :param return_type:
        :param params:
        :param kwargs:
        :return:
        """

        if params is not None:
            return self.__request_set(name_logged, path_logged, params)

        else:
            raise Exception('Error:\n'
                            'В функцию  user_request_set нужно передать параметр dict[str: [str, Union[str, int]]]')
    # =========================== Конец  setСmd ===============================


