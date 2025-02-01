from flask import Flask, request, jsonify
from flask_admin import Admin, BaseView, expose
import json

json_file = 'static/live/photos.json'

class JSONAdminView(BaseView):
    @staticmethod
    def read_json():
        with open(json_file, "r") as f:
            return json.load(f)

    @staticmethod
    def write_json(data):
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)

    @expose("/")
    def index(self):
        data = self.read_json()
        return self.render("admin/json_list.html", data=data)

    @expose("/create", methods=["POST"])
    def create(self):
        new_entry = request.json
        data = self.read_json()
        data.append(new_entry)
        self.write_json(data)
        return jsonify({"message": "Created successfully"}), 201

    @expose("/update/<int:item_id>", methods=["PUT"])
    def update(self, item_id):
        data = self.read_json()
        if item_id >= len(data):
            return jsonify({"error": "Item not found"}), 404

        data[item_id] = request.json
        self.write_json(data)
        return jsonify({"message": "Updated successfully"}), 200

    @expose("/delete/<int:item_id>", methods=["DELETE"])
    def delete(self, item_id):
        data = self.read_json()
        if item_id >= len(data):
            return jsonify({"error": "Item not found"}), 404

        data.pop(item_id)
        self.write_json(data)
        return jsonify({"message": "Deleted successfully"}), 200