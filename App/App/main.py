from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDRoundFlatButton
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView  
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem 
from kivy.utils import get_color_from_hex
from kivy.properties import ObjectProperty  
from model import connect_mongodb, get_user_data, get_user_type, get_role_info, update_representative_student_data, update_other_data, get_all_students, update_student, delete_student, get_student_data, create_student, create_area, get_all_areas, get_all_teacher, assign_teacher_to_area_db

Window.size = (350, 600)

class TeacherScreen(Screen):
    pass

class TeacherCard(MDCard):
    name = StringProperty()
    lastname = StringProperty()
    ced = StringProperty()
    teacher_id = StringProperty()

class StudentsScreen(Screen):
    pass

class StudentCard(MDCard):
    name = StringProperty()
    lastname = StringProperty()
    ced = StringProperty()
    age = StringProperty()
    student_id = StringProperty()

class AreasScreen(Screen):
    pass

class AreasCard(MDCard):
    name = StringProperty()
    area_id = StringProperty()
    name_tea = StringProperty()



class LoginScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class RegistrarEstudianteScreen(Screen):
    pass

class RegistrarAreaScreen(Screen):
    pass

class RegistrarDocenteScreen(Screen):
    pass

class UpdateStudentScreen(Screen):
    selected_student_id = StringProperty()  

    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        if app.selected_student_id:
            self.student_id = app.selected_student_id 
            self.load_student_data()

    def load_student_data(self):
        print(self.student_id)
        db = connect_mongodb()
        print(db)
        student_data, representative_data = get_student_data(db, self.student_id)

        if student_data:  # Verifica si student_data no está vacío
            self.ids.name_stu.text = student_data['name_stu']
            self.ids.lastname_stu.text = student_data['lastna_stu']
            self.ids.document_id_stu.text = str(student_data['ced_stu'])
            self.ids.age_stu.text = str(student_data['age_stu'])
            self.ids.grp_sng_stu.text = student_data['grp_sng_stu']

            if representative_data: #Verifica si los datos del representante no son None
                self.ids.name_repre.text = representative_data['name_repre']
                self.ids.lastname_repre.text = representative_data['lastna_repre']
                self.ids.document_id_repre.text = str(representative_data['ced_repre'])
                self.ids.age_repre.text = str(representative_data['age_repre'])

            else:
                print(f"No se encontraron datos del representante para el ID: {self.student_id}")

        else:
            print(f"No se encontró información para el estudiante con ID: {self.student_id}")
            # Maneja el caso en que no se encuentran datos del estudiante, por ejemplo, muestra un mensaje
            self.ids.name_stu.text = ""  # Limpia los campos
            self.ids.lastname_stu.text = ""
            self.ids.document_id_stu.text = ""
            self.ids.age_stu.text = ""

            app = App.get_running_app()  # Get the app instance
            if app:  # Make sure the app exists
                app.show_error_dialog(f"No se encontró información para el estudiante con ID: {self.student_id}")
            else:
                print("Error: Application instance not found.")

class DeleteStudentScreen(Screen):
    pass



