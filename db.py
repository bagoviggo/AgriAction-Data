"""Thin Postgres helper. Schema is owned by the Next.js Prisma app
(see agriaction-web/prisma/schema.prisma); this service only reads and writes rows."""
import os
import psycopg2

def get_connection():
    url = os.getenv("DATABASE_URL")
    if not url:
        return None
    return psycopg2.connect(url)

def log_message(conn, ward_id: str, module: str, content: str, status: str):
    if conn is None:
        print(f"[NO DB] Would log: ward={ward_id} module={module} status={status}")
        return
    with conn.cursor() as cur:
        cur.execute(
            'INSERT INTO "MessageLog" (id, "wardId", module, content, status, "sentAt") '
            "VALUES (gen_random_uuid(), %s, %s, %s, %s, now())",
            (ward_id, module, content, status),
        )
    conn.commit()

def get_active_wards(conn) -> list[dict]:
    if conn is None:
        return []
    with conn.cursor() as cur:
        cur.execute('SELECT id, name, lat, lon FROM "Ward"')
        rows = cur.fetchall()
    return [{"id": r[0], "name": r[1], "lat": r[2], "lon": r[3]} for r in rows]
