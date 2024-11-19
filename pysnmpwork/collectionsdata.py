import os
import sys
import re


from pysnmpwork.pyworksnmp import ConnectionSnmpSwitch


class CollectionsData:

    def __init__(self, name_logged: str = None, path_logged: str = None, oid=None):
        """

        :param name_logged:
        :param path_logged:
        :param oid:
        """
        self.nl = name_logged,
        self.pl = path_logged,
        self.oid = oid

    # ============ Работа с файлами ======================
    def get_path(self):

        """
        :return:
        """
        return os.path.split(sys.argv[0])[0]

    def get_exe(self, file: str) -> str:
        """
        Функция get_exe():
            Ишит  tftpd32.exe файл
            :return:
            Возвращает путь к файлу tftpd32.exe
        """

        return f'{self.get_path()}/{file}'

    def read_file(self, file: str) -> list[str]:
        """
        Функция read_file():
            Считывыет данные с csv файла
            :return:
                Возвращает список
        """
        result: list[str] = list()

        file = open(f'{self.get_path()}/{file}', 'r', encoding='UTF-8')

        for ip in file:

            slices: str = ip.split('\n')[0]
            if re.findall(r'\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}', slices):
                result.append(slices)

        file.close()

        return result

    # ============ Конец модулей ======================

    # ============ Модули запросов ====================

    def get_data_switch(self, return_type: str = None, ip: str = None, community: str = None):

        """
        Функция get_data_switch():
            Собирает данные с коммутатора
        :param return_type:
        :param ip:
        :param community:
        :return:
        """

        public = ConnectionSnmpSwitch(161, ip, community)

        try:

            return public.snmp_requests(return_type, self.nl[0], self.pl[0], *self.oid)

        except Exception as e:
            return e

    def getCmd_data_switch(self, return_type: str = None, ip: str = None, community: str = None):
        """

        :param return_type:
        :param ip:
        :param community:
        :return:
        """
        public = ConnectionSnmpSwitch(161, ip, community)

        try:
            return public.user_request_get(return_type, self.nl[0], self.pl[0], self.oid)

        except Exception as e:
            return e

    def setCmd_data_switch(self, ip: str = None, community: str = None):
        """

        :param return_type:
        :param ip:
        :param community:
        :return:
        """
        public = ConnectionSnmpSwitch(161, ip, community)

        try:
            return public.user_request_set(self.nl[0], self.pl[0], self.oid)

        except Exception as e:
            return e


def main():
    v = ['1.3.6.1.2.1.17.7.1.4.3.1.4.1', '1.3.6.1.2.1.1.6.0', '1.3.6.1.4.1.171.12.1.2.7.1.2.1']
    params = {
        'parm': ['1.3.6.1.4.1.171.12.1.2.1.1.6.3', 3],
        'parm1': ['1.3.6.1.4.1.171.12.1.2.1.1.4.3', 2],
        'parm2': ['1.3.6.1.4.1.171.12.1.2.1.1.5.3', 'bob.cfg'],
        'parm3': ['1.3.6.1.4.1.171.12.1.2.1.1.7.3', 3],
        'parm4': ['1.3.6.1.4.1.171.12.1.2.1.1.3.3', '10.6.0.20'],
        'parm5': ['1.3.6.1.4.1.171.12.1.2.1.1.9.3', 1],
        'parm6': ['1.3.6.1.4.1.171.12.1.2.1.1.8.3', 3],
    }
    data = CollectionsData(None, None, params)

    for i in ['10.20.24.23', '10.20.12.3']:
    #    print(data.get_data_switch(list, i, 'g3xW6UrJNEqwautRead'))
        #print(data.getCmd_data_switch(dict, i, 'g3xW6UrJNEqwautRead'))
        data.setCmd_data_switch(i, 'MmWWJSktY3EHBpWrite')


if __name__ == '__main__':
   main()