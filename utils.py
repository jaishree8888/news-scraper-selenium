import re

def validate_topic(topic):
    if not topic or topic.strip() == "":
        return False, "Topic cannot be empty"

    topic = topic.strip()

    if len(topic) > 50:
        return False, "Topic too long"

    if len(topic.split()) > 5:
        return False, "Too many keywords"

    if not re.match("^[a-zA-Z0-9 ]+$", topic):
        return False, "Invalid characters in topic"

    return True, "Valid"