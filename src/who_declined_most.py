import vk 
import time
#--------------------------------- BEGINNING OF METHOD DEF. PART --------------------------------- 
#Going through all found messages and counting amount of times, that dude declined someone's invitation
def get_declined_score(all_messages, user_ids_names):
    user_leaver_scores = {}
    for name in user_ids_names.keys():
        user_leaver_scores[name]=0

    for message in all_messages:
        if isinstance(message, int): 
                continue 
        for keys in message: 
                if isinstance(keys, str): 
                    continue
                elif isinstance(keys, int):
                    continue

                time.sleep(3)
                print("Name is:{}".format(vk_api.users.get(user_ids=keys['uid'])[0]['first_name']))
                print("Message is:{}".format(keys['body']))
                
                for name in user_ids_names.keys():    
                    if keys['uid'] == user_ids_names[name]:
                        user_leaver_scores[name]+=1

    return user_leaver_scores

#Structuring people names and corresponding scores
def structure_scores(user_leaver_scrs, user_ids_names):
    users_id_score = {}
    for user in user_ids_names.keys():
        users_id_score[user]=user_leaver_scores[user]

    return users_id_score

#Retrieving access token form file in "resources" folder
def get_token_from_file(file_name):
    access_token = ''
    with open(file_name, 'r') as token_file:
        access_token = token_file.read()

    return access_token

#Fetching all "No I'cant go, dude" messages
def get_messages_from_peer(query_list, pid):
    cant_go_messages = []
    for query in query_list:
        cant_go_messages.append(vk_api.messages.search(q=query, peer_id=pid))

    return cant_go_messages

#Fetching group paticipant ids and names 
def get_chat_uids_names(ch_id):
    chat = vk_api.messages.getChat(chat_id=ch_id)
    uids_names = {}
    for uid in chat['users']:
        user_info = vk_api.users.get(user_ids=uid)
        uids_names[user_info[0]['first_name']]=uid

    return uids_names
#--------------------------------- END OF METHOD DEF. PART --------------------------------- 


############################################## BEGINNING OF THE MAIN PROGRAM ##############################################
#Session authorization 
access_tok = get_token_from_file('../resources/a_t.txt')
session = vk.Session(access_token=access_tok)
vk_api=vk.API(session)

user_ids_names = get_chat_uids_names(30)

#Defining a list of search query strings, that neccessery in order to retrieve correct "No I'cant go, dude" messages
search_query_list = ['Сегодня без меня','Не иду', 'не смогу', 'не пойду']

cant_go_messages = get_messages_from_peer(search_query_list, '2000000030')

user_leaver_scores = get_declined_score(cant_go_messages, user_ids_names)

users_id_score = structure_scores(user_leaver_scores, user_ids_names)

print(users_id_score)
############################################## END OF THE MAIN PROGRAM ##############################################