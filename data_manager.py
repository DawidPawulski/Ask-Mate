import database_common
from psycopg2 import sql
import datetime

dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")



@database_common.connection_hanlder
def get_questions_by_key(cursor, sortkey, sort_order, limit_on_off):

	if limit_on_off == "limit_on":
		if sort_order == 'ASC':
			cursor.execute(sql.SQL("SELECT * FROM question ORDER BY {sortkey} ASC LIMIT 5").format(
				sortkey=sql.Identifier(sortkey)))
		elif sort_order == 'DESC':
			cursor.execute(sql.SQL("SELECT * FROM question ORDER BY {sortkey} DESC LIMIT 5").format(
				sortkey=sql.Identifier(sortkey)))
	elif limit_on_off == "limit_off":
		if sort_order == 'ASC':
			cursor.execute(
				sql.SQL("SELECT * FROM question ORDER BY {sortkey} ASC").format(sortkey=sql.Identifier(sortkey)))
		elif sort_order == 'DESC':
			cursor.execute(
				sql.SQL("SELECT * FROM question ORDER BY {sortkey} DESC").format(sortkey=sql.Identifier(sortkey)))

	questions = cursor.fetchall()
	return questions


@database_common.connection_hanlder
def get_question_by_id(cursor, question_id):
	cursor.execute("""
	                SELECT * FROM question
	                WHERE id = %(question_id)s;
	               """,
	               {'question_id': question_id})
	question = cursor.fetchall()[0]
	return question


@database_common.connection_hanlder
def get_answers_by_question_id(cursor, question_id):
	cursor.execute("""
	                SELECT * FROM answer 
	                WHERE question_id = %(question_id)s ORDER BY submission_time DESC;
	               """,
	               {'question_id': question_id})
	answers = cursor.fetchall()
	return answers


@database_common.connection_hanlder
def add_new_question(cursor, question):
	cursor.execute("""
	                INSERT INTO question (submission_time ,title, message, image, vote_number, view_number, user_id)
	                VALUES (%(submission_time)s, %(title)s, %(message)s, %(image)s, %(vote_number)s, %(view_number)s, %(user_id)s);
	               """,
	               {'title': question['title'],
	                'message': question['message'],
	                'image': question['image'],
	                'submission_time': dt,
	                'vote_number': 0,
	                'view_number': 0,
	                'user_id': question['user_id']})


@database_common.connection_hanlder
def delete_question(cursor, question_id):
	cursor.execute("""
	                DELETE FROM comment
	                WHERE question_id = %(question_id)s;
		               """,
	               {'question_id': question_id})

	cursor.execute("""
	                DELETE FROM answer
	                WHERE question_id = %(question_id)s;
		               """,
	               {'question_id': question_id})

	cursor.execute("""
	                DELETE FROM question
	                WHERE id = %(question_id)s;
		               """,
	               {'question_id': question_id})


@database_common.connection_hanlder
def update_question(cursor, question):
	cursor.execute("""
	                UPDATE question
	                SET title = %(title)s, message= %(message)s, image= %(image)s
	                WHERE id = %(question_id)s;
		               """,
	               {'question_id': question['question_id'],
	                'title': question['title'],
	                'message': question['message'],
	                'image': question['image']})


@database_common.connection_hanlder
def update_answer(cursor, answer, answer_id):
	cursor.execute("""
				UPDATE answer
				SET message = %(message)s,
					image = %(image)s
				WHERE id = %(answer_id)s;
				""", {'message': answer['message'], 'answer_id': answer_id, 'image': answer['image']})


@database_common.connection_hanlder
def get_answers_by_id(cursor, answer_id):
	cursor.execute("""
					SELECT * FROM answer WHERE id = %(answer_id)s;
					""", {'answer_id': answer_id})

	answer = cursor.fetchall()[0]

	return answer


