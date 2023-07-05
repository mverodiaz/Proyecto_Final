from flask import Flask,jsonify,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__) #Crea el objeto app de la clase Flask
CORS(app) #permite acceder desde el front al back

# configuro la base de datos, con el nombre el usuario y la clave
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user:password@localhost/proyecto_final'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@127.0.0.1/proyecto_final'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

# ---------fin configuracion-----------

#definimos la tabla
class PickUp(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100))
    precio=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    imagen=db.Column(db.String(400))
    def __init__(self,nombre,precio,stock,imagen):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.imagen = imagen

    #Si hay mas tablas para crear las definimos aca

with app.app_context():
    db.create_all() #Crea las tablas

class PickUpSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','stock','imagen')
    
PickUp_schema=PickUpSchema() #El objeto para traer un producto
PickUps_schema=PickUpSchema(many=True) #Trae muchos registro de producto



#Creamos los endpoint
#GET
#POST
#Delete
#Put

#Get endpoint del get
@app.route('/pickups',methods=['GET'])
def get_PickUps():
    all_pickups = PickUp.query.all() #heredamos del db.model
    result= PickUps_schema.dump(all_pickups) #lo heredamos de ma.schema
                                                #Trae todos los registros de la tabla y los retornamos en un JSON
    return jsonify(result)


@app.route('/pickups/<id>',methods=['GET'])
def get_PickUp(id):
    pickup=PickUp.query.get(id)
    return PickUp_schema.jsonify(pickup)   # retorna el JSON de un producto recibido como parametro




@app.route('/pickups/<id>',methods=['DELETE'])
def delete_PickUp(id):
    pickup=PickUp.query.get(id)
    db.session.delete(pickup)
    db.session.commit()
    return PickUp_schema.jsonify(pickup)   # me devuelve un json con el registro eliminado


@app.route('/pickups', methods=['POST']) # crea ruta o endpoint
def create_PickUp():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    imagen=request.json['imagen']
    new_PickUp=PickUp(nombre,precio,stock,imagen)
    db.session.add(new_PickUp)
    db.session.commit()
    return PickUp_schema.jsonify(new_PickUp)


@app.route('/pickups/<id>' ,methods=['PUT'])
def update_PickUp(id):
    pickup=PickUp.query.get(id)
 
    pickup.nombre=request.json['nombre']
    pickup.precio=request.json['precio']
    pickup.stock=request.json['stock']
    pickup.imagen=request.json['imagen']


    db.session.commit()
    return PickUp_schema.jsonify(pickup)

#Programa Principal
if __name__ == '__main__':
    app.run(debug=True, port=5000)