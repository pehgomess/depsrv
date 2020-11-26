from sqlalchemy import (create_engine, MetaData, Column,
                        Table, Integer, String, DateTime, 
                        select, update, delete)
import argparse


def configdb():
    global user_table
    global engine
    engine = create_engine('sqlite:///hostname.db',echo=False)
    metadata = MetaData(bind=engine)
    user_table = Table('cadastrohostname', metadata, Column('hostname', String(20), primary_key=True))
    metadata.create_all()
    

class cadastrohostname(object):
    def __init__(self, hostname, action):
        self.hostname = hostname.lower()
        if self.hostname == "new":
            self.hostname
        elif len(self.hostname) == 12:
            len(self.hostname)
        else:
            print("O nome do servidor precisa possuir 12 caracteres o valor atual e de {}".format(len(self.hostname)))
            exit(1) 
        self.action = action.lower()

    @classmethod 
    def get_hostname(cls, hostname):
        s = select([user_table], user_table.c.hostname == hostname)
        for row in s.execute():
            if row:
                print("Existe {}".format(hostname))
                exit(0)

    @classmethod        
    def save_hostname(cls, hostname):
        conn = engine.connect()
        ins = user_table.insert()
        new_hostname = ins.values(hostname=hostname)
        conn.execute(new_hostname)

    @classmethod
    def create(cls, hostname):
        if cadastrohostname.get_hostname(hostname):
            print ("hostname: {}. existe".format(hostname))
        else:
            cadastrohostname.save_hostname(hostname)
            print("hostname: {}. cadastrado".format(hostname))

    def cadastrandoNovo(self):
        s = select([user_table])
        row = s.execute()
        last = row.fetchall()
        last = last[::-1]
        new = last[0]
        number = new[-1]
        lastrem = number[6:11]
        templatenome = "skylab"
        hostnumber = int(lastrem) +1
        sethostname = templatenome + str(hostnumber) + "p"
        cadastrohostname.save_hostname(sethostname)
        print("hostname: {}. cadastrado".format(sethostname))
        
    @classmethod 
    def remove(cls, hostname):
        print(hostname)
        pass 

    def run(self):
        if self.action == "insert":
            self.create(hostname)
#        elif self.action == "update":
#            print ("OK")
        elif self.action == "delete":
            self.remove(hostname)
        elif self.action == "select":
            self.get_hostname(hostname)
        elif self.action == "new" and self.hostname == "new":
            self.cadastrandoNovo()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cadastro de hostname')
    parser.add_argument('--action', action="store", dest="action", required=True)
    parser.add_argument('--hostname', action="store", dest="hostname", type=str)
    setname_args = parser.parse_args() 
    action = setname_args.action
    hostname = setname_args.hostname
    execute = cadastrohostname(hostname=hostname, action=action)
    configdb()
    execute.run()
    

