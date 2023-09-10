from db_states import *
import json

Session = sessionmaker(bind=engine)
session = Session()

def add_new_user(id):
    if session.query(Users).filter(Users.id == id).one_or_none() == None:
        new_user = Users(id=id, page="start")
        session.add(new_user)
        session.commit()

def get_page(id):
    return session.query(Users).filter(Users.id == id).one().page

def set_page(id, page):
    session.query(Users).filter(Users.id == id).one().page = page
    session.commit()

def get_intention(id):
    return json.loads(session.query(Users).filter(Users.id == id).one().intention)

def set_intention(id, intention):
    session.query(Users).filter(Users.id == id).one().intention = json.dumps(intention, ensure_ascii=False)
    session.commit()

def put_interests(id, interests):
    session.query(Users).filter(Users.id == id).one().interests = json.dumps(interests, ensure_ascii=False)
    session.commit()

def start_pairing(user_id, whishes):
    new_pair = Pairs_Finding(user_id=user_id, whishes=json.dumps(whishes, ensure_ascii=False), declined_users="[]", done=0)
    session.add(new_pair)
    session.flush()
    pair_id = new_pair.id
    session.commit()
    return pair_id

def supple_pairing(search_id, time, place, description):
    user_session = session.query(Pairs_Finding).filter(Pairs_Finding.id == search_id).one()
    user_session.time = time
    user_session.place = place
    user_session.description = description
    session.commit()

def finish_pairing(search_id, user_id, pair_user_id):
    pair_session = session.query(Pairs_Finding).filter(Pairs_Finding.id == search_id).one()
    pair_session.pair_user_id = pair_user_id
    pair_session.done = 1
    session.commit()

def notify_about_pairing(search_id, pair_user_id):
    find_pair_session = session.query(Pairs_Finding).filter(Pairs_Finding.id == search_id).one()
    find_pair_session.pair_user_id = pair_user_id
    session.commit()
    return find_pair_session.user_id
    
def decline_pairing(search_id, user_id, pair_user_id):
    find_pair_session = session.query(Pairs_Finding).filter(Pairs_Finding.id == search_id).one()
    find_pair_session.pair_user_id = None
    declined_users = json.loads(find_pair_session.declined_users)
    declined_users.append(pair_user_id)
    find_pair_session.declined_users = json.dumps(declined_users, ensure_ascii=False)
    session.commit()

def get_finding_pairs():
    return session.query(Pairs_Finding)