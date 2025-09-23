from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql.cursors
from werkzeug.security import generate_password_hash, check_password_hash

# Inicialización de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'tu_llave_secreta_muy_segura' # Necesario para los mensajes flash

def obtener_conexion():
    """
    Establece la conexión con la base de datos.
    Asegúrate de cambiar los valores para que coincidan con tu configuración.
    """
    try:
        connection = pymysql.connect(host='localhost',
                                     # El puerto puede variar, 3306 es el predeterminado
                                     port=3339,
                                     user='root',
                                     password='', # Tu contraseña de MySQL
                                     database='proyecto_final', # El nombre de tu base de datos
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

@app.route("/")
def index():
    """Página principal, redirige al inicio de sesión."""
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Maneja el inicio de sesión de los usuarios."""
    if request.method == 'POST':
        username_email = request.form['username_email']
        password = request.form['password']

        conexion = obtener_conexion()
        if not conexion:
            flash('Error de conexión con el servidor. Inténtalo más tarde.', 'danger')
            return render_template('login.html')

        try:
            with conexion.cursor() as cursor:
                # Buscamos al usuario por email o por nombre de usuario (nombre_completo)
                sql = "SELECT * FROM usuarios WHERE email = %s OR nombre_completo = %s"
                cursor.execute(sql, (username_email, username_email))
                usuario = cursor.fetchone()

                if usuario and check_password_hash(usuario['password'], password):
                    # En una aplicación real, aquí crearías una sesión de usuario.
                    # Por ejemplo: session['user_id'] = usuario['id']
                    flash('¡Inicio de sesión exitoso!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Usuario o contraseña incorrectos.', 'warning')
                    return redirect(url_for('login'))
        finally:
            conexion.close()

    return render_template('login.html')

@app.route("/registro", methods=['GET', 'POST'])
def registro():
    """Maneja el registro de nuevos usuarios."""
    if request.method == 'POST':
        rol = request.form['rol']
        dia = request.form['dia']
        mes = request.form['mes']
        año = request.form['año']
        email = request.form['email']
        # El formulario usa 'nombre_usuario' pero la BD 'nombre_completo'
        nombre_completo = request.form['nombre_usuario']
        contraseña = request.form['contraseña']

        # Combinar la fecha
        fecha_nacimiento = f"{año}-{mes}-{dia}"

        # Hashear la contraseña por seguridad
        hashed_password = generate_password_hash(contraseña)

        conexion = obtener_conexion()
        if not conexion:
            flash('Error de conexión con el servidor. Inténtalo más tarde.', 'danger')
            return render_template('registro.html')

        try:
            with conexion.cursor() as cursor:
                # Comprobar si el email o el nombre de usuario ya existen
                sql_check = "SELECT * FROM usuarios WHERE email = %s OR nombre_completo = %s"
                cursor.execute(sql_check, (email, nombre_completo))
                if cursor.fetchone():
                    flash('El email o nombre de usuario ya está en uso.', 'warning')
                    return redirect(url_for('registro'))

                # Insertar nuevo usuario
                sql_insert = """
                    INSERT INTO usuarios (rol, fecha_nacimiento, email, nombre_completo, password)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert, (rol, fecha_nacimiento, email, nombre_completo, hashed_password))
            conexion.commit()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except pymysql.MySQLError as e:
            flash(f'Error al registrar el usuario: {e}', 'danger')
            return redirect(url_for('registro'))
        finally:
            conexion.close()

    return render_template('registro.html')

@app.route("/home")
def home():
    """Página de bienvenida después de un inicio de sesión exitoso."""
    # Aquí iría la lógica principal de tu aplicación.
    return render_template('home.html')

if __name__ == '__main__':
    # El modo debug es útil para desarrollo, ¡desactívalo en producción!
    app.run(debug=True)