@database_common.connection_hanlder
def add_answer(cursor, answer):
	cursor.execute("""
	                INSERT INTO answer (submission_time, message, question_id, image, vote_number, user_id)
	                VALUES (%(submission_time)s, %(message)s, %(question_id)s, %(image)s, %(vote_number)s, %(user_id)s);
	               """,
	               {'message': answer['message'],
	                'question_id': answer['question_id'],
	                'image': answer['image'],
	                'submission_time': dt,
	                'vote_number': 0,
	                'user_id': answer['user_id']})


@database_common.connection_hanlder
def delete_answer(cursor, answer_id):
	cursor.execute("""
	                DELETE FROM comment
	                WHERE answer_id = %(answer_id)s;
		               """,
	               {'answer_id': answer_id})
	cursor.execute("""
	                DELETE FROM answer
	                WHERE id = %(answer_id)s;
		               """,
	               {'answer_id': answer_id})


@database_common.connection_hanlder
def delete_comment(cursor, comment_id):
	cursor.execute("""
	                DELETE FROM comment
	                WHERE id = %(comment_id)s;
		               """,
	               {'comment_id': comment_id})


@database_common.connection_hanlder
def get_question_id_by_answer_id(cursor, answer_id):
	cursor.execute("""
	                SELECT question_id FROM answer
	                WHERE id = %(answer_id)s;
	               """,
	               {'answer_id': answer_id})
	question_id = cursor.fetchall()
	return question_id[0]['question_id']


@database_common.connection_hanlder
def get_question_id_by_comment_id(cursor, comment_id):
	cursor.execute("""
	                SELECT question_id FROM comment
	                WHERE id = %(comment_id)s;
	               """,
	               {'comment_id': comment_id})
	question_id = cursor.fetchall()
	return question_id[0]['question_id']


@database_common.connection_hanlder
def get_vote_number_by_question_id(cursor, question_id):
	cursor.execute("""
	                SELECT vote_number FROM question
	                WHERE id = %(question_id)s;
	               """,
	               {'question_id': question_id})
	votes = cursor.fetchall()
	return votes[0]['vote_number']


@database_common.connection_hanlder
def get_vote_number_by_answer_id(cursor, answer_id):
	cursor.execute("""
	                SELECT vote_number FROM answer
	                WHERE id = %(answer_id)s;
	               """,
	               {'answer_id': answer_id})
	votes = cursor.fetchall()
	return votes[0]['vote_number']


@database_common.connection_hanlder
def update_question_vote_number(cursor, question_id, vote_number):
	cursor.execute("""
	                UPDATE question
	                SET vote_number = %(vote_number)s
	                WHERE id = %(question_id)s;
		               """,
	               {'question_id': question_id,
	                'vote_number': vote_number})


@database_common.connection_hanlder
def update_answer_vote_number(cursor, answer_id, vote_number):
	cursor.execute("""
	                UPDATE answer
	                SET vote_number = %(vote_number)s
	                WHERE id = %(answer_id)s;
		               """,
	               {'answer_id': answer_id,
	                'vote_number': vote_number})


@database_common.connection_hanlder
def update_views_number(cursor, question_id, up_or_down_views):
	cursor.execute("""
	                UPDATE question
	                SET view_number = view_number + %(up_or_down_views)s
	                WHERE id = %(question_id)s;
		               """,
	               {'question_id': question_id,
	                'up_or_down_views': up_or_down_views})


@database_common.connection_hanlder
def get_question_by_phrase(cursor, phrase):
	cursor.execute("""
					SELECT * FROM question WHERE UPPER(title) LIKE UPPER('%%' || %(phrase)s || '%%') 
					OR UPPER(message) LIKE UPPER('%%' || %(phrase)s || '%%');
					""", {'phrase': phrase})

	questions = cursor.fetchall()

	return questions


@database_common.connection_hanlder
def get_answer_by_phrase(cursor, phrase):
	cursor.execute("""
					SELECT * FROM answer WHERE UPPER(message) LIKE UPPER('%%' || %(phrase)s || '%%');
					""", {'phrase': phrase})

	answers = cursor.fetchall()

	return answers


