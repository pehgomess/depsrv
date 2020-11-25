from flask_restful import Resource, reqparse
from models.servidor import ServidorModel

class Servidores(Resource):
    def get(self):
        return {'servidores': [servidor.json() for servidor in ServidorModel.query.all()]}

class Servidor(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('hostname', type=str, required=True, help="O hostname e necessario para a criacao do servidor")
    argumentos.add_argument('tipo')
    argumentos.add_argument('so')
    argumentos.add_argument('macaddress', type=str, required=True, help="O macaddress e necessario para a criacao do servidor")
    argumentos.add_argument('ipaddress')
    argumentos.add_argument('netmask')
    argumentos.add_argument('gateway')

    def get(self, servidor_id):
        servidor = ServidorModel.find_servidor(servidor_id)
        if servidor:
            return servidor
        return {'message': 'servidor not found.'}, 404

    def post(self, servidor_id):
        if ServidorModel.find_servidor(servidor_id):
            return {"message": "servidor id '{}'. existe.".format(servidor_id)}, 400

        dados = Servidor.argumentos.parse_args()
        servidor = ServidorModel(servidor_id, **dados)
        try:
            servidor.save_servidor()
        except:
            return {'message': 'Erro ao salvar no banco de dados, validar a comunicacao com o banco.'}, 500
        return servidor.json()

    def put(self, servidor_id):
        dados = Servidor.argumentos.parse_args()
        servidor_encontrado = ServidorModel.find_servidor(servidor_id)
        if servidor_encontrado:
            servidor_encontrado.update_servidor(**dados)
            servidor_encontrado.save_servidor()
            return servidor_encontrado.json(), 200
        servidor = ServidorModel(servidor_id, **dados)
        try:
            servidor.save_servidor()
        except:
            return {'message': 'Erro ao salvar no banco de dados, validar a comunicacao com o banco.'}, 500
        return servidor.json(), 201

    def delete(self, servidor_id):
        servidor = ServidorModel.find_servidor(servidor_id)
        if servidor:
            try:
                servidor.delete_servidor()
            except:
                return {'message': 'Erro ao salvar no banco de dados, validar a comunicacao com o banco.'}, 500
            return {'message': 'servidor deletado.'}
        return {'message': 'servidor nao existe'}, 404
