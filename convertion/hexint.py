class HexInteger:

    def __add_zero(self, strs):
        """
        Функция add_zero():
            :param strs:
                Добавляет нули
            :return:
                Возвращет число с нужным количеством знаков
        """
        return '0' + strs

    def __formats(self, strings: str) -> str:
        """
        Функция formats():
            :param strings:
                1.Принимает двоичное число
                2.Если число меньше 4 четырех знаков до добавлет не достающие нули
                3. Используеться в спомогательная функция add_zero
            :return:
                Возвращает нормализованное число
        """
        while len(strings) < 4:
            strings = self.__add_zero(strings)
        return strings

    def __bins(self, strings: str) -> str:

        """
        Функция bins():
            :param strings:
                Принимате шестнадцацеричное число  и конвертирует в двоичное число
            :return:
                Возвращает двоичное число 0001 или 1011 и т.д
        """

        return bin(int('0x' + strings, base=16)).replace('0b', '')

    def get_ports(self, hex_number: str = None) -> list[str]:
        """
        Функция get_ports():
            :param hex_number:
                1. Принимает шестнадцацеричное число
                2. Определяет по шестнадцатеричному числу номер порта коммутатора
            :return:
                Возвращает список -> result: list[str] портов которые находяться в определенном vlan
        """
        result: list[str] = list()
        counter = 0
        for strs in hex_number[2:]:
            for i, g in enumerate(self.__formats(self.__bins(strs))):
                counter += 1
                if g == '1':
                    result.append(counter)
        return result
