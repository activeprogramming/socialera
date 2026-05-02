import json
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# -------------------- GESTIÓN DE PROGRESO (JSON) --------------------
ARCHIVO_PROGRESO = "progreso.json"

def cargar_progreso():
    if os.path.exists(ARCHIVO_PROGRESO):
        with open(ARCHIVO_PROGRESO, "r") as f:
            return json.load(f)
    else:
        # Datos iniciales: todas las misiones bloqueadas excepto la 1
        return {
            "puntaje_total": 0,
            "misiones": [
                {"id": 0, "nombre": "Grecia", "completada": False, "puntaje": 0, "desbloqueada": True},
                {"id": 1, "nombre": "Roma", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 2, "nombre": "Egipto", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 3, "nombre": "Mayas", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 4, "nombre": "China", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 5, "nombre": "Edad Media", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 6, "nombre": "Renacimiento", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 7, "nombre": "Revolución Francesa", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 8, "nombre": "Independencia", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 9, "nombre": "Globalización", "completada": False, "puntaje": 0, "desbloqueada": False}
            ]
        }

def guardar_progreso(datos):
    with open(ARCHIVO_PROGRESO, "w") as f:
        json.dump(datos, f)

# -------------------- PANTALLAS --------------------
class MenuScreen(Screen):
    def on_enter(self):
        datos = cargar_progreso()
        self.ids.puntaje_label.text = f"Puntaje total: {datos['puntaje_total']} pts"

    def reiniciar_juego(self):
        datos_iniciales = {
            "puntaje_total": 0,
            "misiones": [
                {"id": 0, "nombre": "Grecia", "completada": False, "puntaje": 0, "desbloqueada": True},
                {"id": 1, "nombre": "Roma", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 2, "nombre": "Egipto", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 3, "nombre": "Mayas", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 4, "nombre": "China", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 5, "nombre": "Edad Media", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 6, "nombre": "Renacimiento", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 7, "nombre": "Revolución Francesa", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 8, "nombre": "Independencia", "completada": False, "puntaje": 0, "desbloqueada": False},
                {"id": 9, "nombre": "Globalización", "completada": False, "puntaje": 0, "desbloqueada": False}
            ]
        }
        guardar_progreso(datos_iniciales)
        self.on_enter()
        pop = Popup(title="Juego reiniciado", 
                    content=Label(text="Todo el progreso se ha borrado."),
                    size_hint=(0.6,0.3))
        pop.open()

class MapaScreen(Screen):
    def on_enter(self):
        datos = cargar_progreso()
        # Actualizar texto de cada botón según si está desbloqueada/completada
        for mision in datos["misiones"]:
            btn_id = f"btn_m{mision['id']}"
            if btn_id in self.ids:
                if mision["completada"]:
                    self.ids[btn_id].text = f"✅ {mision['nombre']} (completada)"
                elif mision["desbloqueada"]:
                    self.ids[btn_id].text = f"🔓 {mision['nombre']}"
                else:
                    self.ids[btn_id].text = f"🔒 {mision['nombre']} (bloqueada)"
                    self.ids[btn_id].disabled = True
                # Habilitar si está desbloqueada
                if mision["desbloqueada"]:
                    self.ids[btn_id].disabled = False

