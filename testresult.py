Accepted,  WRONGANSWER, RUNERR, TIMEOUT, SYSERR, WAIT, UNEVAL = range(1, 8)


class evalResult():
    def __init__(self, rtype: int, info: str = '', time: int = 0, user_result=''):
        self.type = rtype
        self.info = info
        self.time = time
        self.user_result = user_result

    def to_dict(self):
        return {
            'type': NAME_resulttype[self.type],
            'info': self.info,
            'time': self.time,
            'user_result': self.user_result
        }


def get_blank():
    blank = evalResult(UNEVAL)
    return blank


INFO_SYSCON = 'System error! Please contact with website administrators.'

NAME_resulttype = {Accepted: 'Accepted', TIMEOUT: 'Timeout', WRONGANSWER: 'Wrong Answer',
                   RUNERR: 'RUNERR', SYSERR: 'SYSERR', WAIT: 'Wait', None: 'None', UNEVAL: 'Unknown'}
