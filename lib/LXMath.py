def powerCalculator(w='', v='', a=''):

    result = 0.0
    solvedFor = ''
    
    if w == '':
        result = float(v) * float(a)
        solvedFor = 'w'
    elif v == '':
        result = float(w) / float(a)
        solvedFor = 'v'
    elif a == '':
        result = float(w) / float(v)
        solvedFor = 'a'

    return result, solvedFor