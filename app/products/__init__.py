from os import getenv
path = getenv("FILEPATH")
import csv
from flask import Flask, request, jsonify

def writeArqNotSub(payload):
    f = open(path, "a")    
    fieldnames = ["id", "name", "price"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writerow(payload)
    f.close()

def delete(id):
    result = readArq()
    fieldnames = ["id", "name", "price"]
    f = open(path, "w")    
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    f1 = open(path, "a")    
    writer = csv.DictWriter(f1, fieldnames=fieldnames)
    bool = False
    valor = {}
    writer.writerow({"id":"id", "name": "name", "price": "price"})
    for i in result:
        if(i["id"] != int(id)):
            writer.writerow(i)
            f.close()
        elif (i["id"] == int(id)):
            bool = True
            valor = {"id": int(i["id"]), "name": i["name"], "price": float(i["price"])}
    return (bool, valor)

def patch(id):
    result = readArq()
    for i in result:
        if(i["id"] == int(id)):
            print(i["price"])
            fieldnames = ["id", "name", "price"]
            f = open(path, "w")    
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            data = request.get_json()
            name = data.get("name")
            price = data.get("price")
            f1 = open(path, "a")    
            writer = csv.DictWriter(f1, fieldnames=fieldnames)
            if name:    
                i["name"] = name
            if price:
                i["price"] = float(price)
            writer.writerow({"id":"id", "name": "name", "price": "price"})
            for k in result:
                writer.writerow(k)
                f.close()
            return (True, {"id": int(id), "name": i["name"], "price": i["price"]})
    return (False, {"error": "product id " + id + " not found"})

def readArq():
    result = []
    f = open(path, "r")
    reader = csv.DictReader(f)
    for line in reader:  
        result.append({ "id": int(line["id"]), "name": line["name"], "price": float(line["price"])})
    f.close()
    return result