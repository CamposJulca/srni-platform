import os
from typing import Optional

from openai import OpenAI


class SQLGenerator:
    """
    SQLGenerator
    ------------
    Encapsula la llamada al modelo de lenguaje para transformar
    un prompt NL2SQL en una consulta SQL pura.

    - NO ejecuta SQL
    - NO valida SQL
    - SOLO devuelve texto SQL
    """

    def __init__(
        self,
        model: str = "gpt-4.1-mini",
        temperature: float = 0.0,
        max_tokens: int = 500,
    ):
        """
        :param model: Modelo LLM a utilizar
        :param temperature: Determinismo (0.0 recomendado)
        :param max_tokens: Límite de tokens de salida
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, prompt: str) -> str:
        """
        Envía el prompt al LLM y retorna SOLO SQL limpio.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You generate SQL queries only.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        sql = response.choices[0].message.content.strip()

        return self._sanitize(sql)

    @staticmethod
    def _sanitize(sql: str) -> str:
        """
        Limpieza defensiva mínima.
        El validador estricto viene después.
        """
        return sql.rstrip(";").strip()