@database_common.connection_hanlder
def add_question_comment(cursor, comment):
	cursor.execute("""
	                INSERT INTO comment (submission_time, message, question_id, user_id)
	                VALUES (%(submission_time)s, %(message)s, %(question_id)s, %(user_id)s);
	               """,
	               {'message': comment['message'],
	                'question_id': comment['question_id'],
	                'submission_time': dt,
	                'user_id': comment['user_id']})


@database_common.connection_hanlder
def get_question_comments(cursor, question_id):
	cursor.execute("""
	                SELECT * FROM comment
	                WHERE question_id = %(question_id)s AND answer_id IS NULL;
	               """,
	               {'question_id': question_id})
	comments = cursor.fetchall()
	return comments


@database_common.connection_hanlder
def add_answer_comment(cursor, comment):
	cursor.execute("""
	                INSERT INTO comment (submission_time, message, question_id, answer_id, user_id)
	                VALUES (%(submission_time)s, %(message)s, %(question_id)s, %(answer_id)s, %(user_id)s);
	               """,
	               {'message': comment['message'],
	                'question_id': comment['question_id'],
	                'submission_time': dt,
	                'answer_id': comment['answer_id'],
	                'user_id': comment['user_id']})


@database_common.connection_hanlder
def get_answer_comments(cursor, question_id):
	cursor.execute("""
	                SELECT * FROM comment
	                WHERE question_id = %(question_id)s AND answer_id IS NOT NULL;
	               """,
	               {'question_id': question_id})
	comments = cursor.fetchall()
	return comments


@database_common.connection_hanlder
def get_comment_message_by_comment_id(cursor, comment_id):
	cursor.execute("""
	                SELECT message FROM comment
	                WHERE id = %(comment_id)s;
	               """,
	               {'comment_id': comment_id})
	comment = cursor.fetchall()[0]['message']
	return comment


@database_common.connection_hanlder
def update_comment_message(cursor, comment_id, comment_message):
	cursor.execute("""
	                UPDATE comment
	                SET message = %(comment_message)s
	                WHERE id = %(comment_id)s;
		               """,
	               {'comment_id': comment_id,
	                'comment_message': comment_message})


@database_common.connection_hanlder
def register_new_user(cursor, login, password):
	cursor.execute("""
				   INSERT INTO users(login, password) 
				   VALUES (%(login)s,%(password)s);
				   """, {'login':login,
						 'password':password})


@database_common.connection_hanlder
def get_comment_message_by_comment_id(cursor, comment_id):
	cursor.execute("""
	                SELECT message FROM comment
	                WHERE id = %(comment_id)s;
	               """,
	               {'comment_id': comment_id})
	comment = cursor.fetchall()[0]['message']
	return comment


@database_common.connection_hanlder
def update_comment_message(cursor, comment_id, comment_message):
	cursor.execute("""
	                UPDATE comment
	                SET message = %(comment_message)s
	                WHERE id = %(comment_id)s;
		               """,
	               {'comment_id': comment_id,
	                'comment_message': comment_message})


@database_common.connection_hanlder
def create_user_table_if_not_exist(cursor):
	cursor.execute("""
					CREATE TABLE IF NOT EXISTS users (
					user_id serial PRIMARY KEY,
					login varchar(24) UNIQUE NOT NULL,
					password text NOT NULL,
					reputation integer DEFAULT 0
					);
					""")


@database_common.connection_hanlder
def get_exist_users_info(cursor):
	cursor.execute("""
				   SELECT user_id, login, password, reputation FROM users
				   """)
	user_info = cursor.fetchall()
	return user_info

# @database_common.connection_hanlder
# def get_user_info(cursor, user_id):
# 	cursor.execute("""
# 					SELECT *
# 					FROM users
# 					INNER JOIN answer
# 					ON (users.user_id = answer.user_id)
# 					INNER JOIN comment
# 					ON (users.user_id = comment.user_id)
# 					INNER JOIN question
# 					ON (users.user_id = question.user_id);
# 					""")
# 	all_user_info = cursor.fetchall()
# 	return all_user_info


