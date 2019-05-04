from math import sqrt
import random
import string


def generate_word(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def edit_dist(a, b):
    m = len(b)
    n = len(a)
    dp = [list(range(m)), list(range(m))]
    for i in range(n):
        cur, prev = i & 1, 1 ^ (i & 1)
        dp[cur][0] = dp[prev][0] if a[i] == b[0] else dp[prev][0] + 1
        for j in range(1, m):
            dp[cur][j] = 1 + min([dp[cur][j - 1], dp[prev][j - 1] - (1 if a[i] == b[j] else 0), dp[prev][j]])
    return dp[(n & 1) ^ 1][m - 1]

def get_words_score(a, b, k = 5):
    score = 0.0
    sb = get_word_stats(b, k)
    sa = get_word_stats(a, k)
    for i in range(k):
        mult1 = 0.5 ** i
        for j in range(i, min(k, i + 2)):
            mult2 = 0.5 ** (j - i)
            for p in sa[i].keys():
                if p in sb[j]:
                    cnt = min(sa[i][p], sb[j][p])
                    score += cnt * mult1 * mult2
                    sa[i][p] -= cnt
                    sb[j][p] -= cnt
            for p in sb[i].keys():
                if p in sa[j]:
                    cnt = min(sb[i][p], sa[j][p])
                    score += cnt * mult1 * mult2
                    sb[i][p] -= cnt
                    sa[j][p] -= cnt
    return score


def get_word_stats(word, k=4):
    res = [{} for _ in range(k)]
    for i in range(len(word)):
        for j in range(i + 1, min(len(word), i + 1 + k)):
            res[j - i - 1][word[i] + word[j]] = res[j - i - 1].get(word[i] + word[j], 0) + 1
    return res


def similarity_1223(a, b):
    return get_words_score(a, b) / (max(get_words_score(a, a), get_words_score(b, b)))



def similarity_1(a, b):
    return 1 - edit_dist(a, b) / max(len(a), len(b))


if __name__ == '__main__':
    words = open('words.txt').read().split()[:2001]
    w1 = 'salingeralejandro'
    w2 = 'alejandrosalinger'
    print(similarity_1223(w1, w2))
    print(similarity_1(w1, w2))
    for w1 in words:
        for w2 in words:
            if w1 < w2 and len(w1) > 2 and len(w2) > 2:
                a = similarity_1(w1, w2)
                b = similarity_2(w1, w2)
                if abs(a - b) > 0.1 and (a > 0.3 and b > 0.3) and a < b:
                    print('{} ~ {}  edit: {} my: {}'.format(w1, w2, a, b))
