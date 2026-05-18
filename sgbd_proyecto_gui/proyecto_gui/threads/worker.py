"""Módulo para el manejo de hilos (threads) y evitar el bloqueo de la GUI."""

import threading
from typing import Callable, Any

class BackgroundWorker(threading.Thread):
    """
    Clase que ejecuta una tarea pesada en un hilo en segundo plano.
    ¿Por qué un hilo? Tkinter corre en un único "Hilo Principal" (Main Thread).
    Si hacemos un cálculo lento o acceso I/O ahí, la ventana se congela.
    """

    def __init__(self, target: Callable, ui_after_method: Callable, 
                 on_success: Callable = None, on_error: Callable = None, 
                 args: tuple = ()):
        super().__init__()
        self.target = target
        self.ui_after_method = ui_after_method
        self.on_success = on_success
        self.on_error = on_error
        self.args = args
        self.daemon = True  # El hilo muere si se cierra la ventana principal

    def run(self) -> None:
        try:
            # Ejecutamos la tarea pesada bloqueante en este hilo secundario
            resultado = self.target(*self.args)
            
            # Al terminar, no podemos actualizar la GUI directamente. 
            # Inyectamos el resultado en la cola de eventos del Hilo Principal usando `after()`.
            if self.on_success:
                self.ui_after_method(0, lambda: self.on_success(resultado))
                
        except Exception as e:
            if self.on_error:
                self.ui_after_method(0, lambda: self.on_error(e))
