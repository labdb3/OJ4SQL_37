import copy
import decimal
import json

INFO_COLS = '#columns not match'


def judge(user_result, stand_result, judge_type, judge_kwargs, sql_type):
    '''
    TODO: 无序评测有问题,改成多重集合形式
    '''
    udata = user_result['data']
    sdata = stand_result['data']
    # 行数不相等
    if len(udata) != len(sdata):
        return False, ''
    # 列数不相等
    if len(udata) > 0 and len(udata[0]) != len(sdata[0]):
        return False, INFO_COLS
    if judge_type == 'OD':
        return udata == sdata, ''
    elif judge_type == 'UD':
        return set(udata) == set(sdata), ''
    # judge_kwargs: decimal_cols:[int,], decimal_prec:int or [int]
    judge_kwargs = json.loads(judge_kwargs)
    round_cols = judge_kwargs['round_cols']
    round_prec = judge_kwargs['round_prec']
    if isinstance(round_prec, int):
        round_prec = [round_prec]*len(round_cols)
    round_prec_decimal = [0]*len(round_cols)
    for i, p in enumerate(round_prec):
        if p <= 0:
            p = '1'
        else:
            p = '0.'+'0'*(p-1)+'1'
        round_prec_decimal[i] = decimal.Decimal(p)

    udata = copy.deepcopy(udata)
    sdata = copy.deepcopy(sdata)
    try:
        sdata = [tuple((cell.quantize(round_prec_decimal[round_cols.index(ci)]) if ci in round_cols and isinstance(cell, decimal.Decimal) else
                        round(cell, round_prec[round_cols.index(ci)]) if ci in round_cols and isinstance(cell, float) else
                        cell for ci, cell in enumerate(row)))for row in sdata]
        udata = [tuple((cell.quantize(round_prec_decimal[round_cols.index(ci)]) if ci in round_cols and isinstance(cell, decimal.Decimal) else
                        round(cell, round_prec[round_cols.index(ci)]) if ci in round_cols and isinstance(cell, float) else
                        cell for ci, cell in enumerate(row)))for row in udata]
        if judge_type == 'OQ':
            return udata == sdata, ''
        elif judge_type == 'UQ':
            return set(udata) == set(sdata), ''
    except Exception as e:
        print(e)
        e.with_traceback()
        return False, ''
