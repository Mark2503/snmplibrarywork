# from pysnmpwork.pyworksnmp import ConnectionSnmpSwitch

# cs = ConnectionSnmpSwitch(port=162, ip='10.200.0.7', community='publick')
# print(cs.snmp_requests(list, 'log', None, '1.'))


from pysnmp.hlapi import *

# Замените эти значения на соответствующие значения для вашего коммутатора
COMMUNITY = 'public'
IP = '10.200.0.7'
SNMP_PORT = 161

# Создаем объект SnmpEngine
snmp_engine = SnmpEngine()

# Определяем цель для запроса SNMP
target = UdpTransportTarget((IP, SNMP_PORT))

# Определяем контекст безопасности для запроса SNMP
context = CommunityData(COMMUNITY)

# Определяем OID для запроса
oid = ObjectType(ObjectIdentity('1.'))

# Выполняем запрос SNMP GET
errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(snmp_engine, context, target, ContextData(), oid)
)

# Проверяем наличие ошибок
if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    # Выводим результаты
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
