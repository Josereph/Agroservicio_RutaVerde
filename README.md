# 🌿 Agroservicio _Ruta Verde_

Aplicación web para la **gestión de viajes, transportes y entregas** del agroservicio “Ruta Verde”.  
El sistema permite asignar vehículos, conductores, registrar entregas, controlar evidencias (fotos y firmas), y optimizar la logística agrícola 🚜.

---

##  Descripción general

**Agroservicio Ruta Verde** busca digitalizar los procesos de transporte del agroservicio.  
Con esta app, el usuario puede:
- Controlar los viajes y transportes de carga.  
- Registrar clientes, vehículos y conductores.  
- Llevar seguimiento del estado de cada entrega.  
- Guardar fotos y documentos de evidencia.  
- Mejorar la eficiencia y seguridad en las entregas.

Todo esto se logra con una aplicación web desarrollada en **Python + Flask**, usando **Bootstrap 5** para la interfaz y **MySQL** como base de datos principal.

---

##  Características principales

✅ Control de viajes y transportes de carga  
✅ Registro de clientes, conductores y vehículos  
✅ Seguimiento de pedidos (cargando → en ruta → entregado)  
✅ Evidencias digitales con fotos y firmas  
✅ Alertas automáticas por licencias o seguros vencidos  
✅ Base de datos centralizada en MySQL  
✅ Compatible con PC y móviles  

---

##  Tecnologías utilizadas

| Tipo | Tecnología |
|------|-------------|
| **Backend** | Python 3.8+, Flask, Flask-SQLAlchemy, Flask-Migrate, python-dotenv |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5 |
| **Base de datos** | MySQL Workbench |
| **Control de versiones** | Git / GitHub |
| **Entorno de desarrollo** | Visual Studio Code |

---

##  Instalación y configuración (Windows / PowerShell)

### 1️⃣ Clonar el repositorio y crear tu rama de trabajo
```powershell
git clone <URL-del-repo>
cd Agroservicio_-Ruta_Verde-
git checkout -b develop
```

### 2️⃣ Crear el entorno virtual
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```
> Si PowerShell bloquea scripts:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 3️⃣ Instalar dependencias  
Crea un archivo llamado **`requirements.txt`** con este contenido:

```txt
Flask==3.0.0
Flask-SQLAlchemy==3.0.0
Flask-Migrate==4.0.0
python-dotenv==1.0.0
```

Luego instalá todo:
```powershell
pip install -r requirements.txt
```

### 4️⃣ Variables de entorno  
Crea un archivo **.env** en la raíz del proyecto:
```ini
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=mysql+pymysql://usuario:password@localhost:3306/rutaverde
SECRET_KEY=pon_un_valor_seguro_aqui
```

### 5️⃣ Base de datos y migraciones
```powershell
flask db init
flask db migrate -m "init schema"
flask db upgrade
```

### 6️⃣ Ejecutar la aplicación
```powershell
flask run
```

Abrí [http://127.0.0.1:5000/](http://127.0.0.1:5000/) para verla en acción 👀

---

## Estructura recomendada del proyecto (Para el proyecto final sera cambiada)

```
Agroservicio_-Ruta_Verde-/
├─ app.py
├─ config.py
├─ requirements.txt
├─ .env
├─ .gitignore
├─ /instance/
├─ /migrations/
├─ /rutaverde/
│  ├─ __init__.py
│  ├─ models.py
│  ├─ routes.py
│  ├─ services/
│  └─ utils/
├─ /templates/
└─ /static/
   ├─ css/
   ├─ js/
   └─ img/
```

---

##  Requisitos mínimos

| Recurso | Recomendado |
|----------|--------------|
| **Procesador** | Intel Core i3 (8ª gen) o equivalente AMD |
| **Memoria RAM** | Mínimo 4 GB (recomendado 8 GB) |
| **Sistema operativo** | Windows 10 o superior |
| **Navegadores compatibles** | Chrome, Edge, Firefox, Opera, Safari |

---

##  Comandos Git básicos

```powershell
# Ver estado del proyecto
git status

# Agregar y guardar cambios
git add .
git commit -m "feat: configuración inicial con Flask y Bootstrap"

# Subir rama develop al repositorio remoto
git push -u origin develop
```

Si creas otra rama (por ejemplo `base`):
```powershell
git checkout -b base
git push -u origin base
```

Para mantener tus ramas actualizadas:
```powershell
git checkout develop
git pull origin develop
```

---

##  Archivo .gitignore recomendado

Crea un archivo **.gitignore** en la raíz con esto:

```gitignore
# Entorno virtual
.venv/
env/
venv/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Variables / secretos
.env
*.env

# VSCode
.vscode/

# MySQL dumps
*.sql
*.dump

# Flask/Migrate cache
migrations/versions/__pycache__/
```

---

## 👥 Equipo de desarrollo

| Integrante | Carnet |
|-------------|---------|
| José Diego Centeno Cortez | 2023-CC-250 |
| René Arturo Hernández Pocasangre | 2023-HP-250 |
| Joseph Arnulfo Orellana Crespín | 2023-OC-250 |
| Emerson Manuel Hernández García | 2023-HG-250 |
| José Wilfredo Valle Escalante | 2023-VE-250 |

---

##  Licencia

Proyecto creado con fines **educativos** 🎓  
© 2025 – Universidad Católica de El Salvador  
Todos los derechos reservados.

---

##  Notas finales

- Si ves errores como `git: 'ckeckout' is not a git command`, revisá la ortografía 😅.  
  El comando correcto es `git checkout`.  
- No subas tu carpeta `.venv` ni tu archivo `.env` (contienen credenciales y dependencias locales).  
- Recordá ejecutar `pip freeze > requirements.txt` si agregás nuevas librerías.  
- ¡Y listo! Con esto tenés tu entorno configurado y tu README completo para GitHub 🚀