@database_common.connection_hanlder
def get_user_by_question(cursor, question_id):
	cursor.execute("""
				   SELECT login
				   FROM users
				   INNER JOIN question
				   ON users.user_id = question.user_id
				   WHERE question.id = %(question_id)s
				   """, {'question_id': question_id})
	question_owner_name = cursor.fetchall()[0]
	return question_owner_name


@database_common.connection_hanlder
def get_login_answer_ID_by_questionID(cursor, question_id):
	cursor.execute("""
				   SELECT login ,answer.id AS answer_id, reputation, answer.user_id
				   FROM users
				   INNER JOIN answer ON users.user_id = answer.user_id AND answer.question_id = %(question_id)s
				   """, {'question_id':question_id})
	answer_owner_name = cursor.fetchall()
	return answer_owner_name


@database_common.connection_hanlder
def get_reputation_points_and_userID_question(cursor, question_id):
	cursor.execute("""
				   SELECT users.reputation AS reputation, users.user_id AS user_id 
				   FROM question
				   INNER JOIN users
				   ON question.user_id = users.user_id AND question.id = %(question_id)s
				   """, {'question_id':question_id})
	reputation_points = cursor.fetchall()
	return reputation_points[0]


@database_common.connection_hanlder
def get_reputation_points_answer(cursor, answer_id):
	cursor.execute("""
				   SELECT users.reputation AS reputation, users.user_id AS user_id
				   FROM answer
				   INNER JOIN users
				   ON answer.user_id = users.user_id AND answer.id = %(answer_id)s
				   """, {'answer_id':answer_id})
	reputation_points = cursor.fetchall()
	return reputation_points[0]



@database_common.connection_hanlder
def change_reputation_points(cursor, new_reputation_points, user_id):
	cursor.execute("""
				   UPDATE users
				   SET reputation = %(reputation)s
				   WHERE user_id = %(user_id)s
				   """, {'user_id':user_id,
						 'reputation':new_reputation_points})


@database_common.connection_hanlder
def find_user_and_password(cursor, login):
	cursor.execute("""
					SELECT login, password
					FROM users
					WHERE login = %(login)s
				   """,
	               {"login": login})
	user = cursor.fetchall()
	return user


@database_common.connection_hanlder
def get_user_id_by_login(cursor, login):
	cursor.execute("""
						SELECT user_id
						FROM users
						WHERE login = %(login)s
					   """,
	               {"login": login})
	user = cursor.fetchall()
	return user[0]['user_id']

@database_common.connection_hanlder
def update_answer_check(cursor, answer_id):
	cursor.execute("""
				   UPDATE answer
				   SET check_answer = 'true'
				   WHERE id = %(answer_id)s
				   """, {'answer_id':answer_id})


@database_common.connection_hanlder
def get_user_details(cursor, user_id):
	cursor.execute("""
					SELECT * FROM users WHERE user_id = %(user_id)s;
					""", {'user_id': user_id})
	user_info = cursor.fetchall()[0]
	return user_info


@database_common.connection_hanlder
def get_user_answers(cursor, user_id):
	cursor.execute("""
					SELECT * FROM users INNER JOIN answer ON (answer.user_id = %(user_id)s)
					WHERE users.user_id = %(user_id)s;
					""", {'user_id': user_id})
	user_answers = cursor.fetchall()
	return user_answers


@database_common.connection_hanlder
def get_user_questions(cursor, user_id):
	cursor.execute("""
					SELECT * FROM users INNER JOIN question ON (question.user_id = %(user_id)s)
					WHERE users.user_id = %(user_id)s;
					""", {'user_id': user_id})
	user_questions = cursor.fetchall()
	return user_questions


@database_common.connection_hanlder
def get_user_comments(cursor, user_id):
	cursor.execute("""
					SELECT * FROM users INNER JOIN comment ON (comment.user_id = %(user_id)s)
					WHERE users.user_id = %(user_id)s;
					""", {'user_id': user_id})
	user_comments = cursor.fetchall()
	return user_comments