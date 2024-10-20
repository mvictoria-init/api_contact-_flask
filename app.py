from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contacts.db"
db = SQLAlchemy(app)

# create models of db 
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'phone' : self.phone,
        }

# create table
with app.app_context():
    db.create_all()
    
# create routes
@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify({ 'contacts' : [contact.serialize() for contact in contacts]})

@app.route('/contacts', methods=['POST'])
def create_contacts():
    data = request.get_json()
    contact = Contact(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(contact)
    db.session.commit()
    return jsonify({'mensaje': 'Contacto creado con exito',
                   'contact': contact.serialize()}), 201

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get_or_404(id)
    if not contact:
        return jsonify({'mensaje': 'Contacto no encontrado'}), 404
    return jsonify(contact.serialize())

@app.route('/contacts/<int:id>', methods=['PUT', 'PATCH'])
def update_contact(id):
    
    contact = Contact.query.get_or_404(id)
    
    data = request.get_json()
    
    if 'name' in data:
        contact.name = data['name']
    if 'email' in data:
        contact.email = data['email']    
    if 'phone' in data:
        contact.phone = data['phone']
    
    db.session.commit()
    
    return jsonify({'mensaje': 'Contacto actualizado con exito',
                   'contact': contact.serialize()}), 200
    
@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    if not contact:
        return jsonify({'mensaje': 'Contacto no encontrado'}), 404
    else:
        db.session.delete(contact)
        db.session.commit()
    return jsonify({'mensaje': 'Contacto eliminado con exito'})