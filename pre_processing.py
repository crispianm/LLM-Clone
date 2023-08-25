import json
import os

def import_json_files(folder_path):
  """Imports all JSON files in a folder and its subfolders that begin with the word message.

  Args:
    folder_path: The path to the folder.

  Returns:
    A list of dictionaries, where each dictionary represents an object in the JSON file.
  """

  json_objects = []

  for root, directories, files in os.walk(folder_path):
    for file in files:
      if file.startswith("message") and file.endswith(".json"):
        with open(os.path.join(root, file), "r") as f:
          json_data = f.read()

          json_objects.append(json.loads(json_data))

  return json_objects


def parse_threads(threads):

  '''
  Parse the threads, and return a list of dictionaries, where each dictionary represents a message.

  Args:
    threads: A list of dictionaries, where each dictionary represents a thread.

  Returns:
    A list of dictionaries, where each dictionary represents a message.
  
  '''

  messages_array = []

  for thread in threads:

    thread_info = {
      'thread_title': thread['title'],
      'is_still_participant': thread['is_still_participant'],
      'thread_path': thread['thread_path'],
      'magic_words': thread['magic_words'],
    }

    try:
      thread_info['nb_participants'] = len(thread['participants'])
    except:
      thread_info['nb_participants'] = 0

    thread_messages = thread['messages']
    for message in thread_messages:

      message_info = {
        'sender_name': message['sender_name'],
        'timestamp': message.get('timestamp') or (message.get('timestamp_ms') / 1000),
        # 'type': message['type'],
      }

      # Isolate media type
      if message.get('photos') != None:
        message_info['media'] = "Photo"
      elif message.get('videos') != None:
          message_info['media'] = "Video"
      elif message.get('files') != None:
          message_info['media'] = "File"
      else:
          message_info['media'] = "None"

      # Isolate message content
      try:
          message_info['message'] = message['content']
      except:
          message_info['message'] = ""

      try:
          message_info['length'] = len(message['content'])
      except:
          message_info['length'] = 0

      messages_array.append({**message_info, **thread_info})

  return messages_array


if __name__ == "__main__":

  folder_path = "../data/messages2"

  json_objects = import_json_files(folder_path)
  messages_array = parse_threads(json_objects)
