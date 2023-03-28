from src.components.likes_dislikes import get_likes_dislike
from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect
from src.utils.permissions import check_editable


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
            user_id             INTEGER NOT NULL,
            comment             TEXT NOT NULL,
            time                TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            world_id            INTEGER NOT NULL REFERENCES worlds ON DELETE CASCADE,
            component_id        INTEGER NOT NULL,
            component_type      TEXT NOT NULL
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def add_comment(user_id, session_key, world_id, component_id, component_type, comment):
    """
    This function will be called when a user makes
    a comment on a component

    :param user_id: the id of the user commenting
    :param session_key: the session key of the user
    :param world_id: the id of the world the comment is in
    :param comment: the comment being made
    :param component_id: the id of the item being commented on
    :param component_type: the table name of the element being commented on

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        insert_request = """
            INSERT INTO comments(user_id, comment, world_id, component_id, component_type) VALUES
            (%s, %s, %s, %s, %s)
            RETURNING id
                    """
        cur.execute(insert_request, (user_id, comment, world_id, component_id, component_type))
        outcome = cur.fetchall()
        conn.commit()
        conn.close()
        if outcome != ():
            return [True, outcome[0][0]]
    return [False, -1]


def delete_comment(user_id, session_key, comment_id):
    """
    This function will delete a comment from the table.

    :param user_id: the id of the user deleting
    :param session_key: the user's session key
    :param comment_id: the id of the comment being deleted

    :return: True if deleted, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        user_check = """
            SELECT user_id, world_id FROM comments
            WHERE component_id = %s
            """
        cur.execute(user_check, [comment_id])
        outcome = cur.fetchall()
        if outcome:
            outcome = outcome[0]
            if check_editable(outcome[1], user_id, session_key) or outcome[0] == user_id:
                delete_request = """
                    DELETE FROM comments WHERE
                    component_id = %s
                    RETURNING id
                    """
                cur.execute(delete_request, [comment_id])
                outcome = cur.fetchall()
                if outcome != ():
                    conn.commit()
                    conn.close()
                    return True
    return False


def edit_comment(user_id, session_key, comment_id, comment):
    """
    This function will edit the text in a comment, given
    the user trying to is the one who posted the comment

    :param user_id: the is of the user editing
    :param session_key: the user's session key
    :param comment_id: the id of the comment being edited
    :param comment: the new comment text

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        edit_query = """
            UPDATE comments SET
            comment = %s
            WHERE id = %s AND user_id = %s
            RETURNING id
            """
        cur.execute(edit_query, (comment, comment_id, user_id))

        outcome = cur.fetchall()

        if outcome == ():
            conn.close()
            return False

        conn.commit()
        conn.close()
        return True

    return False


def get_comment(comment_id, user_id):
    """
    This function will get the info related to a comment

    :param comment_id: the id of the component with the comments
    :param user_id: the id of the user signed in

    :return: info on the comment

    :format return: { user: { user_id: user's id,
                              user_name: user's name,
                              profile_picture: user's profile picture},
                      comment: the comment,
                      time: the time stamp of the comment
                      like_info: {
                          likes: int of likes,
                          dislikes: int of dislikes
                          user_like: is user liked it (True or False),
                          user_dislike: is user disliked it (True or False)
                      }
                    }
    """
    conn = connect()
    cur = conn.cursor()

    comment_request = """
            SELECT users.id, users.username, users.profile_pic, comment, time FROM comments
                INNER JOIN users ON comments.user_id = users.id
            WHERE comments.id = %s
            """
    cur.execute(comment_request, [comment_id])
    results = cur.fetchall()

    conn.close()

    if results != ():
        results = results[0]
        values = {
            'user': {
                'user_id': results[0],
                'user_name': results[1],
                'profile_pic': results[2]
            },
            'comment': results[3],
            'time': results[4],
            'like_dislike_info': get_likes_dislike(user_id, comment_id, 'comments')
        }

        return values
    return {}


def get_component_comments(user_id, component_id, component_table):
    """
    This function will get the comments associated with
    a component and the info associated to them

    :param user_id: the id of the user signed in
    :param component_id: the id of the component with the comments
    :param component_table: the table of component with the comments

    :return: list of comments and their info

    :format: [{ user: { user_id: user's id,
                        user_name: user's name,
                        profile_picture: user's profile picture},
                comment: the comment,
                time: the time stamp of the comment
                like_dislike_info: {
                          likes: int of likes,
                          dislikes: int of dislikes
                          user_like: is user liked it (True or False),
                          user_dislike: is user disliked it (True or False)
                      }
            }]
    """
    if user_id is None:
        user_id = -1

    conn = connect()
    cur = conn.cursor()

    comment_request = """
        SELECT users.id AS commenter_id, users.username, users.profile_pic, comment, time, comments.id AS comment_id FROM comments
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
            'user': {'user_id': comment[0],
                     'user_name': comment[1],
                     'profile_pic': comment[2]},
            'comment': comment[3],
            'time': comment[4],
            'like_dislike_info': get_likes_dislike(user_id, comment[5], 'comments')
        })

    conn.close()
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