class MisionDetalleScreen(Screen):
    mision_id = NumericProperty(0)
    titulo = StringProperty("")
    historia = StringProperty("")
    opcionA_texto = StringProperty("")
    opcionB_texto = StringProperty("")
    pesoA = NumericProperty(0)
    pesoB = NumericProperty(0)
    retroA = StringProperty("")
    retroB = StringProperty("")
    
    def on_pre_enter(self):
        # Cargar contenido de la misión según su ID
        misiones_contenido = {
            0: {
                "titulo": "🏛️ Grecia Antigua",
                "historia": "Eres un estratega en el año 431 a.C. Atenas y Esparta se disputan el control. Tu decisión afectará el futuro de la Hélade.",
                "opcionA": "Atenas (democracia, arte y comercio)",
                "opcionB": "Esparta (disciplina militar y austeridad)",
                "pesoA": 20,
                "pesoB": 20,
                "retroA": "Apoyaste a Atenas. La democracia florece pero la guerra se prolonga. +20 puntos.",
                "retroB": "Apoyaste a Esparta. La disciplina gana pero el arte se oscurece. +20 puntos."
            },
            1: {
                "titulo": "🏛️ Imperio Romano",
                "historia": "Eres cónsul en el año 50 a.C. ¿Construyes acueductos para el pueblo o fortaleces las legiones?",
                "opcionA": "Construir acueductos (bienestar social)",
                "opcionB": "Fortificar legiones (poder militar)",
                "pesoA": 20,
                "pesoB": 20,
                "retroA": "El pueblo te ama. El imperio progresa con agua y salud. +20 pts",
                "retroB": "Roma expande su frontera. Eres temido pero respetado. +20 pts"
            },
            2: {
                "titulo": "🏺 Antiguo Egipto",
                "historia": "Eres faraón. ¿Inviertes en una gran pirámide para la eternidad o mejoras las cosechas con canales?",
                "opcionA": "Construir una gran pirámide",
                "opcionB": "Construir canales de riego",
                "pesoA": 20,
                "pesoB": 20,
                "retroA": "La pirámide asombra al mundo. Tu legado es eterno. +20 pts",
                "retroB": "Las cosechas abundan, el pueblo está feliz. +20 pts"
            },
            3: {
                "titulo": "🗿 Civilización Maya",
                "historia": "Tu ciudad-estado en decadencia. ¿Preservas el conocimiento astronómico o migras al norte?",
                "opcionA": "Preservar códices y ciencia",
                "opcionB": "Migrar en busca de tierras fértiles",
                "pesoA": 20,
                "pesoB": 20,
                "retroA": "Los sacerdotes guardan la sabiduría. Eres recordado. +20 pts",
                "retroB": "Sobrevives pero pierdes parte de tu legado. +20 pts"
            },
            4: {
                "titulo": "🐉 China Imperial",
                "historia": "Eres consejero del emperador. ¿Construyes la Gran Muralla o abres la Ruta de la Seda?",
                "opcionA": "Construir la Gran Muralla",
                "opcionB": "Abrir la Ruta de la Seda",
                "pesoA": 20,
                "pesoB": 20,
                "retroA": "El imperio está protegido de nómadas. Seguridad. +20 pts",
                "retroB": "El comercio trae riqueza y cultura. +20 pts"
            },
            5: {
                "titulo": "⚔️ Edad Media",
                "historia": "Eres un señor feudal. ¿Construyes una catedral para la fe o fortificas tu castillo?",
                "opcionA": "Construir una catedral",
                "opcionB": "Fortificar el castillo",
                "pesoA": 20,
                "pesoB": 20,
                "retroA": "La catedral eleva el espíritu. Peregrinos te honran. +20 pts",
                "retroB": "Tu castillo resiste invasiones. +20 pts"
            },
            6: {
                "titulo": "🎨 Renacimiento",
                "historia": "Eres mecenas en Florencia. ¿Financias a Da Vinci o a un ejército para proteger la ciudad?",
                "opcionA": "Financiar a Da Vinci",
                "opcionB": "Financiar un ejército",
                "pesoA": 20,
                "pesoB": 20,
                "retroA": "El arte florece. La Mona Lisa existirá. +20 pts",
                "retroB": "La ciudad está segura pero el arte se retrasa. +20 pts"
            },
            7: {
                "titulo": "⚜️ Revolución Francesa",
                "historia": "Estás en la Asamblea. ¿Apoyas a los girondinos (moderados) o jacobinos (radicales)?",
                "opcionA": "Girondinos (reformas lentas)",
                "opcionB": "Jacobinos (cambio rápido y violento)",
                "pesoA": 20,
                "pesoB": 20,
                "retroA": "Francia avanza sin tanto terror. +20 pts",
                "retroB": "La república nace entre sangre. +20 pts"
            },
            8: {
                "titulo": "🇲🇽 Independencia de México",
                "historia": "1810. ¿Sigues a Hidalgo o a Iturbide?",
                "opcionA": "Unirte a Hidalgo (levantamiento popular)",
                "opcionB": "Unirte a Iturbide (ejército realista)",
                "pesoA": 20,
                "pesoB": 20,
                "retroA": "Luchas por la libertad. +20 pts",
                "retroB": "Logras independencia conservadora. +20 pts"
            },
            9: {
                "titulo": "🌍 Globalización",
                "historia": "Eres líder mundial. ¿Aprietas el comercio global o proteges lo local?",
                "opcionA": "Libre comercio mundial",
                "opcionB": "Proteccionismo local",
                "pesoA": 20,
                "pesoB": 20,
                "retroA": "Riqueza global pero desigualdad. +20 pts",
                "retroB": "Industria local protegida. +20 pts"
            }
        }
        cont = misiones_contenido[self.mision_id]
        self.titulo = cont["titulo"]
        self.historia = cont["historia"]
        self.opcionA_texto = cont["opcionA"]
        self.opcionB_texto = cont["opcionB"]
        self.pesoA = cont["pesoA"]
        self.pesoB = cont["pesoB"]
        self.retroA = cont["retroA"]
        self.retroB = cont["retroB"]
        
        # Verificar si ya fue completada
        datos = cargar_progreso()
        mision_datos = datos["misiones"][self.mision_id]
        if mision_datos["completada"]:
            self.ids.mensaje_completada.text = "✅ Ya completaste esta misión. No puedes repetir."
            self.ids.btn_opcionA.disabled = True
            self.ids.btn_opcionB.disabled = True
        else:
            self.ids.mensaje_completada.text = ""
            self.ids.btn_opcionA.disabled = False
            self.ids.btn_opcionB.disabled = False
    
    def elegir_opcion(self, opcion):
        # Sumar puntaje y marcar completada
        datos = cargar_progreso()
        if datos["misiones"][self.mision_id]["completada"]:
            return
        # Sumar puntos según opción
        puntos = self.pesoA if opcion == 'A' else self.pesoB
        datos["puntaje_total"] += puntos
        datos["misiones"][self.mision_id]["completada"] = True
        datos["misiones"][self.mision_id]["puntaje"] = puntos
        
        # Desbloquear siguiente misión (si no es la última)
        if self.mision_id + 1 < len(datos["misiones"]):
            datos["misiones"][self.mision_id + 1]["desbloqueada"] = True
        
        guardar_progreso(datos)
        
        # Mostrar mensaje de retroalimentación
        mensaje = self.retroA if opcion == 'A' else self.retroB
        pop = Popup(title="Decisión histórica",
                    content=Label(text=f"{mensaje}\n\n+{puntos} puntos"),
                    size_hint=(0.7, 0.4))
        pop.open()
        # Volver al mapa después de cerrar
        def regresar(inst):
            self.manager.current = 'mapa'
        pop.bind(on_dismiss=regresar)

class LogrosScreen(Screen):
    def on_enter(self):
        datos = cargar_progreso()
        completadas = sum(1 for m in datos["misiones"] if m["completada"])
        total = len(datos["misiones"])
        self.ids.resumen.text = f"Has completado {completadas} de {total} misiones.\nPuntaje total: {datos['puntaje_total']}\n\n¡Sigue aprendiendo!"
        
    def regresar_menu(self):
        self.manager.current = 'menu'

# -------------------- GESTOR DE PANTALLAS --------------------
class HistoriaVivaApp(App):
    def build(self):
        Window.set_icon('icono.png')
        Window.title = 'Historia Viva - Ciencias Sociales'
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MapaScreen(name='mapa'))
        sm.add_widget(MisionDetalleScreen(name='mision_detalle'))
        sm.add_widget(LogrosScreen(name='logros'))
        return sm

if __name__ == '__main__':
    HistoriaVivaApp().run()