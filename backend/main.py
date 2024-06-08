from flask import request, jsonify
from config import app, db
from models import Contact


@app.route('/contacts', methods=['GET'])
def get_contacts():
    """
    Retrieve all contacts from the database and return them as JSON.

    Returns:
        A JSON response containing a list of contacts.
    """
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify(json_contacts)


@app.route('/create_contact', methods=['POST'])
def create_contact():
    """
    Create a new contact.

    This function handles the POST request to create a new contact in the database.
    It expects the following fields in the request's JSON payload:
    - firstName: The first name of the contact.
    - lastName: The last name of the contact.
    - email: The email address of the contact.

    Returns:
    - If all fields are provided, the function creates a new contact in the database and returns a JSON response
        with a success message and HTTP status code 201 (Created).
    - If any of the required fields are missing, the function returns a JSON response with an error message
        and HTTP status code 400 (Bad Request).
    - If an exception occurs during the creation of the contact, the function returns a JSON response with an error message
        and HTTP status code 500 (Internal Server Error).
    """
    first_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    email = request.json.get('email')

    if not first_name or not last_name or not email:
        return (jsonify({'error': 'Please provide all fields'}),
                400,)

    new_contact = Contact(first_name=first_name,
                          last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
        return (jsonify({'message': 'Contact created successfully!'}), 201)
    except Exception as e:
        return (jsonify({'error': f'Something went wrong. \n {str(e)}'}), 500)


@app.route('/update_contact/<int:id>', methods=['PATCH'])
def update_contact(id):
    """
    Update a contact with the given ID.

    Args:
        id (int): The ID of the contact to be updated.

    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
            - If the contact is found and updated successfully, the response will be {'message': 'Contact updated successfully!'} and the status code will be 200.
            - If the contact is not found, the response will be {'error': 'Contact not found!'} and the status code will be 404.
            - If an error occurs during the update process, the response will be {'error': 'Something went wrong. \n <error_message>'} and the status code will be 500.
    """
    contact = Contact.query.get(id)

    if not contact:
        return (jsonify({'error': 'Contact not found!'}), 404)

    data = request.json
    contact.first_name = data.get('firstName', contact.first_name)
    contact.last_name = data.get('lastName', contact.last_name)
    contact.email = data.get('email', contact.email)

    try:
        db.session.commit()
        return (jsonify({'message': 'Contact updated successfully!'}), 200)
    except Exception as e:
        return (jsonify({'error': f'Something went wrong. \n {str(e)}'}), 500)


@app.route('/delete_contact/<int:id>', methods=['DELETE'])
def delete_contact(id):
    """
    Delete a contact from the database.

    Args:
        id (int): The ID of the contact to be deleted.

    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
            - If the contact is found and successfully deleted, returns a JSON response with a success message and an HTTP status code of 200.
            - If the contact is not found, returns a JSON response with an error message and an HTTP status code of 404.
            - If an exception occurs during the deletion process, returns a JSON response with an error message and an HTTP status code of 500.
    """
    contact = Contact.query.get(id)

    if not contact:
        return (jsonify({'error': 'Contact not found!'}), 404)

    try:
        db.session.delete(contact)
        db.session.commit()
        return (jsonify({'message': 'Contact deleted successfully!'}), 200)
    except Exception as e:
        return (jsonify({'error': f'Something went wrong. \n {str(e)}'}), 500)


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
