from application.clasificar_caso import ClasificarCaso


class CLIController:
    def __init__(self, caso_use_case: ClasificarCaso):
        self.caso_use_case = caso_use_case

    def run(self):
        while True:
            txt = input("\nDescriba el problema (o 'salir'): ").strip()
            if txt.lower() == "salir":
                break
            try:
                id_caso = self.caso_use_case.ejecutar(txt)
                print(f"Caso registrado con ID: {id_caso}")
            except Exception as e:
                print("Error:", e)