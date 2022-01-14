import requests, json, time, math

def getRequest(params, authorizationid):
    headers = {
        'authorization': authorizationid
    }
    r = requests.get(
        f'https://discord.com/api/v9/guilds/{params}', headers=headers)
    return json.loads(r.text)

def getMessageCount(guildid, authorid, authorizationid):
    return int(getRequest(f'{guildid}/messages/search?author_id={authorid}&limit=2', authorizationid)['total_results'])

def retrieveMessageHistory(guildid, authorid, authorizationid):
    jsonn = getRequest(f'{guildid}/messages/search?author_id={authorid}&limit=2', authorizationid)
    message_count = int(jsonn['total_results'])
    pagination_count = math.floor(message_count/25)
    last_page_message_count = 0
    if(message_count%25 > 0):
        pagination_count += 1
        last_page_message_count = message_count%25
    print('Retrieving ' + str(message_count) +' messages... Approx. waiting time = ' + str(pagination_count*5) + ' seconds')
    message_history = []
    i = 0
    while i < pagination_count:
        offset_pagination = i * 25
        paginated_json = getRequest(f'{guildid}/messages/search?author_id={authorid}&offset={offset_pagination}', authorizationid)
        j = 0
        max_messages_on_page = 25
        if(last_page_message_count > 0 and (pagination_count-1) == i): max_messages_on_page = last_page_message_count
        while j < max_messages_on_page:
            message_history.append(paginated_json['messages'][j][0])
            j += 1
        i += 1
        time.sleep(5)
    return message_history

def sendMessage(content, channelId, authorizationId):
    payload = {
        'content': content
    }
    header = {
        'authorization': authorizationId
    }
    r = requests.post(f"https://discord.com/api/v9/channels/{channelId}/messages", data=payload, headers=header)