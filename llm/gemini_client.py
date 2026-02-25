import os, json, time
from google import genai

class GeminiClient:
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key: 
            raise ValueError("⚠️ No se encontró la variable GOOGLE_API_KEY")
        
        self.client = genai.Client(api_key=api_key)
        
        # Usamos el modelo exacto que apareció en tu lista
        # Este es el modelo de última generación disponible en tu cuenta
        self.model_id = "gemini-2.5-flash"

    def evaluate_code(self, code: str, problem_desc: str, passed: bool):
        prompt = f"""
        Actúa como un Senior Software Engineer.
        Evalúa este código Python para el problema: '{problem_desc}'
        ¿Pasó los tests técnicos?: {passed}
        
        Código del usuario:
        {code}
        
        Responde ÚNICAMENTE con un JSON puro con esta estructura:
        {{
          "Score": (int entre 0 y 100),
          "Correctness": "explicación",
          "Efficiency": "análisis Big O",
          "Readability": "comentario",
          "Suggestions": ["lista de strings"]
        }}
        """
        
        for attempt in range(3):
            try:
                # Llamada usando el modelo 2.5 Flash de tu lista
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt
                )
                
                # Limpiar la respuesta del LLM
                text = response.text
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0]
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0]
                
                return json.loads(text.strip())
                
            except Exception as e:
                if "429" in str(e):
                    print(f"⚠️ Cuota agotada (2.5 Flash). Esperando 12s... (Intento {attempt+1})")
                    time.sleep(12)
                else:
                    print(f"❌ Error con {self.model_id}: {e}")
                    # Si falla, intentamos con el modelo 'pro' de tu lista como último recurso
                    self.model_id = "gemini-2.5-pro"
                    continue
                    
        return {"Score": 0, "Correctness": "No se pudo conectar con los modelos 2.5"}