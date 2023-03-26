import sqlparse
from sqlparse.tokens import Whitespace, Punctuation, Name


def extract_tables(sql: str):
    if sql.strip().startswith("create"):
        return ()
    tokens = list(sqlparse.lexer.tokenize(sql))
    tables = set()
    for i in range(len(tokens)):
        if tokens[i][0] == sqlparse.tokens.Keyword:
            if tokens[i][1] == 'from' or 'join' in tokens[i][1] or tokens[i][1] == "table":
                j = i+1
                while j < len(tokens):
                    t = tokens[j]
                    j += 1
                    if t[0] in [Whitespace, Punctuation]:
                        continue
                    elif t[0] == Name:
                        tables.add(t[1])
                        while j < len(tokens) and tokens[j][0] == Whitespace:
                            j += 1
                        if j < len(tokens) and tokens[j][0] == Name:
                            j += 1
                    else:
                        break
    return tables


if __name__ == '__main__':
    sql = '''
    create table test_null(a int);
    '''
#      sql = '''
#      select *
#  from tc left join sc on tc.cno = sc.cno
#  where sc.cno is null '''
    tables = extract_tables(sql)
    print(tables)
