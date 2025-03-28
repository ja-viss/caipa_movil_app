from pymongo import MongoClient
import pymongo.errors


def connect_mongodb():
    try:
        # Cadena de conexión a MongoDB Atlas
        connection_string = "mongodb+srv://caipatachira1988:RbchsWo3nkZiUGq0@caipa.vctrk.mongodb.net/caipa?retryWrites=true&w=majority"
        client = MongoClient(connection_string)
        db = client.caipa 
        print("Conexión a MongoDB Atlas exitosa.")
        return db
    except Exception as e:
        print(f"Error de conexión a MongoDB Atlas: {e}")
        return None

def get_user_data(db, username, password):
    try:
        collection = db.user_loggin
        user_data = collection.find_one({"email": username, "password": password})
        return user_data
    except Exception as e:
        print(f"Error en la consulta de usuario: {e}")
        return None

def get_user_type(db, username):
    try:
        collection = db.user_loggin
        user_type_data = collection.find_one({"email": username})
        return user_type_data
    except Exception as e:
        print(f"Error en la consulta de tipo de usuario: {e}")
        return None

def get_student_data(db, student_id):
    print(db, student_id)
    print('llego a get_student_data')
    try:
        collection = db.student_caipa
        print('Funcion get_student_data')
        student_data = collection.find_one({"ced_stu": student_id})
        ced_student = student_data.get('_id') 
        print(ced_student)

        if student_data:
            collection_repre = db.repre_caipa
            representative_data = collection_repre.find_one({"id_estu": ced_student})
            print('------------------------------------------')
            print(student_data, representative_data)
            print('------------------------------------------')
            return student_data, representative_data  # Devuelve ambos, incluso si representative_data es None
        else:
            print(f"No se encontraron datos del estudiante para el ID: {student_id}")
            return {}, None  # Devuelve un diccionario vacío para student_data y None para representative_data

    except Exception as e:
        print(f"Error en la consulta del estudiante: {e}")
        return {}, None  # Devuelve un diccionario vacío y None en caso de excepción


def get_role_info(db, user_type, user_identify):
    try:
        if user_type == 'Representante':
            collection = db.repre_caipa
            info_rol = collection.find_one({"ced_repre": user_identify})
            if info_rol:
                id_stu = info_rol.get("id_stu")
                collection_stu = db.student_caipa
                info_stu = collection_stu.find_one({"id": id_stu})
                return info_rol, info_stu

        elif user_type == 'Docente':
            collection = db.teacher_caipa
            print('------------------------------------------')
            print(user_identify)
            info_rol = collection.find_one({"ced_tea": user_identify})
            print(info_rol)
            print('------------------------------------------')
            return info_rol

        elif user_type == 'Administrativo':
            collection = db.admin_caipa
            print('------------------------------------------') 
            info_rol = collection.find_one({"ced_admin": user_identify})
            print(info_rol)
            print('------------------------------------------')
            return info_rol

    except Exception as e:
        print(f"Error en la consulta de información de rol: {e}")
        return None

def update_representative_student_data(db, user_identify, user_type, name, lastname, age, phone, email, student_id, name_stu, lastname_stu, age_stu):
    try:
        collection_repre = db.repre_caipa
        collection_stu = db.student_caipa

        # Actualizar datos del representante
        collection_repre.update_one(
            {"ced_repre": user_identify},
            {"$set": {
                "name_repre": name,
                "lastna_repre": lastname,
                "age_repre": age,
                "phone_repre": phone,
                "email_repre": email
            }}
        )

        # Actualizar datos del estudiante
        collection_stu.update_one(
            {"id": student_id},
            {"$set": {
                "name_stu": name_stu,
                "lastna_stu": lastname_stu,
                "age_stu": age_stu
            }}
        )

        return True, "Datos actualizados correctamente"
    except Exception as e:
        return False, f"Error al actualizar los datos: {e}"

def update_other_data(db, user_identify, user_type, name, lastname, age, phone, email):
    try:
        if user_type == 'Docente':
            collection = db.teacher_caipa
            collection.update_one(
                {"ced_tea": user_identify},
                {"$set": {
                    "name_tea": name,
                    "lastna_tea": lastname,
                    "age_tea": age,
                    "phone_tea": phone,
                    "email_tea": email
                }}
            )

        elif user_type == 'Administrativo':
            collection = db.admin_caipa
            collection.update_one(
                {"ced_admin": user_identify},
                {"$set": {
                    "name_admin": name,
                    "lastna_admin": lastname,
                    "age_admin": age,
                    "phone_admin": phone,
                    "email_admin": email
                }}
            )

        return True, "Datos actualizados correctamente"
    except Exception as e:
        return False, f"Error al actualizar los datos: {e}"

