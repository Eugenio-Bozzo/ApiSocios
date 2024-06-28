from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Rutas de la aplicación
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM Socios")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar Socios en la bdd
@app.route('/Agregar', methods=['POST'])
def addUser():
    Nombre = request.form['Nombre']
    Apellido = request.form['Apellido']
    Dni = request.form['Dni']
    Edad = request.form['Edad']
    Deporte = request.form['Deporte']

    if Nombre and Apellido and Dni and Edad and Deporte:
        cursor = db.database.cursor()
        sql = "INSERT INTO Socios (Nombre, Apellido, Dni, Edad, Deporte) VALUES (%s, %s, %s, %s, %s)"
        data = (Nombre, Apellido, Dni, Edad, Deporte)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

#Ruta para Borrar Socios en la bdd
@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM Socios WHERE Id_Socios=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

#Ruta para editar Socios en la bdd
@app.route('/Edit/<string:id>', methods=['POST'])
def edit(id):
    Nombre = request.form['Nombre']
    Apellido = request.form['Apellido']
    Dni = request.form['Dni']
    Edad = request.form['Edad']
    Deporte = request.form['Deporte']

    if Nombre and Apellido and Dni and Edad and Deporte:
        cursor = db.database.cursor()
        sql = "UPDATE Socios SET Nombre = %s, Apellido = %s, Dni = %s, Edad = %s, Deporte = %s WHERE Id_Socios = %s"
        data = (Nombre, Apellido, Dni, Edad, Deporte, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5500)