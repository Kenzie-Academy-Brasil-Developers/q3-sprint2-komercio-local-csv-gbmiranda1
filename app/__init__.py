
from ast import Return
from turtle import pos
from flask import Flask, request, jsonify
from os import getenv
import csv


app = Flask(__name__)

path = getenv("FILEPATH")

@app.get("/products")
def getProducts():
    arg_1 = int(request.args.get("page", 1))
    arg_2 = int(request.args.get("per_page", 3)) 
    result = []
    f = open(path, "r")
    reader = csv.DictReader(f)
    for line in reader:  
        result.append({ "id": int(line["id"]), "name": line["name"], "price": float(line["price"])})
    f.close()
    if arg_1 == 1 and arg_2 == 3:
        return jsonify(result[0:3]), 200
    else:
        return jsonify(result[(arg_2*arg_1)-arg_2:(arg_2*arg_1)])

@app.get("/products/<id>")
def getProductsId(id):
    result = []
    f = open(path, "r")
    reader = csv.DictReader(f)
    for line in reader:
        result.append(line)
    f.close()
    for i in result:
        if(i["id"] == id):
            return jsonify({"id": int(i["id"]), "name": i["name"], "price": float(i["price"])}), 200
    return jsonify({"error": "product id "+id+" not found"}), 404

@app.post("/products")
def postProducts():
    result = []
    openArq = open(path, "r")
    reader = csv.DictReader(openArq)
    for line in reader:
        result.append(line)
    openArq.close()
    id = int((result[(len(result)-1)])["id"])+1
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")
    fieldnames = ["id", "name", "price"]
    payload = {"id": int(id), "name": name, "price": float(price)}
    f = open(path, "a")    
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if(name and price):
        writer.writerow(payload)
        f.close()
        return payload, 201
    return {"error": "missing data"}, 422

@app.patch("/products/<id>")
def patchProducts(id):
    result = []
    openArq = open(path, "r")
    reader = csv.DictReader(openArq)
    for line in reader:
        result.append(line)
    openArq.close()
    fieldnames = ["id", "name", "price"]
    f = open(path, "w")    
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")
    f1 = open(path, "a")    
    writer = csv.DictWriter(f1, fieldnames=fieldnames)
    for i in result:
        if(i["id"] == id):
            if name:    
                i["name"] = name
            if price:
                i["price"] = price
            writer.writerow({"id":"id", "name": "name", "price": "price"})
            for i in result:
                writer.writerow(i)
            f.close()
            return {"id": int(i["id"]), "name": i["name"], "price": float(i["price"])}
    return {"error": "product id " + id + " not found"}, 404


@app.delete("/products/<id>")
def deleteProduct(id):
    result = []
    openArq = open(path, "r")
    reader = csv.DictReader(openArq)
    for line in reader:
        result.append(line)
    openArq.close()
    fieldnames = ["id", "name", "price"]
    f = open(path, "w")    
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    f1 = open(path, "a")    
    writer = csv.DictWriter(f1, fieldnames=fieldnames)
    bool = False
    valor = {}
    writer.writerow({"id":"id", "name": "name", "price": "price"})
    for i in result:
        if(i["id"] != id):
            writer.writerow(i)
            f.close()
        elif (i["id"] == id):
            bool = True
            valor = {"id": int(i["id"]), "name": i["name"], "price": float(i["price"])}
    if bool:
        return valor, 200
    return {"error": "product id " + id + " not found"}, 404
    