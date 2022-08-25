from src.utils.db_utils import connect


def rebuild_comments_table():
    """
    This function will empty the comments table.
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS comments CASCADE;
        """
    create_sql = """
        CREATE TABLE comments(
            id                  SERIAL PRIMARY KEY,
            user_id             TEXT NOT NULL,
            comment             TEXT NOT NULL,
            time                TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            likes               INTEGER DEFAULT 0,
            dislikes            INTEGER DEFAULT 0,
            component_id        INTEGER NOT NULL,
            component_type      TEXT NOT NULL
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def get_component_comments(component_id, component_table):
    """
    This function will get the comments associated with
    a component and the info associated to them

    :param component_id: the id of the component with the comments
    :param component_table: the table of component with the comments

    :return: list of comments and their info

    :format: [{ user: { user_id: user's id,
                        user_name: user's name,
                        profile_picture: user's profile picture},
                comment: the comment,
                time: the time stamp of the comment
                likes: int of likes,
                dislikes: int of dislikes
            }]
    """
    conn = connect()
    cur = conn.cursor()

    comment_request = """
        SELECT users.id, users.name, users.profile_pic, comment, time, likes, dislikes FROM comments
            INNER JOIN users ON users.id = comments.user_id
        WHERE component_id = %s AND component_type = %s
        """
    cur.execute(comment_request, (component_id, component_table))
    results = cur.fetchall()
    conn.close()

    # compile the comments
    data = []
    for comment in results:
        data.append({
            'user':   {'user_id':     comment[0],
                       'user_name':   comment[1],
                       'profile_pic': comment[2]},
            'comment':  comment[3],
            'time':     comment[4],
            'likes':    comment[5],
            'dislikes': comment[6]
        })
    return data


def get_user_comments(user_id, limit, page):
    """
    This function will get the comments made by a
    user with a page limit and selection

    :param user_id: the id of the user being checked
    :param limit: the amount of comments to return
        (if none, default 25)
    :param page: the offset of the comment page
    """

    conn = connect()
    cur = conn.cursor()

    if limit is None:
        limit = 25

    request = """
        SELECT * FROM comments
        WHERE user_id = %s
        LIMIT %s OFFSET %s
        """
    cur.execute(request, (user_id, limit, (page - 1) * limit))
    outcome = cur.fetchall()

    conn.close()

    return outcome
