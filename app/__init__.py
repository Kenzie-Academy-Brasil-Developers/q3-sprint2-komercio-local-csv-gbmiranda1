
from flask import Flask, request, jsonify
from os import getenv
from app.products import patch, readArq, delete, writeArqNotSub


app = Flask(__name__)

path = getenv("FILEPATH")

@app.get("/products")
def getProducts():
    arg_1 = int(request.args.get("page", 1))
    arg_2 = int(request.args.get("per_page", 3)) 
    result = readArq()
    if arg_1 == 1 and arg_2 == 3:
        return jsonify(result[0:3]), 200
    else:
        return jsonify(result[(arg_2*arg_1)-arg_2:(arg_2*arg_1)])

@app.get("/products/<int:id>")
def getProductsId(id):
    result = readArq()
    for i in result:
        if(i["id"] == id):
            return jsonify({"id": int(i["id"]), "name": i["name"], "price": float(i["price"])}), 200
    return jsonify({"error": "product id "+id+" not found"}), 404

@app.post("/products")
def postProducts():
    result = readArq()
    id = int((result[(len(result)-1)])["id"])+1
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")
    payload = {"id": int(id), "name": name, "price": float(price)}
    if(name and price):
        writeArqNotSub(payload)
        return payload, 201
    return {"error": "missing data"}, 422

@app.patch("/products/<id>")
def patchProducts(id):
    result = patch(id)
    print(result)
    if result[0]:
        return result[1], 200
    return result[1], 404


@app.delete("/products/<id>")
def deleteProduct(id):
    result = delete(id)
    if result[0]:
        return result[1], 200
    return {"error": "product id " + int(id) + " not found"}, 404
    