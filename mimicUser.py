import discordApi, time, dateutil, re
from random import randrange
import nlpaug.augmenter.word as naw

# Configuration

authorization_id = '' # You authorizationId (Header)
guild_id = '' # Id of the server where the user will be mimicked
author_id = '' # Id of the user that you want to mimic
message_timeout_multiplier = 0.9 # Shorten time between each message by multiplier
max_timeout = 3200 # Max timeout in seconds between each message

skip_to_index = 0 # Skip to index (message nr.)

# Retrieving message history

timestamp_last_msg = None

message_history = discordApi.retrieveMessageHistory(guild_id, author_id, authorization_id)
message_history.reverse()
index = 0

## Loop

for message in message_history:
    # Skip to index
    if(index < skip_to_index):
        print('Skipping Index / '+str(index))
        index += 1
        continue

    type = message['type']
    if (type != 19 and type != 0):
        continue
    channel_id = message['channel_id']
    timestamp = dateutil.parser.parse(message['timestamp'], ignoretz=True)
    content = message['content']
    attachments = message['attachments']
    url_included = False

    if(content == ''):
        if attachments:
            content = message['attachments'][0]['url']
            url_included = True

    # Text augmentation

    # Check if content got URL - if yes skip augmentation otherwise URL will not work
    regex = r'('
    # Scheme (HTTP, HTTPS, FTP and SFTP):
    regex += r'(?:(https?|s?ftp):\/\/)?'
    # www:
    regex += r'(?:www\.)?'
    regex += r')'
    find_urls_in_string = re.compile(regex, re.IGNORECASE)
    url = find_urls_in_string.search(content)
    if url is not None and url.group(0) is not None: url_included = True

    if(url_included == False):
        aug = naw.RandomWordAug(action="swap")
        content = aug.augment(content)
    # Send message

    discordApi.sendMessage(content, channel_id, authorization_id)

    # Timeout until next message
    timeout = 0
    if timestamp_last_msg is None:
        timeout = 0
        timestamp_last_msg = timestamp
    else:
        timeout = (timestamp - timestamp_last_msg).total_seconds() * message_timeout_multiplier
        timestamp_last_msg = timestamp

    if(timeout > max_timeout):
        timeout = 3600 + randrange(100)

    # Add random timeout

    extra_random_timeout = randrange(10)

    total_timeout = timeout+1.5+extra_random_timeout

    print('---------------')
    print('Message = '+content)
    print('Timeout = '+str(total_timeout))
    print('Index = ' + str(index))

    time.sleep(total_timeout)
    index += 1
