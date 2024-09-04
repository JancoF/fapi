from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recetas_espanolas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
fake = Faker('es_ES')

class Receta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ingredientes = db.Column(db.String(500), nullable=False)
    instrucciones = db.Column(db.String(1000), nullable=False)

@app.route('/recetas', methods=['GET'])
def obtener_recetas():
    try:
        recetas = Receta.query.all()
        if not recetas:
            return jsonify({"message": "No se encontraron recetas."}), 404
        return jsonify([{
            'id': r.id,
            'nombre': r.nombre,
            'ingredientes': r.ingredientes,
            'instrucciones': r.instrucciones
        } for r in recetas])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recetas/buscar', methods=['GET'])
def buscar_recetas():
    consulta = request.args.get('q')
    try:
        recetas = Receta.query.filter(
            Receta.nombre.contains(consulta) | Receta.ingredientes.contains(consulta)
        ).all()
        if not recetas:
            return jsonify({"message": f"No se encontraron recetas que coincidan con '{consulta}'."}), 404
        return jsonify([{
            'id': r.id,
            'nombre': r.nombre,
            'ingredientes': r.ingredientes,
            'instrucciones': r.instrucciones
        } for r in recetas])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def crear_recetas_falsas(num_recetas=200):
    platos_espanoles = [
        "Paella", "Tortilla Española", "Gazpacho", "Patatas Bravas", "Croquetas",
        "Fabada", "Cocido Madrileño", "Pulpo a la Gallega", "Pisto", "Albóndigas",
        "Calamares a la Romana", "Empanada", "Churros", "Ensaladilla Rusa", "Jamón Ibérico"
    ]
    
    ingredientes_espanoles = [
        "arroz", "tomate", "cebolla", "ajo", "pimentón", "aceite de oliva", "patata",
        "huevo", "jamón", "chorizo", "alubias", "garbanzos", "pimiento", "pescado",
        "mariscos", "pan", "queso", "vino", "azafrán", "perejil", "limón"
    ]

    for _ in range(num_recetas):
        nombre_base = random.choice(platos_espanoles)
        variacion = fake.word()
        receta = Receta(
            nombre=f"{nombre_base} {variacion}",
            ingredientes=', '.join(random.sample(ingredientes_espanoles, random.randint(5, 10))),
            instrucciones=fake.paragraph(nb_sentences=5)
        )
        db.session.add(receta)
    db.session.commit()

def inicializar_db():
    with app.app_context():
        db.create_all()
        if Receta.query.count() == 0:
            crear_recetas_falsas()
        print("Base de datos inicializada exitosamente.")

if __name__ == '__main__':
    inicializar_db()  # Asegúrate de que esta línea esté presente
    app.run(host='0.0.0.0', port=5000, debug=True)
