from collection import namedtuple

Rule = namedtuple('Rule', ['regexp', 'conv_func'])


class Converter(object):
    """ Class that convert string given a structure of rules
    """
    def __init__(self, rules):
        self.rules = []
        for pattern, conversion  in rules.iteritems():
            rule = Rule(regexp=re.compile(pattern), )
            self.rules.append() 

    def convert(self, str):
        res = ''

        return res

