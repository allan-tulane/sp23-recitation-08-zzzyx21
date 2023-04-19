
####### Problem 3 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('elephant', 'relevant'), ('AAAGAATTCA', 'AAATCA')]
alignments = [('book', 'back'), ('kookaburra', 'kookybird-'), ('relev-ant','-elephant'), ('AAAGAATTCA', 'AAA---T-CA')]

def MED(S, T):
    if (S == ""):
        return(len(T))
    elif (T == ""):
        return(len(S))
    else:
        if (S[0] == T[0]):
            return(MED(S[1:], T[1:]))
        else:
            return(1 + min(MED(S, T[1:]), MED(S[1:], T)))


def fast_MED(S, T, MED={}):
    # TODO -  implement memoization
    if (S, T) in MED.keys(): 
        return MED.get((S, T))
    elif (S == ""):
        return(len(T))
    elif (T == ""):
        return(len(S))
    else:
        if (S[0] == T[0]):
            return(fast_MED(S[1:], T[1:]))
        else:
            result = 1 + min(fast_MED(S, T[1:], MED), fast_MED(S[1:], T, MED), fast_MED(S[1:], T[1:], MED))
            MED[(S, T)] = result
            return result
    pass

def fast_align_MED(S, T, MED={}):
    # TODO - keep track of alignment
    if (S, T) in MED:
        return MED[(S, T)][0], MED[(S, T)][1]
    elif (T == ""):
        MED[(S, T)] = (S, "-"*len(S), len(S))
        return S, "-"*len(S)
    elif (S == ""):
        MED[(S,T)] = ("-"*len(T),T, len(T))
        return "-"*len(T),T
    else:
        if (S[0] == T[0]):
            a = fast_align_MED(S[1:], T, MED)
            b = fast_align_MED(S, T[1:], MED)
            c = fast_align_MED(S[1:], T[1:], MED)
            counta = MED[(S[1:], T)][2] + 1
            countb = MED[(S, T[1:])][2] + 1
            countc = MED[(S[1:], T[1:])][2]
            a = (S[0]+a[0], "-"+a[1])
            b = ("-"+b[0], T[0]+b[1])
            c = (S[0]+c[0], T[0]+c[1])

            if countc <= countb and countc <= counta:

                MED[(S, T)] = (c[0], c[1], countc)

            elif countb <= countc and countb <= counta:
                MED[(S, T)] = (b[0], b[1], countb)

            else:
                MED[(S, T)] = (a[0], a[1], counta)

            return MED[(S, T)][0], MED[(S, T)][1]

        else:
            d = fast_align_MED(S[1:], T, MED)
            e = fast_align_MED(S, T[1:], MED)
            f = fast_align_MED(S[1:], T[1:], MED)
            countd = MED[(S[1:], T)][2] + 1
            counte = MED[(S, T[1:])][2] + 1
            countf = MED[(S[1:], T[1:])][2] + 1
            d = (S[0]+d[0], "-" + d[1])
            e = ("-" + e[0], T[0]+e[1])
            f = (S[0] + f[0], T[0] + f[1])
            if countf <= counte and countf <= countd:
                MED[(S, T)] = (f[0], f[1],countf)
            elif counte <= countf and counte <= countd:
                MED[(S, T)] = (e[0], e[1], counte)
            else:
                MED[(S, T)] = (d[0], d[1], countd)
            return MED[(S, T)][0], MED[(S, T)][1]

    pass

def test_MED():
    for S, T in test_cases:
        assert fast_MED(S, T) == MED(S, T)
                                 
def test_align():
    for i in range(len(test_cases)):
        S, T = test_cases[i]
        align_S, align_T = fast_align_MED(S, T)
        assert (align_S == alignments[i][0] and align_T == alignments[i][1])