class CaipaApp(MDApp):
    dialog = None
    user_type = StringProperty()
    user_data = ObjectProperty()
    student_data = ObjectProperty()
    name = StringProperty("")
    lastname = StringProperty("")
    age = StringProperty("")
    phone = StringProperty("")
    email = StringProperty("")
    name_stu = StringProperty("")
    lastname_stu = StringProperty("")
    age_stu = StringProperty("")
    student = StringProperty()
    selected_student_id = StringProperty()  
    selected_teacher_id = StringProperty()  
    selected_area_id = StringProperty()      
    db = None 

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'LightBlue'

        # Load the KV file first
        self.root = Builder.load_file("main.kv") 
        return self.root
    
    def open_menu(self, button):
        if self.user_type == 'Representante':
            menu_items = [
                {"text": "Opción 1", "viewclass": "OneLineListItem", "on_release": lambda x="Opción 1": self.menu_option(x)},
                {"text": "Opción 2", "viewclass": "OneLineListItem", "on_release": lambda x="Opción 2": self.menu_option(x)},
                {"text": "Opción 3", "viewclass": "OneLineListItem", "on_release": lambda x="Opción 3": self.menu_option(x)},
            ]

        if self.user_type == 'Docente':
            menu_items = [
                {"text": "Opción 1", "viewclass": "OneLineListItem", "on_release": lambda x="Opción 1": self.menu_option(x)},
                {"text": "Opción 2", "viewclass": "OneLineListItem", "on_release": lambda x="Opción 2": self.menu_option(x)},
                {"text": "Opción 3", "viewclass": "OneLineListItem", "on_release": lambda x="Opción 3": self.menu_option(x)},
            ]

        if self.user_type == 'Administrativo':
            menu_items = [
                {"text": "Estudiante", "viewclass": "OneLineListItem", "on_release": lambda x="Registrar Estudiante": self.menu_option(x)},
                {"text": "Area", "viewclass": "OneLineListItem", "on_release": lambda x="Registrar Area": self.menu_option(x)},
                {"text": "Docente", "viewclass": "OneLineListItem", "on_release": lambda x="Registrar Docente": self.menu_option(x)},
            ]

        self.menu = MDDropdownMenu(
            items=menu_items,
            width=200,
        )
        self.menu.caller = button
        self.menu.open()

    def menu_option(self, text):
        if text == "Registrar Estudiante":
            self.root.current = 'students_screen'  # ¡Corregido!
        elif text == "Registrar Area":
            self.root.current = 'areas_screen'        # ¡Corregido!
        elif text == "Registrar Docente":
            self.root.current = 'registrar_docente'     # ¡Corregido!
        else:
            print(f"Opción seleccionada: {text}")
        self.menu.dismiss()

    def load_students_admin(self):
        if self.user_type == 'Administrativo':
            students_screen = self.root.get_screen('students_screen')
            student_list_box = students_screen.ids.student_list_box
            student_list_box.clear_widgets()

            db = connect_mongodb()
            if db:
                try:
                    students = get_all_students(db)
                    print(f"Estudiantes obtenidos: {students}")  # Depuración
                    if students:
                        for student in students:
                            student_card = StudentCard(
                                name=student['name_stu'],
                                lastname=student['lastna_stu'],
                                ced=student['ced_stu'],
                                age=student['age_stu'],
                                student_id=str(student['ced_stu'])
                            )
                            student_list_box.add_widget(student_card)
                        self.root.current = 'students_screen'
                    else:
                        self.show_error_dialog("No se encontraron estudiantes.")
                except Exception as e:
                    self.show_error_dialog(f"Error al cargar estudiantes: {str(e)}")
            else:
                self.show_error_dialog("Error al conectar a la base de datos.")        

    def load_areas_admin(self):
        print("entro a la funcion areas")
        if self.user_type == 'Administrativo':
            areas_screen = self.root.get_screen('areas_screen')
            areas_list_box = areas_screen.ids.areas_list_box
            areas_list_box.clear_widgets()
            db = connect_mongodb()
            if db:
                try:
                    areas = get_all_areas(db)
                    print(f"areas obtenidos: {areas}")  # Depuración
                    if areas:
                        for area in areas:
                            teacher_name = area.get('teacher_assigned_name')
                            if teacher_name:
                                name_tea = teacher_name
                                print(name_tea)
                            else:
                                name_tea = 'Aun no posee Docente Asignado'
                            areas_card = AreasCard(
                                name=area['name_area'],
                                name_tea=name_tea,
                                area_id=str(area['_id'])
                            )
                            areas_list_box.add_widget(areas_card)
                        self.root.current = 'areas_screen'
                    else:
                        self.show_error_dialog("No se encontraron areas.")
                except Exception as e:
                    self.show_error_dialog(f"Error al cargar areas: {str(e)}")
            else:
                self.show_error_dialog("Error al conectar a la base de datos.")        

    def load_teacher_admin(self, area_id=None):
        if self.user_type == 'Administrativo':
            teacher_screen = self.root.get_screen('teacher_screen')
            teacher_list_box = teacher_screen.ids.teacher_list_box
            teacher_list_box.clear_widgets()

            self.selected_area_id = area_id  # Almacena el area_id en la instancia de la aplicación

            db = connect_mongodb()
            if db:
                try:
                    teachers = get_all_teacher(db)
                    print(f"Docentes obtenidos: {teachers}")  # Depuración
                    if teachers:
                        for teacher in teachers:
                            teacher_card = TeacherCard(
                                name=teacher['name_tea'],
                                lastname=teacher['lastna_tea'],
                                ced=teacher['ced_tea'],
                                teacher_id=str(teacher['_id'])
                            )
                            teacher_list_box.add_widget(teacher_card)
                        self.root.current = 'teacher_screen'
                    else:
                        self.show_error_dialog("No se encontraron Docentes.")
                except Exception as e:
                    self.show_error_dialog(f"Error al cargar Docentes: {str(e)}")
            else:
                self.show_error_dialog("Error al conectar a la base de datos.")        
  
  
    def login(self):
        login_screen = self.root.get_screen('login')
        username = login_screen.ids.user.text
        password = login_screen.ids.password.text

        db = connect_mongodb()  # Obtiene la conexión a MongoDB
        if db is not None:
            user_data = get_user_data(db, username, password) # Obtiene los datos del usuario

            if user_data:
                print('inicia bien')
                self.start_session(username, db)
            else:
                self.show_error_dialog('Credenciales inválidas')
                login_screen.ids.user.text = ''
                login_screen.ids.password.text = ''
        else: # Si connect_mongodb falla
            self.show_error_dialog('Error al conectar a la base de datos')

    def assign_teacher_to_area(self, teacher_id):
        if self.selected_area_id:
            # Aquí debes implementar la lógica para asignar el teacher_id al area_id en tu base de datos.
            # Por ejemplo, puedes llamar a una función en tu modelo que realice la actualización.
            print(f"Asignando docente {teacher_id} al área {self.selected_area_id}")
            # Lógica para actualizar la base de datos (usando tu modelo)
            db = connect_mongodb()
            if db:
                try:
                    #Asumiendo que tienes una funcion en model.py o donde este tu logica de base de datos
                    #llamada assign_teacher_to_area_db(db, teacher_id, area_id)
                    message = assign_teacher_to_area_db(db, teacher_id, self.selected_area_id)
                    self.show_error_dialog(message)
                    self.root.current = 'areas_screen'
                except Exception as e:
                    self.show_error_dialog(f"Error al asignar docente: {str(e)}")
            else:
                self.show_error_dialog("Error al conectar a la base de datos.")

        else:
            self.show_error_dialog("No se ha seleccionado un área.")    

    def start_session(self, username, db):
        self.dialog = MDDialog(
            title='Información',
            text=f'Bienvenido {username}',
            buttons=[MDFlatButton(text='OK', on_release=self.close)],
        )
        self.dialog.open()

        user_type_data = get_user_type(db, username)
        print(user_type_data)
        if user_type_data:
            self.user_type = user_type_data.get("rol")
            self.user_identify = user_type_data.get("ced")
            self.load_user_data(db, self.user_type, self.user_identify)
            self.root.current = 'main'
        else:
            self.user_type = '' # Limpia el tipo de usuario si falla la info de user type.

    def load_user_data(self, db, user_type, user_identify):
        if user_type == 'Representante':
            info_rol, info_stu = get_role_info(db, user_type, user_identify)
            self.user_data = info_rol
            self.student_data = info_stu

            if info_rol and info_stu:
                self.change_content('inicio', info_rol, info_stu)

        elif user_type == 'Docente':
            info_rol = get_role_info(db, user_type, user_identify)
            self.user_data = info_rol

            if info_rol:
                self.change_content('inicio', info_rol)

        elif user_type == 'Administrativo':
            info_rol = get_role_info(db, user_type, user_identify)
            self.user_data = info_rol

            if info_rol:
                self.change_content('inicio', info_rol)

        else:
            self.user_type = ''

    def update_user(self):
        # Usar las variables de instancia para obtener los valores
        name = self.name
        lastname = self.lastname
        age = self.age
        phone = self.phone
        email = self.email
        name_stu = self.name_stu
        lastname_stu = self.lastname_stu
        age_stu = self.age_stu

        if self.user_type == 'Representante':
            if not all([name, lastname, age, phone, email, name_stu, lastname_stu, age_stu]):
                self.show_error_dialog("Todos los campos son obligatorios")
                return

        elif self.user_type == 'Docente':
            if not all([name, lastname, age, phone, email]):
                self.show_error_dialog("Todos los campos son obligatorios")
                return

        elif self.user_type == 'Administrativo':
            if not all([name, lastname, age, phone, email]):
                self.show_error_dialog("Todos los campos son obligatorios")
                return

        # Llamar a la función en model.py para actualizar los datos
        db = connect_mongodb()
        if db:
            if self.user_type == 'Representante':
                success, message = update_representative_student_data(
                    db, self.user_identify, self.user_type,
                    name, lastname, age, phone, email,
                    self.student_data.get("id"),
                    name_stu, lastname_stu, age_stu
                )

            else:
                success, message = update_other_data(
                    db, self.user_identify, self.user_type,
                    name, lastname, age, phone, email
                )

            if success:
                self.show_error_dialog("Datos actualizados correctamente")
                # Opcionalmente, refrescar los datos mostrados después de la actualización
                self.load_user_data(db, self.user_type, self.user_identify)
                self.change_content('actualizar') # o 'actualizar' si quieres permanecer en la pantalla de actualización
            else:
                self.show_error_dialog(message)
        else:
            self.show_error_dialog("Error al conectar a la base de datos")

    def update_student(self):
        print('se entro a la funcion debe leer el id')
        print(self.selected_student_id)
        # Obtener los valores de los campos de texto
        name_stu = self.root.get_screen('update_student_screen').ids.name_stu.text
        lastna_stu = self.root.get_screen('update_student_screen').ids.lastname_stu.text
        age_stu = self.root.get_screen('update_student_screen').ids.age_stu.text
        grp_sng_stu = self.root.get_screen('update_student_screen').ids.grp_sng_stu.text
        # Obtener el ID del estudiante seleccionado (puedes pasarlo como propiedad)
        student_id = self.selected_student_id  # Asegúrate de establecer esta propiedad al seleccionar un estudiante
        id_repre = self.root.get_screen('update_student_screen').ids.document_id_repre.text
        name_repre = self.root.get_screen('update_student_screen').ids.name_repre.text
        lastna_repre = self.root.get_screen('update_student_screen').ids.lastname_repre.text
        age_repre = self.root.get_screen('update_student_screen').ids.age_repre.text
        # Llamar a la función de actualización en model.py
        db = connect_mongodb()
        if db:
            success, message = update_student(db, student_id, name_stu, lastna_stu, age_stu, grp_sng_stu, id_repre, name_repre, lastna_repre, age_repre)
            if success:
                self.show_error_dialog(message)
                # Volver a la pantalla principal o actualizar la lista de estudiantes
                self.root.current = 'main'
            else:
                self.show_error_dialog(message)
        else:
            self.show_error_dialog("Error al conectar a la base de datos")

    def create_student(self):
        ced_stu = self.root.get_screen('registrar_estudiante').ids.document_id_stu.text        
        name_stu = self.root.get_screen('registrar_estudiante').ids.name_stu.text
        lastna_stu = self.root.get_screen('registrar_estudiante').ids.lastname_stu.text
        age_stu = self.root.get_screen('registrar_estudiante').ids.age_stu.text
        grp_sng_stu = self.root.get_screen('registrar_estudiante').ids.grp_sng_stu.text
        direcc_stu = self.root.get_screen('registrar_estudiante').ids.direcc_stu.text
        fech_nac = self.root.get_screen('registrar_estudiante').ids.fech_nac.text
        cami_stu = self.root.get_screen('registrar_estudiante').ids.cami_stu.text
        pan_stu = self.root.get_screen('registrar_estudiante').ids.pan_stu.text
        zapa_stu = self.root.get_screen('registrar_estudiante').ids.zapa_stu.text
        birth_stu = self.root.get_screen('registrar_estudiante').ids.birth_stu.text
        state_stu = self.root.get_screen('registrar_estudiante').ids.state_stu.text
        natio_stu = self.root.get_screen('registrar_estudiante').ids.natio_stu.text
        country_stu = self.root.get_screen('registrar_estudiante').ids.country_stu.text
        gender = self.root.get_screen('registrar_estudiante').ids.gender.text
        pes_stu = self.root.get_screen('registrar_estudiante').ids.pes_stu.text
        
        ced_repre = self.root.get_screen('registrar_estudiante').ids.document_id_repre.text                
        name_repre = self.root.get_screen('registrar_estudiante').ids.name_repre.text
        lastna_repre = self.root.get_screen('registrar_estudiante').ids.lastname_repre.text
        age_repre = self.root.get_screen('registrar_estudiante').ids.age_repre.text
        number_repre = self.root.get_screen('registrar_estudiante').ids.number_repre.text
        phone_repre = self.root.get_screen('registrar_estudiante').ids.phone_repre.text
        email_repre = self.root.get_screen('registrar_estudiante').ids.email_repre.text
        direcc_repre = self.root.get_screen('registrar_estudiante').ids.direcc_repre.text
        password = self.root.get_screen('registrar_estudiante').ids.password.text
        # Llamar a la función de creación en model.py
        db = connect_mongodb()
        if db:
            success, message = create_student(db, ced_stu, name_stu, lastna_stu, age_stu, grp_sng_stu, direcc_stu, fech_nac, cami_stu, pan_stu, zapa_stu, birth_stu, natio_stu, country_stu, gender, pes_stu, ced_repre, name_repre, lastna_repre, age_repre, phone_repre, number_repre, email_repre, direcc_repre, password)
            if success:
                self.show_error_dialog(message)

                self.root.get_screen('registrar_estudiante').ids.document_id_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.name_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.lastname_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.age_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.grp_sng_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.direcc_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.fech_nac.text = ''
                self.root.get_screen('registrar_estudiante').ids.cami_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.pan_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.zapa_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.birth_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.state_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.natio_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.country_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.gender.text = ''
                self.root.get_screen('registrar_estudiante').ids.pes_stu.text = ''
                self.root.get_screen('registrar_estudiante').ids.document_id_repre.text = ''
                self.root.get_screen('registrar_estudiante').ids.name_repre.text = ''
                self.root.get_screen('registrar_estudiante').ids.lastname_repre.text = ''
                self.root.get_screen('registrar_estudiante').ids.age_repre.text = ''
                self.root.get_screen('registrar_estudiante').ids.number_repre.text = ''
                self.root.get_screen('registrar_estudiante').ids.phone_repre.text = ''
                self.root.get_screen('registrar_estudiante').ids.email_repre.text = ''
                self.root.get_screen('registrar_estudiante').ids.direcc_repre.text = ''
                self.root.get_screen('registrar_estudiante').ids.password.text = ''

                # Volver a la pantalla principal
                self.root.current = 'main'

            else:
                self.show_error_dialog(message)
        else:
            self.show_error_dialog("Error al conectar a la base de datos")

    def create_area_caipa(self):

        name_area = self.root.get_screen('registrar_area').ids.name_area.text

        db = connect_mongodb()
        if db:
            success, message = create_area(db, name_area)
            if success:
                self.show_error_dialog(message)

                self.root.get_screen('registrar_area').ids.name_area.text = ''

                self.root.current = 'main'

            else:
                self.show_error_dialog(message)
        else:
            self.show_error_dialog("Error al conectar a la base de datos")
       
  
    def show_delete_confirmation(self, student_id):
        self.selected_student_id = student_id  # Guarda el ID del estudiante a eliminar

        confirm_dialog = MDDialog(
            text="¿Estás seguro de que deseas eliminar este estudiante?",
            buttons=[
                MDFlatButton(
                    text="Cancelar",
                    on_release=lambda *args: confirm_dialog.dismiss()
                ),
                MDFlatButton(
                    text="Eliminar",
                    on_release=lambda *args: self.delete_student(confirm_dialog)
                ),
            ],
        )
        confirm_dialog.open()


    def delete_student(self, confirm_dialog):
        # Obtener el ID del estudiante seleccionado (puedes pasarlo como propiedad)
        student_id = self.selected_student_id  # Asegúrate de establecer esta propiedad al seleccionar un estudiante
        print(self.selected_student_id)
        # Llamar a la función de eliminación en model.py
        db = connect_mongodb()
        if db:
            confirm_dialog.dismiss()
            success, message = delete_student(db, student_id)
            if success:
                self.show_error_dialog(message)
                # Volver a la pantalla principal o actualizar la lista de estudiantes
                self.dialog.dismiss()
                self.load_students_admin() # Llama a la funcion load_students_admin de la clase CaipaApp
            else:
                self.show_error_dialog(message)
        else:
            self.show_error_dialog("Error al conectar a la base de datos")


    def change_content(self, screen_name, info_rol=None, info_stu=None):
        info_rol = self.user_data 
        info_stu = self.student_data 
        main_screen = self.root.get_screen('main')
        content_container = main_screen.ids.content_container
        content_container.clear_widgets()
        content = MDBoxLayout(orientation='vertical', padding=20, spacing=10)

        if screen_name == 'inicio':
            content = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 10

    MDBoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: "50dp"
        md_bg_color: app.theme_cls.primary_color 
        radius:20
        MDLabel:
            text: "Informacion Personal"
            font_style: 'Overline'  
            color: 1, 1, 1, 1  
            font_size: '20sp'
            halign: 'center'
            valign: 'center'

    MDGridLayout:
        cols: 2  
        spacing: 15
        
        MDTextField:
            id: name
            icon_left: "account-circle"
            hint_text: "Nombre"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True
        
        MDTextField:
            id: lastname
            icon_left: "account-circle"
            hint_text: "Apellidos"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True

        MDTextField:
            id: document_id
            icon_left: "card-account-details"
            hint_text: "Cedula de Identidad"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True
            
            
        MDTextField:
            id: age
            icon_left: "page-layout-body"
            hint_text: "Edad"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True

        MDTextField:
            id: phone
            icon_left: "phone"
            hint_text: "Numero de Telefono"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True
            
        MDTextField:
            id: email
            icon_left: "email-box"
            hint_text: "Correo Electronico"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True

        MDRaisedButton:
            text: "Cerrar sesion"
            size_hint_x: None
            width: 150
            pos_hint: {"center_x": 0.5}
            on_press: app.logout()

