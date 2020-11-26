import re
from sql_alchemy import banco

class ServidorModel(banco.Model):
    listso = ['rhel', 'ubuntu', 'centos']
    so = [soformat.strip().lower() for soformat in listso]

    __tablename__ = 'servidores'

    servidor_id = banco.Column(banco.String, primary_key=True)
    hostname = banco.Column(banco.String(20))
    tipo = banco.Column(banco.String(10))
    so = banco.Column(banco.String(10))
    macaddress = banco.Column(banco.String(20))
    ipaddress = banco.Column(banco.String(20))
    netmask = banco.Column(banco.String(20))
    gateway = banco.Column(banco.String(20))

    def __init__(self, servidor_id, hostname, tipo, so, macaddress, ipaddress, netmask, gateway):
#        self.servidor_id = servidor_id.lower()
#        if len(self.servidor_id) == 12:
#            len(self.servidor_id)
#        else:
#            print("O nome do servidor precisa possuir 12 caracteres o valor atual e de {}".format(len(self.__hostname)))
#            exit(1)
#        self.tipo = tipo.lower()
#        self.so = so.lower()
#        if self.so in so:
#            self.so
#        else:
#            return {'message': 'Erro para cadastrar o servidor, o S.O : {} nao esta na lista '.format(self.so)}, 404
#        return servidor_id.json(), 404
#        self.hostname = hostname.lower()
#        if len(self.hostname) == 12:
#            len(self.hostname)
#        else:
#            return {'message': 'O nome do servidor precisa possuir 12 caracteres o valor atual e de {}'.format(len(self.__hostname))}
#        return servidor_id.json(), 404
        self.servidor_id = servidor_id
        self.hostname = hostname
        self.tipo = tipo
        self.so = so
        self.macaddress = macaddress
        self.macaddress = re.sub('[.:-]', '', self.macaddress).lower()
        self.macaddress = ''.join(self.macaddress.split())
        assert len(self.macaddress) == 12
        assert self.macaddress.isalnum()
        self.macaddress = ":".join(["%s" % (self.macaddress[i:i+2])
                                      for i in range(0, 12, 2)])
        self.macaddress
        self.ipaddress = ipaddress
        self.netmask = netmask
        self.gateway = gateway

    def json(self):
        return {
            'servidor_id': self.servidor_id,
            'hostname': self.hostname,
            'tipo': self.tipo,
            'so': self.so,
            'macaddress': self.macaddress,
            'ipaddress': self.ipaddress,
            'netmask': self.netmask,
            'gateway': self.gateway
            }

    @classmethod #decorador
    def find_servidor(cls, servidor_id):
        servidor = cls.query.filter_by(servidor_id=servidor_id).first()
        if servidor:
            return servidor
        return None

    def save_servidor(self):
        banco.session.add(self)
        banco.session.commit()

    def update_servidor(self, hostname, tipo, so, macaddress, ipaddress, netmask, gateway):
        self.hostname = hostname
        self.tipo = tipo
        self.so = so
        self.macaddress = macaddress
        self.ipaddress = ipaddress
        self.netmask = netmask
        self.gateway = gateway

    def delete_servidor(self):
        banco.session.delete(self)
        banco.session.commit()