def get_all_teacher(db):
    try:
        collection = db.teacher_caipa
        teacher = list(collection.find())
        print(teacher)
        return teacher
    except Exception as e:
        print(f"Error al obtener docentes: {e}")
        return None
    

def get_all_students(db):
    try:
        collection = db.student_caipa
        students = list(collection.find())
        print(students)
        return students
    except Exception as e:
        print(f"Error al obtener estudiantes: {e}")
        return None

def get_all_areas_simple(db):
    try:
        collection = db.areas
        areas = list(collection.find())
        print(areas)
        return areas
    except Exception as e:
        print(f"Error al obtener areas: {e}")
        return None
    

def get_all_areas(db):
    try:
        collection_area = db.areas
        collection_detect = db.teacher_area_stu
        collection_teacher = db.teacher_caipa

        areas = list(collection_area.find())
        area_teacher_map = {}

        # Crear un diccionario que mapea area_id a teacher_id (como cadena)
        for relation in collection_detect.find():
            if 'area' in relation and 'teacher' in relation:
                area_id = str(relation['area'])
                teacher_id = str(relation['teacher']) # Asegúrate de convertir a string aquí
                area_teacher_map[area_id] = teacher_id

        # Obtener los nombres de los docentes en un diccionario para búsqueda eficiente
        teacher_name_map = {}
        for teacher in collection_teacher.find():
            teacher_id_str = str(teacher['_id']) # Convertir ObjectId a string para la clave
            teacher_name_map[teacher_id_str] = teacher.get('name_tea')

        # Agregar la información del docente (nombre) a cada área
        areas_with_teacher = []
        for area in areas:
            area_id_str = str(area['_id'])
            teacher_id_str = area_teacher_map.get(area_id_str) # Obtener teacher_id como string
            teacher_name = teacher_name_map.get(teacher_id_str) # Buscar usando la cadena

            area_info = {
                "_id": area['_id'],
                "name_area": area['name_area'],
                "teacher_assigned_id": teacher_id_str,
                "teacher_assigned_name": teacher_name
            }
            areas_with_teacher.append(area_info)

        print(areas_with_teacher)
        return areas_with_teacher
    except Exception as e:
        print(f"Error al obtener áreas con información de docentes: {e}")
        return None


def delete_student(db, student_id):
    try:
        collection_stu = db.student_caipa
        collection_repre = db.repre_caipa
        collection_users = db.user_loggin

        student_data = collection_stu.find_one({"ced_stu": student_id})
        if not student_data:
            return False, "No se encontró el estudiante"

        id_stu = student_data['_id']
        print(id_stu)

        # Buscar y eliminar el usuario antes de eliminar el estudiante y el representante
        result_repre_find = collection_repre.find_one({"id_estu": id_stu})
        if result_repre_find:
            ced_repre = result_repre_find['ced_repre']
            result_users = collection_users.delete_one({"ced": ced_repre})
            if result_users.deleted_count == 0:
                print(f"Advertencia: No se encontró el usuario con cedula {ced_repre}")
        else:
            print(f"Advertencia: No se encontró el representante para el estudiante con id {id_stu}")

        # Eliminar el estudiante y el representante
        result_repre = collection_repre.delete_one({"id_estu": id_stu})
        result = collection_stu.delete_one({"ced_stu": student_id})

        if result.deleted_count > 0 and result_repre.deleted_count > 0:
            return True, "Estudiante y Representante eliminado correctamente"
        elif result.deleted_count > 0:
            return True, "Estudiante eliminado correctamente, Representante no encontrado"
        elif result_repre.deleted_count > 0:
            return True, "Representante eliminado correctamente, Estudiante no encontrado"
        else:
            return False, "No se encontró el estudiante o el representante"

    except pymongo.errors.PyMongoError as e:
        return False, f"Error de MongoDB: {e}"
    except KeyError as e:
        return False, f"Error de clave faltante: {e}"
    except Exception as e:
        return False, f"Error inesperado: {e}"

