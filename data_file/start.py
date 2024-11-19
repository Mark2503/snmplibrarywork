import os
from pysnmpwork.config import saves
from convertion.hexint import *
from pysnmpwork.collectionsdata import *


def oid_download_config(cfg: str, iptftp: str):
    """
    :param cfg:
    :param iptftp:
    :return:
    """

    params = {
        'parm': ['1.3.6.1.4.1.171.12.1.2.1.1.6.3', 3],
        'parm1': ['1.3.6.1.4.1.171.12.1.2.1.1.4.3', 2],
        'parm2': ['1.3.6.1.4.1.171.12.1.2.1.1.5.3', cfg],
        'parm3': ['1.3.6.1.4.1.171.12.1.2.1.1.7.3', 3],
        'parm4': ['1.3.6.1.4.1.171.12.1.2.1.1.3.3', iptftp],
        'parm5': ['1.3.6.1.4.1.171.12.1.2.1.1.9.3', 1],
        'parm6': ['1.3.6.1.4.1.171.12.1.2.1.1.8.3', 3],
    }

    return params


def distribution_port(port: list[int]) -> tuple[str, str]:
    """
    :param port:
    :return:
    """

    ports: list[int] = [25, 26, 27, 28]

    tagged: str = str([i for i in port if i in ports])[1:-1].replace(' ', '')
    untagged: str = str([i for i in port if i not in ports])[1:-1].replace(' ', '')
    all_port: str = str(port)[1:-1].replace(' ', '')

    return tagged, untagged, all_port


def create_settings_switch(name_valn, tagged, untagged, all_ports, newtag, newvaln):

    """
    :param newvaln:
    :param newtag:
    :param name_valn:
    :param tagged:
    :param untagged:
    :param all_ports:
    :return:
    """
    return f'# VLAN\n' \
           f'config vlan {name_valn} delete {all_ports}\n' \
           f'create vlan {newvaln} tag {newtag}\n' \
           f'config vlan {newvaln} add tagged {tagged}\n' \
           f'config vlan {newvaln} add untagged {untagged}\n'


def data_switch(ip_list: str, data_create, community: str, newtag, newvlan):

    """
    :param newvlan:
    :param newtag:
    :param ip_list:
    :param data_create:
    :param community:
    :return:
    """
    hi = HexInteger()

    sysDescr: str = 'SNMPv2-MIB::sysDescr.0'
    location: str = 'SNMPv2-MIB::sysLocation.0'
    firware: str = 'SNMPv2-SMI::enterprises.171.12.1.2.7.1.2.1'
    dot1qVlanStaticName: str = 'SNMPv2-SMI::mib-2.17.7.1.4.3.1.1.1'
    dot1qVlanStaticEgressPorts: str = 'SNMPv2-SMI::mib-2.17.7.1.4.3.1.2.1'

    for ip in ip_list:

        try:
            model: str = data_create.getCmd_data_switch(dict, ip, community)[sysDescr]
            loc: str = data_create.getCmd_data_switch(dict, ip, community)[location]
            fir: str = data_create.getCmd_data_switch(dict, ip, community)[firware].replace('*', '')
            name_vlan = data_create.getCmd_data_switch(dict, ip, community)[dot1qVlanStaticName]
            tagged_port = hi.get_ports(data_create.getCmd_data_switch(dict, ip, community)[dot1qVlanStaticEgressPorts])

            mod_model: str = re.findall(
                r'DES-\d{1,4}-\d{1,2}|DES-\d{1,4}/[A-Za-z0-9]+|DES-\d{1,4}',
                model)[0]

            tagged = distribution_port(tagged_port)[0]
            untagged = distribution_port(tagged_port)[1]
            all_ports = distribution_port(tagged_port)[2]

            result = create_settings_switch(name_vlan, tagged, untagged, all_ports, newtag, newvlan)
            data_create.create_config(f'{loc}.cfg', mod_model, fir, result)
            print(mod_model, loc, fir, name_vlan, tagged_port)
            data_create.reports(
                'Отчет о сформированных конфигах.txt',
                f'IP:{ip}, Модель:{mod_model}', f'Локация:{loc}'
            )

        except Exception as e:
            data_create.reports(
                'Отчет об ошибках.txt',
                f'Модель: {ip}', f'Ошибка: {e}'
            )


def download_cfg(data_ml, ip: list[str], tftp_ip: str, public, private):
    """
    :param private:
    :param public:
    :param tftp_ip:
    :param data_ml:
    :param ip:
    :return:
    """
    sysDescr: str = 'SNMPv2-MIB::sysDescr.0'
    location: str = 'SNMPv2-MIB::sysLocation.0'

    for i in ip:

        data = data_ml.getCmd_data_switch(dict, i, public)
        model = data[sysDescr]
        loc = data[location]

        params = oid_download_config(f'{loc}.cfg', tftp_ip)
        params.update(saves[model])
        data_dw = CollectionsData(None, None, params)

        print(f'# ================ {model}, {loc} ===================== #')

        data_dw.setCmd_data_switch(i, private)


def start():

    """
    :return:
    """

    new_community: list[str] = ['g3xW6UrJNEqwautRead', 'MmWWJSktY3EHBpWrite']

    sysDescr: str = '1.3.6.1.2.1.1.1'  # 'SNMPv2-MIB::sysDescr.0'
    location: str = '1.3.6.1.2.1.1.6'  # 'SNMPv2-MIB::sysLocation.0'
    firware = "1.3.6.1.4.1.171.12.1.2.7.1.2"  # 'SNMPv2-SMI::enterprises.171.12.1.2.7.1.2.1'
    dot1qVlanStaticName: str = '1.3.6.1.2.1.17.7.1.4.3.1.1'  # 'SNMPv2-SMI::mib-2.17.7.1.4.3.1.1.1'
    dot1qVlanStaticEgressPorts: str = '1.3.6.1.2.1.17.7.1.4.3.1.2'  # 'SNMPv2-SMI::mib-2.17.7.1.4.3.1.2.1'
    dot1qVlanStaticUntaggedPorts: str = '1.3.6.1.2.1.17.7.1.4.3.1.4'  # 'SNMPv2-SMI::mib-2.17.7.1.4.3.1.4.1'

    # Create config

    oid_create = [
        f'{sysDescr}.0', f'{location}.0', f'{firware}.1',
        f'{dot1qVlanStaticName}.1', f'{dot1qVlanStaticEgressPorts}.1'
    ]

    newtag: str = '12'
    newvaln: str = 'fl_pppoe'

    data_create = CollectionsData(None, None, oid_create)
    ip: list[str] = data_create.read_file("Устройств.csv")
    data_switch(ip, data_create, new_community[0], newtag, newvaln)

    # Download config
    tftp_ip: str = '10.6.0.1'

    oid_ml = [f'{sysDescr}.0', f'{location}.0']

    data_ml = CollectionsData(None, None, oid_ml)

    # os.startfile(data_ml.get_exe('tftpd32.exe'))

    download_cfg(data_ml, ip, tftp_ip, new_community[0], new_community[1])


if __name__ == '__main__':
    start()