''')
            
            if self.user_type == 'Representante':
                if info_rol:
                    content.ids.name.text = info_rol['name_repre']
                    content.ids.lastname.text = info_rol['lastna_repre']
                    content.ids.document_id.text = info_rol['ced_repre']
                    content.ids.age.text = str(info_rol['age_repre'])
                    content.ids.phone.text = info_rol['phone_repre']
                    content.ids.email.text = info_rol['email_repre']

            if self.user_type == 'Docente':
                if info_rol:
                    content.ids.name.text = info_rol['name_tea']
                    content.ids.lastname.text = info_rol['lastna_tea']
                    content.ids.document_id.text = info_rol['ced_tea']
                    content.ids.age.text = str(info_rol['age_tea'])
                    content.ids.phone.text = info_rol['phone_tea']
                    content.ids.email.text = info_rol['email_tea']

            if self.user_type == 'Administrativo':
                print('se dsitrtubuyo')
                if info_rol:
                    content.ids.name.text = info_rol['name_admin']
                    content.ids.lastname.text = info_rol['lastna_admin']
                    content.ids.document_id.text = info_rol['ced_admin']
                    content.ids.age.text = str(info_rol['age_admin'])
                    content.ids.phone.text = info_rol['phone_admin']
                    content.ids.email.text = info_rol['email_admin']

        elif screen_name == 'actualizar':
            if self.user_type == 'Representante':
                content = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 10

    MDGridLayout:
        cols: 2  
        spacing: 15

        MDLabel:
            text: "Representante"
            font_style: 'Overline'  
            color: app.theme_cls.primary_color 
            font_size: '16sp'
            halign: 'center'
            valign: 'center'
            
        MDTextField:
            id: name
            icon_left: "account-circle"
            hint_text: "Nombre"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            text: app.name
            on_text: app.name = self.text
                
            
        MDTextField:
            id: lastname
            icon_left: "account-circle"
            hint_text: "Apellidos"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            text: app.lastname
            on_text: app.lastname = self.text
                
                
        MDTextField:
            id: age
            icon_left: "page-layout-body"
            hint_text: "Edad"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            text: app.age
            on_text: app.age = self.text
                

        MDTextField:
            id: phone
            icon_left: "phone"
            hint_text: "Numero de Telefono"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            text: app.phone
            on_text: app.phone = self.text
                
                
        MDTextField:
            id:email
            icon_left: "email-box"
            hint_text: "Correo Electronico"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            text: app.email
            on_text: app.email = self.text
                

        MDLabel:
            text: "Estudiante"
            font_style: 'Overline'  
            color: app.theme_cls.primary_color 
            font_size: '16sp'
            halign: 'center'
            valign: 'center'
            
        MDTextField:
            id: name_stu
            icon_left: "account-circle"
            hint_text: "Nombre"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            text: app.name_stu
            on_text: app.name_stu = self.text
                
                
        MDTextField:
            id: lastname_stu
            icon_left: "account-circle"
            hint_text: "Apellidos"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            text: app.lastname_stu
            on_text: app.lastname_stu = self.text
                
                
        MDTextField:
            id: age_stu
            icon_left: "page-layout-body"
            hint_text: "Edad"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            text: app.age_stu
            on_text: app.age_stu = self.text

        MDRaisedButton:
            text: "Actualizar"
            size_hint_x: None
            width: 150
            pos_hint: {"center_x": 0.5}
            on_press: app.update_user()

''')
                if info_rol and info_stu:
                    self.name = info_rol['name_repre']
                    self.lastname = info_rol['lastna_repre']
                    self.age = str(info_rol['age_repre'])
                    self.phone = info_rol['phone_repre']
                    self.email = info_rol['email_repre']
                    self.document_id = info_rol['ced_repre']

                    self.name_stu = info_stu['name_stu']
                    self.lastname_stu = info_stu['lastna_stu']
                    self.age_stu = str(info_stu['age_stu'])
                    self.document_id_stu = info_stu['ced_stu']

            else:
                content = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 10

    MDGridLayout:
        cols: 2  
        spacing: 15

        MDLabel:
            text: "Informacion"
            font_style: 'Overline'  
            color: app.theme_cls.primary_color 
            font_size: '16sp'
            halign: 'center'
            valign: 'center'
            
        MDTextField:
            id: name
            icon_left: "account-circle"
            hint_text: "Nombre"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            text: app.name
            on_text: app.name = self.text
                
            
        MDTextField:
            id: lastname
            icon_left: "account-circle"
            hint_text: "Apellidos"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            text: app.lastname
            on_text: app.lastname = self.text
                
            
        MDTextField:
            id: age
            icon_left: "page-layout-body"
            hint_text: "Edad"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            text: app.age
            on_text: app.age = self.text
                

        MDTextField:
            id: phone
            icon_left: "phone"
            hint_text: "Numero de Telefono"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            text: app.phone
            on_text: app.phone = self.text
                
                
        MDTextField:
            id: email
            icon_left: "email-box"
            hint_text: "Correo Electronico"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            text: app.email
            on_text: app.email = self.text

        MDRaisedButton:
            text: "Actualizar"
            size_hint_x: None
            width: 150
            pos_hint: {"center_x": 0.5}
            on_press: app.update_user()

