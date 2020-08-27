import psycopg2


def conn_curs():
    dbname = "kplbotdt"
    password = "Ydvw5clyK3HO0otQBITuyJY_nyThD7-L"
    host = "lallah.db.elephantsql.com"

    connection = psycopg2.connect(dbname=dbname, user=dbname,
                                  password=password, host=host)
    cursor = connection.cursor()
    return connection, cursor


def create_table():
    conn, curs = conn_curs()
    create = """
    CREATE TABLE posts(
    id SERIAL PRIMARY KEY,
    title_selftext TEXT NOT NULL,
    subreddit VARCHAR(20) NOT NULL,
    subreddit_id VARCHAR(15) NOT NULL,
    num_comments INT NOT NULL,
    upvotes INT NOT NULL,
    downvotes INT NOT NULL,
    flair VARCHAR(20) NOT NULL,
    has_vid bool NOT NULL,
    num_awards INT NOT NULL)
    """
    curs.execute(create)
    conn.commit()
    return


def insert_post(text, sub, sub_id, num_com, up, down, flair, vid, num_awards):
    conn, curs = conn_curs()
    insert = f"""
    INSERT INTO posts (
    title_selftext, subreddit, subreddit_id,
    num_comments, upvotes, downvotes,
    flair, has_vid, num_awards)
    VALUES ('{text}', '{sub}', '{sub_id}', {num_com}, {up}, {down}, '{flair}', {vid}, {num_awards})
    """
    curs.execute(insert)
    conn.commit()
    return
