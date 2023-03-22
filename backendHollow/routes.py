from flask import Response, request, jsonify, session, render_template
from backendHollow import app, mongo
from backendHollow.forms import RegistrationForm, LoginForm
from bson import json_util
from bson.objectid import ObjectId
import secrets


@app.route("/csrf_token", methods = ["GET"])
def csrf_token():
    form = RegistrationForm()
    token = form.csrf_token.current_token
    session['my_csrf_token'] = token
    print("TOKEN ENVIADO AL FRONT:", session['my_csrf_token'])
    return jsonify({'csrfToken': token})


@app.route("/register", methods = ["POST"])
def register_user():
    form = RegistrationForm(request.form)
    
    if(form.validate_on_submit()):
        print(form.csrf_token.data, "SE HA REGISTADOOOOOOOOOO")
        return jsonify({'message': 'THE USER HAS BEEN SIGNED UP'})
    else:
        print("NO SE REGISTRO, TOKEN DEL FORMULARIO RECIBIDO: ", form.errors)
        return jsonify({'message': 'NO'})

@app.route("/", methods = ['POST', 'GET'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(f'ea {form.username.data} \n {form.email.data} \n {form.hidden_tag()}')
    else:
        print(f'No se pudo validar {form.errors}')

    return render_template("index.html", form = form)


@app.route("/characters", methods=['POST'])
def addCharacter():
    payload = request.json

    characterImgSrc = payload.get('imgSrc', "")
    characterName = payload.get('name', "")
    characterMainInfo = payload.get('mainInfo', "")
    characterSecondaryInfo = payload.get('secondaryInfo', "")

    if characterImgSrc and characterName and characterMainInfo:
        id = mongo.db.characters.insert_one(
            {"imgSrc": characterImgSrc, "name": characterName, "mainInfo": characterMainInfo, "secondaryInfo": characterSecondaryInfo}
        )
        
        response = {
            "message": "Character created succesfully",
            "status": "success",
            "data": {
                "id": str(id.inserted_id),
                "name": characterName,
                "imgSrc": characterImgSrc,
                "mainInfo": characterMainInfo,
                "secondaryInfo": characterSecondaryInfo
            }
        } 

        return response
    else:
        return bad_request()

@app.route("/characters", methods = ['GET'])
def getCharacters():
    characters = mongo.db.characters.find() #returns a BSON, and its a cursor
    response = json_util.dumps(characters)

    return Response(response, mimetype="application/json")

@app.route("/characters/<id>", methods = ['GET'])
def getCharacter(id):
    character_in_bson = mongo.db.characters.find_one({"_id": ObjectId(id)})
    character_in_bson_to_string = json_util.dumps(character_in_bson)

    return Response(character_in_bson_to_string, mimetype="application/json")

@app.route("/characters/<id>", methods = ["DELETE"])
def deleteCharacter(id):
    mongo.db.characters.delete_one({"_id": ObjectId(id)})
    
    response = jsonify({
        "message": f'The character with ID {id} was succefully deleted'
    })
    return response


@app.route("/characters/<id>", methods = ["PUT"])
def updateUser(id):
    characterToUpdate = mongo.db.characters.find_one({"_id": ObjectId(id)})

    characterName = request.json.get('name', characterToUpdate["characterName"])
    characterImgSrc = request.json.get('imgSrc', characterToUpdate["characterImgSrc"])
    characterMainInfo = request.json.get('mainInfo', characterToUpdate["characterMainInfo"])
    characterSecondaryInfo = request.json.get('secondaryInfo', characterToUpdate["characterSecondaryInfo"])

    mongo.db.characters.update_one({"_id": ObjectId(id)}, {"$set": {
        "name": characterName, 
        "imgSrc": characterImgSrc,
        "mainInfo": characterMainInfo,
        "secondaryInfo": characterSecondaryInfo
        }})
    
    response = jsonify({
        'message': f'The character with ID {id} has been updated successfully'
    })

    return response

@app.errorhandler(400)
def bad_request(error = None):
    response = jsonify({
        'message': "Bad Request: The request cannot be processed due to incorrect syntax or invalid data."
    })

    return response, 400