''')
                if self.user_type == 'Docente':
                    if info_rol:
                        self.name = info_rol['name_tea']
                        self.lastname = info_rol['lastna_tea']
                        self.age = str(info_rol['age_tea'])
                        self.phone = info_rol['phone_tea']
                        self.email = info_rol['email_tea']
                        self.document_id = info_rol['ced_tea']

                elif self.user_type == 'Administrativo':
                    if info_rol:
                        self.name = info_rol['name_admin']
                        self.lastname = info_rol['lastna_admin']
                        self.age = str(info_rol['age_admin'])
                        self.phone = info_rol['phone_admin']
                        self.email = info_rol['email_admin']
                        self.document_id = info_rol['ced_admin']

        elif screen_name == 'estudiante':
            if self.user_type == 'Representante':
                content = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 10

    MDBoxLayout:
        orientation: 'horizontal'
        size_hint_y: None 
        height: "50dp"
        md_bg_color: app.theme_cls.primary_color 
        radius: 20
        MDLabel:
            text: "Estudiante"
            font_style: 'Overline'  
            color: 1, 1, 1, 1  
            font_size: '20sp'
            halign: 'center'
            valign: 'center'

    MDGridLayout:
        cols: 2  
        spacing: 15
        
        MDTextField:
            id: name_stu
            icon_left: "account-circle"
            hint_text: "Nombre"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True
            
        MDTextField:
            id: lastname_stu
            icon_left: "account-circle"
            hint_text: "Apellidos"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True

        MDTextField:
            id: document_id_stu
            icon_left: "card-account-details"
            hint_text: "Cedula de Identidad"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True
            
            
        MDTextField:
            id: age_stu
            icon_left: "page-layout-body"
            hint_text: "Edad"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True

''')
                if info_rol and info_stu:
                    content.ids.name_stu.text = info_stu['name_stu']
                    content.ids.lastname_stu.text = info_stu['lastna_stu']
                    content.ids.document_id_stu.text = info_stu['ced_stu']
                    content.ids.age_stu.text = str(info_stu['age_stu'])

            elif self.user_type == 'Docente':
                content = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 10

    MDBoxLayout:
        orientation: 'horizontal'
        size_hint_y: None 
        height: "50dp"
        md_bg_color: app.theme_cls.primary_color 
        radius: 20
        MDLabel:
            text: "Estudiante"
            font_style: 'Overline'  
            color: 1, 1, 1, 1  
            font_size: '20sp'
            halign: 'center'
            valign: 'center'

    MDGridLayout:
        cols: 2  
        spacing: 15
        
        MDTextField:
            id: name_stu
            icon_left: "account-circle"
            hint_text: "Nombre"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True
            
        MDTextField:
            id: lastname_stu
            icon_left: "account-circle"
            hint_text: "Apellidos"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True

        MDTextField:
            id: document_id_stu
            icon_left: "card-account-details"
            hint_text: "Cedula de Identidad"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True
            
            
        MDTextField:
            id: age_stu
            icon_left: "page-layout-body"
            hint_text: "Edad"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 150
            font_size: 15
            pos_hint: {"center_x": 0.5}
            readonly: True

