# 🚀 PocketFlow Code Validator (AI-Powered)

Este proyecto es un motor de evaluación de código automatizado que utiliza la arquitectura de **PocketFlow** para orquestar la ejecución de pruebas unitarias y la validación cualitativa mediante Inteligencia Artificial (**Gemini 2.5 Flash**).

Inspirado en plataformas como LeetCode, este sistema no solo verifica si el código "funciona", sino que analiza su eficiencia, legibilidad y ofrece sugerencias de mejora técnica de nivel Senior.

## 🏗️ Arquitectura del Sistema

El proyecto sigue una arquitectura modular basada en **Nodos de Flujo**:

1.  **LoaderNode**: Gestiona la carga de problemas y soluciones locales.
2.  **ExecNode**: Motor de ejecución segura que valida el código contra casos de prueba JSON.
3.  **LLMNode**: Agente de IA que realiza el análisis estático y genera el feedback profesional.



---

## 🛠️ Tecnologías Utilizadas

* **Python 3.10+**
* **Google GenAI SDK**: Integración con modelos Gemini 2.5.
* **PocketFlow Logic**: Framework minimalista para el manejo de estados compartidos y flujos.
* **Subprocess API**: Ejecución aislada de código de usuario.

## 🚀 Instalación y Configuración

### 1. Clonar y Preparar el Entorno
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar API Key

Debes contar con una clave de Google AI Studio configurada en tu entorno:

export GOOGLE_API_KEY="TU_API_KEY_AQUI"

## Autores

Jorge Gomez

Shirley Leal

