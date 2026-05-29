from openai import AzureOpenAI
import config
from ai.search import load_context

_DEPT_NAME = {
    "ops": "Operaciones",
    "ventas": "Ventas",
}

_SYSTEM_TEMPLATE = """Eres el asistente IA interno del departamento de {dept_name} de Northwind Traders.
Tu función es responder preguntas de los empleados usando la documentación interna del departamento.

Instrucciones:
- Responde SOLO con información de los documentos proporcionados.
- Cuando uses información de un documento, menciona su nombre (por ejemplo: "Según la Política de Inventario...").
- Si la respuesta no está en los documentos, dilo claramente: "No tengo esa información en los documentos disponibles."
- Responde en español, de forma clara y concisa.
- No inventes datos, cifras ni procedimientos que no estén en los documentos.

DOCUMENTACIÓN INTERNA DEL DEPARTAMENTO:
{context}"""


def get_ai_response(user_message: str, department: str, history: list) -> str:
    if not config.AZURE_OPENAI_API_KEY or not config.AZURE_OPENAI_ENDPOINT:
        return (
            "El agente IA no está configurado. "
            "Configura AZURE_OPENAI_ENDPOINT y AZURE_OPENAI_API_KEY en las variables de entorno del App Service."
        )

    client = AzureOpenAI(
        api_key=config.AZURE_OPENAI_API_KEY,
        azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
        api_version="2024-02-01",
    )

    context = load_context(department)
    dept_name = _DEPT_NAME.get(department, "Operaciones")

    system_prompt = _SYSTEM_TEMPLATE.format(dept_name=dept_name, context=context)

    messages = [{"role": "system", "content": system_prompt}]

    for turn in history[-10:]:
        messages.append({"role": turn["role"], "content": turn["content"]})

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=config.AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
        max_tokens=800,
        temperature=0.2,
    )

    return response.choices[0].message.content
