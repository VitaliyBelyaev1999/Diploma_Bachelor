from statsmodels.distributions.empirical_distribution import ECDF
from scipy.stats import gennorm, norm, mannwhitneyu


# Генерация случайного распределения с заданными мат.ожиданием, среднеквадратичным отклонением, объёмом
def make_sequence(mu, sigma, size1, coef):
    seq = gennorm.rvs(coef, loc=mu, scale=sigma, size=size1)
    return seq


# Проверка гипотезы по критерию Манна-Уитни
def mannwhitney_test(seq1, seq2, seqsize):
    u, p = mannwhitneyu(seq1, seq2, alternative='two-sided')  # Значение статистики и анр
    stat = (u - seqsize * seqsize / 2) / ((seqsize * seqsize * (seqsize + seqsize + 1) / 12) ** 0.5)
    return stat


# Вычисление статистик
def mw_statistic(statsize, mu1, mu2, sigma1, sigma2, seqsize, coef):
    mwstat = []
    seq1 = []
    seq2 = []
    for i in range(statsize):
        seq1.append(make_sequence(mu1, sigma1, seqsize, coef))  # 1-ая последовательность случайных значений
        seq2.append(make_sequence(mu2, sigma2, seqsize, coef))  # 2-ая последовательность случайных значений
        mwstat.append(mannwhitney_test(seq1[i], seq2[i], seqsize))  # заполнение mwstat значениями статистики
    return mwstat


# Вычисление статистической мощности
def stat_power(stat, alpha):
    ecdf = ECDF(stat)
    quantile1 = norm.ppf(alpha / 2)
    quantile2 = norm.ppf(1 - alpha / 2)
    beta = ecdf([quantile2]) - ecdf([quantile1])
    power = 1 - beta
    power = float(power)
    return power


# Статистическая мощность (Yongqiang Tang)
def stat_power_tang(stat, alpha, seqsize, sigma1, sigma2):
    ecdf = ECDF(stat)
    quantile = norm.ppf(1 - alpha / 2)
    arg1 = (seqsize ** (1/2) * (teta - 0.5) - quantile * sigma1) / sigma2
    arg2 = (seqsize ** (1/2) * (0.5 - teta) - quantile * sigma1) / sigma2
    power = ecdf(arg1) + ecdf(arg2)
    power = float(power)
    return power


# Расчёт значений для графика
def plot_input(alpha, statsize, mu1, mu2, sigma1, sigma2, seqsize, step, coef):
    count = step
    mwpowerseq = [[], [], [], []]
    seq = []
    while count <= seqsize:
        mwstat = mw_statistic(statsize, mu1, mu2, sigma1, sigma2, count, coef)
        for i in [0, 1, 2, 3]:
            mwpower = stat_power(mwstat, alpha[i])
            mwpowerseq[i].append(mwpower)
            mwpowertang = stat_power_tang(mwstat, alpha[i], seqsize, sigma1, sigma2)
            mwpowerseqtang[i].append(mwpowertang)
        seq.append(count)
        count = count + step
    return mwpowerseq, seq


def empiric_n(mwpowerseq, seq):
    mwpowerseq_res = []
    seq_res = []
    list.sort(mwpowerseq)
    for i in range(len(mwpowerseq)):
        if 0.85 <= mwpowerseq[i] < 1.0:
            mwpowerseq_res.append(mwpowerseq[i])
            seq_res.append(seq[i])
    return mwpowerseq_res, seq_res
