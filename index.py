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
                                     port=3306,
                                     user='root',
                                     password='', # Tu contraseña de MySQL
                                     database='proyecto_final', # El nombre de tu base de datos
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos: {e}")
        # Redirigir a la página de error del sistema si la conexión falla
        return None

@app.route("/")
def index():
    """Página principal, redirige al inicio de sesión."""
    return redirect(url_for('login'))

@app.route("/errorsistema")
def errorsistema():
    """Muestra una página de error genérico del sistema."""
    return render_template('errorsistema.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Maneja el inicio de sesión de los usuarios."""
    if request.method == 'POST':
        username_email = request.form['username_email']
        password = request.form['password']

        conexion = obtener_conexion()
        if not conexion:
            return redirect(url_for('errorsistema'))

        try:
            with conexion.cursor() as cursor:
                # Buscamos al usuario por email o por nombre de usuario (nombre_completo)
                sql = "SELECT * FROM usuarios WHERE email = %s OR nombre_completo = %s"
                cursor.execute(sql, (username_email, username_email))
                usuario = cursor.fetchone()

                # Verificar si la columna 'password' existe antes de intentar acceder a ella
                # Esto es útil para el escenario de "columna no existe"
                if 'password' not in usuario:
                    print("Error: La columna 'password' no existe en la tabla.")
                    return redirect(url_for('errorsistema'))

                if usuario and check_password_hash(usuario['password'], password):
                    # En una aplicación real, aquí crearías una sesión de usuario.
                    flash('¡Inicio de sesión exitoso!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Usuario o contraseña incorrectos.', 'warning')
                    return redirect(url_for('login'))

        except pymysql.err.OperationalError as e:
            # Captura errores específicos como "Tabla no existe"
            if "Table 'proyecto_final.usuarios' doesn't exist" in str(e):
                return redirect(url_for('errorsistema'))
            else:
                flash(f"Error de base de datos: {e}", 'danger')
                return redirect(url_for('login'))
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            return redirect(url_for('errorsistema'))
        finally:
            conexion.close()

    return render_template('login.html')

@app.route("/registro", methods=['GET', 'POST'])
def registro():
    """Maneja el registro de nuevos usuarios."""
    if request.method == 'POST':
        rol = request.form['rol']
        fecha_nacimiento = request.form['fecha_nacimiento']
        email = request.form['email']
        nombre_completo = request.form['nombre_usuario']
        contraseña = request.form['contraseña']

        # Hashear la contraseña por seguridad
        hashed_password = generate_password_hash(contraseña)

        conexion = obtener_conexion()
        if not conexion:
            return redirect(url_for('errorsistema'))

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
        except pymysql.err.OperationalError as e:
            if "Table 'proyecto_final.usuarios' doesn't exist" in str(e) or "Unknown column 'password'" in str(e):
                return redirect(url_for('errorsistema'))
            else:
                flash(f"Error de base de datos: {e}", 'danger')
                return redirect(url_for('registro'))
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            return redirect(url_for('errorsistema'))
        finally:
            conexion.close()

    return render_template('registro.html')

@app.route("/home")
def home():
    """Página de bienvenida después de un inicio de sesión exitoso."""
    return render_template('home.html')

if __name__ == '__main__':
    # El modo debug es útil para desarrollo, ¡desactívalo en producción!
    app.run(debug=True)
