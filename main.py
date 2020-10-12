import powercalc as pc
# import sizecalc as sc
import matplotlib.pyplot as plt
import pandas as pd


def input_data():
    alpha = [0.1, 0.05, 0.01, 0.001]  # уровень значимости
    statsize = 1000  # объём выборки статистик
    mu1 = 0  # мат. ожидание 1-ой последовательности
    mu2 = 0.1  # мат. ожидание 2-ой последовательности
    sigma1 = 1  # среднеквадратичное отклонение 1-ой последовательности
    sigma2 = 1  # среднеквадратичное отклонение 2-ой последовательности
    seqsize = 50000   # объёмы пары выборок
    step = 1000  # шаг
    a1 = 1.04957906144402
    a2 = 0
    coef = 0.5  # beta для обобщенного нормального распределения
    return alpha, statsize, mu1, mu2, sigma1, sigma2, seqsize, step, coef, a1, a2


# Чертёж графика
def draw_plot(mwpowerseq, seq):
    plt.xlabel("Статистическая мощность")
    plt.ylabel("Объём выборки")
    plt.scatter(mwpowerseq, seq, c='blue', label='Power(Mann-Whitney)')
    # plt.plot(mwpowerseq, n, c='navy', label='Size(Mann-Whitney)')
    plt.legend(loc=2)
    plt.grid()
    plt.show()


def write_tests_settings(alpha, seq, mwpowerseq, seq_res, mwpowerseq_res, mu1, mu2, sigma1, sigma2, coef):
    "Данные работы программы в формате csv"
    a = {
        'alpha': alpha,
        'coef': coef,
        'mu1': mu1,
        'mu2': mu2,
        'sigma1': sigma1,
        'sigma2': sigma2,
        'seq': seq,
        'mwpowerseq': mwpowerseq,
    }

    "Данные работы программы в формате csv для мощности больше заданной"
    b = {
        'alpha': alpha,
        'coef': coef,
        'mu1': mu1,
        'mu2': mu2,
        'sigma1': sigma1,
        'sigma2': sigma2,
        'seq': seq_res,
        'mwpowerseq': mwpowerseq_res,
    }
    df = pd.DataFrame.from_dict(b, orient='columns')
    df.to_csv('output_res.csv', mode='a', index=True, header=False, decimal=',', sep=' ', float_format='%.3f')


def main():
    mwpowerseq_res = [[], [], [], []]
    alpha, statsize, mu1, mu2, sigma1, sigma2, seqsize, step, coef, a1, a2 = input_data()
    mwpowerseq, seq = pc.plot_input(alpha, statsize, mu1, mu2, sigma1, sigma2, seqsize, step, coef)
    '''p = sc.calculate_p(coef, mu1, mu2, sigma1, sigma2)
    print(p)'''
    for i in [0, 1, 2, 3]:
        # mwpowerseq_res[i], seq_res = pc.empiric_n(mwpowerseq[i], seq)
        # n = sc.sequence_size(mu1, mu2, sigma1, sigma2, alpha[i], mwpowerseq[i], p[0], a1, a2, coef)
        draw_plot(mwpowerseq[i], seq)
        # write_tests_settings(alpha[i], seq, mwpowerseq[i], seq_res, mwpowerseq_res[i], mu1, mu2, sigma1, sigma2, coef)


if __name__ == "__main__":
    main()