''')
                if info_rol and info_stu:
                    content.ids.name_stu.text = info_stu['name_stu']
                    content.ids.lastname_stu.text = info_stu['lastna_stu']
                    content.ids.document_id_stu.text = info_stu['ced_stu']
                    content.ids.age_stu.text = str(info_stu['age_stu'])

            elif self.user_type == 'Administrativo':
                # Obtener la pantalla
                students_screen = self.root.get_screen('students_screen')
                student_list_box = students_screen.ids.student_list_box
                student_list_box.clear_widgets()

                db = connect_mongodb()
                if db:
                    try:
                        students = get_all_students(db)
                        if students:
                            for student in students:
                                student_card = StudentCard(
                                    name=student['name_stu'],
                                    lastname=student['lastna_stu'],
                                    ced=student['ced_stu'],
                                    age=student['age_stu'],
                                    student_id=str(student['ced_stu'])
                                )
                                student_list_box.add_widget(student_card)
                            self.root.current = 'students_screen' # Navegar a la pantalla
                        else:
                            self.show_error_dialog("No se encontraron estudiantes.")
                    except Exception as e:
                        self.show_error_dialog(f"Error al cargar estudiantes: {str(e)}")
                else:
                    self.show_error_dialog("Error al conectar a la base de datos.")
            
        elif screen_name == 'areas':
            content = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 10

    MDLabel:
        text: "Pantalla de Áreas"
        halign: 'center'
''')
        elif screen_name == 'docentes':
            content = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 10

    MDLabel:
        text: "Pantalla de Docentes"
        halign: 'center'
''')

        content_container.add_widget(content)

    def show_error_dialog(self, message):
        self.dialog = MDDialog(
            title='Advertencia',
            text=message,
            buttons=[MDFlatButton(text='OK', on_release=self.close)],
        )
        self.dialog.open()

    def logout(self):
        self.root.current = 'login'
        self.root.transition.direction = 'right'
        login_screen = self.root.get_screen('login')
        login_screen.ids.user.text = ''
        login_screen.ids.password.text = ''
        self.user_type = ''
        
    def close(self, *args):
        self.dialog.dismiss()


if __name__ == '__main__':
    CaipaApp().run()