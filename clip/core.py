import sys
import os
import re
from clip.storage import JsonStorage
from subprocess import call

regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

storage = JsonStorage()


def get_urls(text):
    words = text.split(' ')
    urls = []
    for word in words:
        if regex.search(word):
            urls.append(word)
    return urls


def get(list, index, default):
    try:
        return list[index]
    except IndexError:
        return default


def execute(command, major, minor):
    copy = False
    value = ""

    if command == "help":
        help()
    elif command == "lists":
        print "Displaying all lists:"
        for k, v in storage.values.items():
            print k
    elif command == "delete":
        value = storage.delete(major, minor)
    elif command == "display":
        value = storage.get(major, minor)
    elif command == "open":
        value = storage.get(major, minor)
        values = []
        for v in value:
            if isinstance(v, dict):
                for k, val in v.items():
                    values.append(get_urls(val))
            else:
                values.append(get_urls(v))
        values = [item for sublist in values for item in sublist]
        print values
        for value in values:
            call(['open', value])
    else:
        if minor:
            value = storage.add(command, major, minor)
        elif major:
            value = storage.get(command, major)
            copy = True
        else:
            value = storage.get(command)

        if len(value) == 1 and not isinstance(value[0], dict):
            copy = True
            value = value[0]
        else:
            for v in value:
                if isinstance(v, dict):
                    for k, v in v.items():
                        print "%s: %s" % (k, v)
                else:
                    print v
            return

    if copy and value:
        outf = os.popen("pbcopy", "w")
        outf.write(value)
        outf.close()

        print "'%s' has been copied to your clipboard" % value
    elif value:
        print value


def help():
    help_text = """
##################################
- clip: help
##################################

clip help                       # Display help information
clip lists                      # Display all list names

clip <list>                     # Create a new list
clip <list>                     # Show items for a list
clip delete <list>              # Delete a list

clip <list> <name> <value>      # Create a new list item
clip <list> <name>              # Copy an item to the clipboard
clip delete <list> <name>       # Deletes an item

clip display <list> <name>      # Display an item without copying it to clipboard
    """

    print help_text
    sys.exit()
