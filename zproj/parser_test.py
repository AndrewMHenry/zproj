import collections

Reader = collections.namedtuple('Reader', 'head tail')

def create_reader(tokens):
    return Reader(head=None, tail=iter(tokens))


def expect_token(reader, kind):
    pass
 



def get_token(head, tail):
    next(tail)
    return head

def expect_token(head, tail, kind):
    if True:
        pass
