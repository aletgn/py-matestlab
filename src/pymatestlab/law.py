def hooke(strain, young):
    return young * strain


def hollomon(strain, K, n):
    return K * (strain**n)