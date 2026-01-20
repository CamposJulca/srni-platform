from django.db import connection


class SchemaLoader:
    """
    SchemaLoader
    ------------
    Extrae el esquema REAL de PostgreSQL (schema public),
    filtrando únicamente las tablas de dominio de negocio
    permitidas para consultas NL2SQL.

    - No usa modelos Django
    - No infiere ni inventa estructuras
    - Diseñado para IA + control simbólico
    """

    # === WHITELIST DE TABLAS DE DOMINIO ===
    # Ajusta aquí si el modelo evoluciona
    ALLOWED_TABLES = {
        "colaborador",
        "contrato",
        "actividad",
        "proyecto",
        "procedimiento",
        "equipo",
        "articulacion",
        "colaborador_contrato",
    }

    def load(self) -> dict:
        """
        Retorna un diccionario con el esquema filtrado:
        {
          table_name: {
            columns: { column: type },
            primary_key: str | None,
            foreign_keys: {
              column: {
                references: "table.column"
              }
            }
          }
        }
        """
        schema: dict[str, dict] = {}

        with connection.cursor() as cursor:

            # 1. Obtener tablas reales del schema public
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_type = 'BASE TABLE';
            """)

            all_tables = {row[0] for row in cursor.fetchall()}

            # 2. Aplicar whitelist
            tables = sorted(all_tables.intersection(self.ALLOWED_TABLES))

            for table in tables:
                schema[table] = {
                    "columns": {},
                    "primary_key": None,
                    "foreign_keys": {}
                }

                # 3. Columnas y tipos
                cursor.execute("""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                      AND table_name = %s
                    ORDER BY ordinal_position;
                """, [table])

                for column_name, data_type in cursor.fetchall():
                    schema[table]["columns"][column_name] = data_type

                # 4. Clave primaria
                cursor.execute("""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                      ON tc.constraint_name = kcu.constraint_name
                     AND tc.table_schema = kcu.table_schema
                    WHERE tc.table_schema = 'public'
                      AND tc.table_name = %s
                      AND tc.constraint_type = 'PRIMARY KEY';
                """, [table])

                pk = cursor.fetchone()
                if pk:
                    schema[table]["primary_key"] = pk[0]

                # 5. Claves foráneas
                cursor.execute("""
                    SELECT
                        kcu.column_name,
                        ccu.table_name AS foreign_table,
                        ccu.column_name AS foreign_column
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                      ON tc.constraint_name = kcu.constraint_name
                     AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage ccu
                      ON ccu.constraint_name = tc.constraint_name
                     AND ccu.table_schema = tc.table_schema
                    WHERE tc.table_schema = 'public'
                      AND tc.constraint_type = 'FOREIGN KEY'
                      AND tc.table_name = %s;
                """, [table])

                for column, foreign_table, foreign_column in cursor.fetchall():
                    # Solo referenciar FKs hacia tablas permitidas
                    if foreign_table in self.ALLOWED_TABLES:
                        schema[table]["foreign_keys"][column] = {
                            "references": f"{foreign_table}.{foreign_column}"
                        }

        return schema
