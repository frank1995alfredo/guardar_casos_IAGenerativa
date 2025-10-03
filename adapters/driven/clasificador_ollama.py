from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from domain.entities import Tecnico
from application.clasificar_caso import ClasificadorPort, TecnicoSelectorPort

class OllamaClasificador(ClasificadorPort):
    
    def __init__(self, model: str = "qwen2.5-coder:14b"):
        self.chain = (PromptTemplate.from_template(
            "Clasifica en UNA de estas opciones:\n{opciones}\n\nProblema: {texto}\nCategoría:")
            | OllamaLLM(model=model)
            | StrOutputParser())

    def clasificar(self, texto: str, opciones: list[str]) -> str:
        return self.chain.invoke({"texto": texto, "opciones": "\n".join(opciones)}).strip()

class OllamaTecnicoSelector(TecnicoSelectorPort):
    def __init__(self, model: str = "qwen2.5-coder:14b"):
        self.chain = (PromptTemplate.from_template(
            """Ejemplos:
                - problema con SAP              → Administrador SAP
                - impresora atascada            → Ingeniero de Infraestructura

                Problema: {texto}
                Lista:
                {lista}
                Devuelve solo el ID:""")
                            | OllamaLLM(model=model)
                            | StrOutputParser())

    def seleccionar(self, texto: str, tecnicos: list[Tecnico]) -> Tecnico:
        lista = "\n".join([f"{t.id} - {t.nombre} - {t.area}" for t in tecnicos])
        resp = self.chain.invoke({"texto": texto, "lista": lista}).strip()
        elegido = int(resp) if resp.isdigit() else tecnicos[0].id
        return next(t for t in tecnicos if t.id == elegido)