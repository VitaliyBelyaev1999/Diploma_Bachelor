from scipy import integrate
from scipy.stats import gennorm, norm
from scipy.special import gamma
from numpy import inf, sqrt


def calculate_p(coef, mu1, mu2, sigma1, sigma2):
    return integrate.quad(func, -inf, inf, args=(coef, mu1, mu2, sigma1, sigma2))


def func(x, coef, mu1, mu2, sigma1, sigma2):
    F1 = gennorm.cdf(x, coef, loc=mu1, scale=sigma1)
    f2 = gennorm.pdf(x, coef, loc=mu2, scale=sigma2)
    print("F1 = ", F1)
    print("f2 = ", f2)
    return F1 * f2


def sequence_size(coef, mu1, mu2, sigma1, sigma2, alpha, mwpowerseq, p, a1, a2):
    n = []
    mwfunc = []
    # n = mwfunc1(coef, mu1, mu2, sigma1, sigma2, mwpowerseq, mwfunc,a1, a2, n, alpha)
    # n = mwfunc2(mwpowerseq, mwfunc, p, a1, a2, n, alpha)
    # n = mwfunc3(coef, mu1, mu2, sigma1, sigma2, mwpowerseq, mwfunc,p, a1, a2, n, alpha)
    return n


def mwfunc1(coef, mu1, mu2, sigma2, mwpowerseq, mwfunc, a1, a2, n, alpha):
    quantile = norm.ppf(1 - alpha/2)
    bquantile_mw = []
    d = (mu2 - mu1) / (sqrt(gamma(3/coef) / gamma(1/coef)) / sigma2)
    for i in range(len(mwpowerseq)):
        bquantile_mw.append(norm.ppf(1 - mwpowerseq[i]))
        mwfunc.append(2 * ((quantile + bquantile_mw[i]) ** 2) / (d ** 2))
        n.append(a1 * mwfunc[i] + a2)
    return n


def mwfunc2(mwpowerseq, mwfunc, p, a1, a2, n, alpha):
    quantile = norm.ppf(1 - alpha)
    bquantile_mw = []
    for i in range(len(mwpowerseq)):
        bquantile_mw.append(norm.ppf(mwpowerseq[i]))
        mwfunc.append(((quantile + bquantile_mw[i]) ** 2) / (3 * (p - 1/2) ** 2))
        n.append(a1 * mwfunc[i] + a2)
    return n


def mwfunc3(coef, mu1, mu2, sigma1, sigma2, mwpowerseq, mwfunc, p, a1, a2, n, alpha):
    quantile = norm.ppf(1 - alpha/2)
    bquantile_mw = []
    sigmaI, sigmaI1, sigmaI2 = sigma_integrals(coef, p, mu1, mu2, sigma1, sigma2)
    sigma_0 = sqrt(4 * sigmaI)
    sigma_n = sqrt(2 * (sigmaI1 ** 2 + sigmaI2 ** 2))
    for i in range(len(mwpowerseq)):
        bquantile_mw.append(norm.ppf(1 - mwpowerseq[i]))
        mwfunc.append(2 * ((sigma_0 * quantile + sigma_n * bquantile_mw[i]) ** 2) / ((p - 1 / 2) ** 2))
        n.append(a1 * mwfunc[i] + a2)
    return n


def sigma_integrals(coef, p, mu1, mu2, sigma1, sigma2):
    sigma = integrate.quad(func_sigma, -inf, inf, args=(coef, mu1, sigma1))
    sigma_1 = integrate.quad(func_sigma1, -inf, inf, args=(coef, mu1, mu2, sigma1, sigma2))
    sigma_2 = integrate.quad(func_sigma2, -inf, inf, args=(coef, mu1, mu2, sigma1, sigma2))
    return sigma[0] - 0.25, sigma_1[0] - (1 - p) ** 2, sigma_2[0] - p ** 2


def func_sigma(x, coef, mu1, sigma1):
    F1 = gennorm.cdf(x, coef, loc=mu1, scale=sigma1)
    f1 = gennorm.pdf(x, coef, loc=mu1, scale=sigma1)
    return F1 * F1 * f1


def func_sigma1(x, coef, mu1, mu2, sigma1, sigma2):
    F2 = gennorm.cdf(x, coef, loc=mu2, scale=sigma2)
    f1 = gennorm.pdf(x, coef, loc=mu1, scale=sigma1)
    return F2 * F2 * f1


def func_sigma2(x, coef, mu1, mu2, sigma1, sigma2):
    F1 = gennorm.cdf(x, coef, loc=mu1, scale=sigma1)
    f2 = gennorm.pdf(x, coef, loc=mu2, scale=sigma2)
    return F1 * F1 * f2
