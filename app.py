from flask import Flask, jsonify, request

app = Flask(__name__)

datos = [{'id': 1, 'paciente_id': 1, 'mensaje': 'Cita programada', 'estado': 'ENVIADA'}, {'id': 2, 'paciente_id': 2, 'mensaje': 'Resultado disponible', 'estado': 'ENVIADA'}, {'id': 3, 'paciente_id': 3, 'mensaje': 'Factura pendiente', 'estado': 'PENDIENTE'}]

@app.get("/")
def inicio():
    return jsonify({
        "servicio": "Notificaciones",
        "estado": "activo",
        "recurso": "/notificaciones"
    })

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.get("/notificaciones")
def listar():
    return jsonify(datos), 200

@app.get("/notificaciones/<int:item_id>")
def obtener(item_id):
    item = next((x for x in datos if x["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Registro no encontrado"}), 404
    return jsonify(item), 200

@app.post("/notificaciones")
def crear():
    nuevo = request.get_json(silent=True)
    if not isinstance(nuevo, dict):
        return jsonify({"error": "Se requiere un cuerpo JSON válido"}), 400

    nuevo["id"] = max([x["id"] for x in datos], default=0) + 1
    datos.append(nuevo)
    return jsonify(nuevo), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
