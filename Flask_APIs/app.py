from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

tshirt_list = []

@app.route("/")
def home():
    return "Hello Flask!"


@app.route("/api/tshirts", methods=["GET"])
def get_tshirts():
    response = {
            "tshirts": tshirt_list
            }
    return make_response(jsonify(response), 200)


@app.route("/api/tshirts", methods=["POST"])
def add_tshirt():
    data = request.get_json()

    if data is None or "tshirt" not in data or "size" not in data:
        error_response = {
                "error": "You need to include 'tshirt' and 'size' fields in your request"
                }
        return make_response(jsonify(error_response), 400)

    new_tshirt = {
            "tshirt": data["tshirt"],
            "size": data["size"]
            }
    tshirt_list.append(new_tshirt)

    success_response = {
            "message": "Your new tshirt was added successfully!",
            "data": new_tshirt
            }
    return make_response(jsonify(success_response), 200)


@app.route("/api/tshirts/<string:colour>", methods=["POST"])
def add_tshirt_with_colour(colour):
    data = request.get_json()

    if data is None or "tshirt" not in data or "size" not in data:
        error_response = {
                "error": "Your request should include the tshirt and size fields"
                }
        return make_response(jsonify(error_response), 400)

    new_tshirt = {
            "tshirt": data["tshirt"],
            "size": data["size"],
            "colour": colour
            }
    tshirt_list.append(new_tshirt)
    success_response = {
            "message": "Tshirt was added successfully",
            "data": new_tshirt
            }
    return make_response(jsonify(success_response), 200)


if __name__ == "__main__":
    app.run(debug=True)
