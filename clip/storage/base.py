import os

class BaseStorage(object):
    values = {}
    filename = os.path.join(os.path.expanduser('~'), '.clip')

    def __init__(self):
        self.bootstrap()

    def bootstrap(self):
        raise NotImplemented

    def save(self):
        raise NotImplemented

    def add(self, list, name, value):
        # Set the value for a given key
        if not self.values.get(list):
            self.values[list] = {}
            value = "Created %s list" % list

        if value and name:
            self.values[list][name] = value

        self.save()
        return [value, ]

    def delete(self, list, name):
        print 'Deleting key'

    def get(self, list, name=None):
        value = []
        if name:
            if self.values.get(list):
                value.append(self.values[list].get(name))
            else:
                self.add(list, None, None)
                return None
        else:
            # Dig down to the deepest level and then bubble upwards
            for k in self.values:
                if list in self.values[k]:
                    value.append(self.values[k][list])

            # If we haven't found anything yet try to grab the entire list
            if len(value) == 0:
                value.append(self.values.get(list))

        return value

    def __unicode__(self):
        return 'Json Storage'