def update_student(db, student_id, name_stu, lastna_stu, age_stu, grp_sng_stu, id_repre, name_repre, lastna_repre, age_repre):
    try:
        collection = db.student_caipa
        collection_repre = db.repre_caipa

        # Buscar estudiante
        student_data = collection.find_one({"ced_stu": student_id})
        if not student_data:
            return False, "No se encontró el estudiante"

        # Actualizar estudiante
        result = collection.update_one(
            {"ced_stu": student_id},
            {"$set": {
                "name_stu": name_stu,
                "lastna_stu": lastna_stu,
                "age_stu": age_stu,
                "grp_sng_stu": grp_sng_stu
            }}
        )

        print(id_repre)

        # Actualizar representante
        result_repre = collection_repre.update_one(
            {"ced_repre": id_repre},
            {"$set": {
                "name_repre": name_repre,
                "lastna_repre": lastna_repre,
                "age_repre": age_repre,
            }}
        )

        # Verificar resultados
        if result.modified_count > 0 and result_repre.modified_count > 0:
            return True, "Estudiante y representante actualizados correctamente"
        elif result.modified_count > 0:
            return True, "Estudiante actualizado correctamente, pero no se encontró el representante"
        else:
            return False, "No se encontró el estudiante"
    except Exception as e:
        return False, f"Error al actualizar el estudiante: {str(e)}"

def create_student(db, ced_stu, name_stu, lastna_stu, age_stu, grp_sng_stu, direcc_stu, fech_nac, cami_stu, pan_stu, zapa_stu, birth_stu, natio_stu, country_stu, gender, pes_stu, ced_repre, name_repre, lastna_repre, age_repre, phone_repre, number_repre, email_repre, direcc_repre, password):
    try:
        status = 'Activo'
        rol = 'Representante'
        collection = db.student_caipa
        collection_repre = db.repre_caipa
        collection_users = db.user_loggin

        user_data = {
            "ced" : ced_repre,
            "email":email_repre,
            "password":password,
            "status": status,
            "rol": rol
        }

        result_users = collection_users.insert_one(user_data)
        
        # Insertar estudiante y obtener su _id
        student_data = {
            "ced_stu": ced_stu,
            "name_stu": name_stu,
            "lastna_stu": lastna_stu,
            "age_stu": age_stu,
            "grp_sng_stu": grp_sng_stu,
            "direcc_stu": direcc_stu,
            "fech_nac": fech_nac,
            "cami_stu": cami_stu,
            "zapa_stu":zapa_stu,
            "pan_stu": pan_stu,
            "birth_stu": birth_stu,
            "natio_stu": natio_stu,
            "country_stu": country_stu,
            "pes_stu": pes_stu,
            "gender": gender
        }

        result = collection.insert_one(student_data)
        student_mongo_id = result.inserted_id  # Obtener el _id del estudiante

        # Insertar representante con el id_estu del estudiante
        repre_data = {
            "ced_repre": ced_repre,
            "name_repre": name_repre,
            "lastna_repre": lastna_repre,
            "phone_repre": phone_repre,
            "age_repre": age_repre,
            "number_repre": number_repre,
            "direcc_repre": direcc_repre,
            "email_repre": email_repre,            
            "id_estu": student_mongo_id  # Referencia al _id del estudiante
        }
        result_repre = collection_repre.insert_one(repre_data)

        # Verificar resultados
        if result.inserted_id and result_repre.inserted_id and result_users.inserted_id:
            return True, "Estudiante y representante creados correctamente"
        elif result.inserted_id:
            return True, "Estudiante creado correctamente, pero hubo un problema al crear el representante"
        else:
            return False, "Error al crear el estudiante"

    except Exception as e:
        return False, f"Error al crear el estudiante: {str(e)}"

def create_area(db, name_area):
    try:

        collection = db.areas

        area_data = {
            "name_area" : name_area
        }

        result = collection.insert_one(area_data)
        
        # Verificar resultados
        if result.inserted_id:
            return True, "Area creada exitosamente."
        else:
            return False, "Error al crear area"

    except Exception as e:
        return False, f"Error al crear area: {str(e)}"

def assign_teacher_to_area_db(db, teacher_id, area_id):
    teacher_area = db.teacher_area_stu
    existing_assignment = teacher_area.find_one({"area": area_id, "teacher": teacher_id})
    if existing_assignment:
        return "El docente ya está asignado a esta área."
    else:
        new_assignment = {
            "area": area_id,
            "teacher": teacher_id
        }
        teacher_area.insert_one(new_assignment)
        return "Docente asignado correctamente."        