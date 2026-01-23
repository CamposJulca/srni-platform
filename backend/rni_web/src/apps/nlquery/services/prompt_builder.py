from typing import Dict


class PromptBuilder:
    """
    PromptBuilder
    -------------
    Construye un prompt determinista y auditable para sistemas NL2SQL.

    Responsabilidades:
    - Convertir el esquema PostgreSQL en contexto legible por un LLM
    - Inyectar reglas estrictas de generación SQL
    - Incorporar la pregunta del usuario sin ambigüedad

    Este módulo:
    - NO llama a la IA
    - NO ejecuta SQL
    - SOLO construye texto controlado
    """

    SYSTEM_INSTRUCTIONS = """
You are an expert SQL generator for PostgreSQL.

Your task is to translate a natural language question into a VALID SQL query.

STRICT RULES:
- Generate ONLY a single SQL SELECT statement.
- DO NOT use INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE.
- DO NOT invent tables or columns.
- Use ONLY the tables and columns provided in the schema.
- Use explicit JOINs when relationships are needed.
- Use table aliases for readability.
- If aggregation is required, use GROUP BY correctly.
- If a LIMIT is not specified, add LIMIT 100.
- DO NOT include explanations, comments, or markdown.
- Output ONLY raw SQL.
"""

    def build(self, schema: Dict, user_question: str) -> str:
        """
        Construye el prompt final para NL2SQL.

        :param schema: Diccionario del esquema filtrado (SchemaLoader)
        :param user_question: Pregunta en lenguaje natural del usuario
        :return: Prompt completo como string
        """

        schema_text = self._serialize_schema(schema)

        prompt = f"""
{self.SYSTEM_INSTRUCTIONS}

DATABASE SCHEMA:
{schema_text}

USER QUESTION:
{user_question}

SQL QUERY:
""".strip()

        return prompt

    def _serialize_schema(self, schema: Dict) -> str:
        """
        Convierte el esquema en texto estructurado y legible para el modelo.
        """

        lines = []

        for table, meta in schema.items():
            lines.append(f"TABLE {table}")
            lines.append("  COLUMNS:")

            for column, dtype in meta["columns"].items():
                lines.append(f"    - {column} ({dtype})")

            if meta.get("primary_key"):
                lines.append(f"  PRIMARY KEY: {meta['primary_key']}")

            if meta.get("foreign_keys"):
                lines.append("  FOREIGN KEYS:")
                for column, fk in meta["foreign_keys"].items():
                    lines.append(
                        f"    - {column} REFERENCES {fk['references']}"
                    )

            lines.append("")  # separación entre tablas

        return "\n".join(lines)
