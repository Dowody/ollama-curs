import psycopg2
import ollama

CONN_INFO = "host=localhost port=5433 dbname=at_data_db user=vlada password=abc"


def calcEmbed(text, model="nomic-embed-text"):
    response = ollama.embeddings(
        model=model,
        prompt=text,
    )
    return response["embedding"]


def updateVector():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(CONN_INFO)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(
            "SELECT id, page, title, context FROM at_data "
            "WHERE page_vector IS NULL OR title_vector IS NULL OR context_vector IS NULL"
        )
        rows = cur.fetchall()

        print(f"Updating {len(rows)}")

        for row in rows:
            row_id, page, title, context = row

            page_vec = calcEmbed(page)
            title_vec = calcEmbed(title)
            context_vec = calcEmbed(context)

            cur.execute(
                "UPDATE at_data SET page_vector = %s, title_vector = %s, "
                "context_vector = %s WHERE id = %s",
                (page_vec, title_vec, context_vec, row_id),
            )

            print("Updated!")

    except Exception as e:
        print("Error:", e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    updateVector()
