"""Makes helper function for creating, and inserting into a postgres database"""
import psycopg2


def conn_curs():
    """
    makes a connection to the database dont worry these are dummy keys
    """
    dbname = "abcdefgh"
    password = "Acka-1jfue4-snYmkall"
    host = "db.elephantsql.com"

    connection = psycopg2.connect(dbname=dbname, user=dbname,
                                  password=password, host=host)
    cursor = connection.cursor()
    return connection, cursor


def create_table():
    """
    creates the table posts, could be more modular but we really were gonna use the entire db for one table so i saw
    no need
    """
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
    """
    inserts a single post into the database

    @param text: str, the title and the posts text as one string
    @param sub: text str, the subreddit this post belongs to
    @param sub_id: str, subreddit's id for this sub
    @param num_com: int, number of comments on this post
    @param up: int, number of upvotes on this post
    @param down: int, number of downvotes on this post
    @param flair: str, the flair on the post, if None then 'None'
    @param vid: bool/str, a sql bool so a python string 'true' or 'false' whether or not
    the post contains a video
    @param num_awards: int, number of awards a post recieved
    """
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
