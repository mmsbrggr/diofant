from .matexpr import MatrixExpr
from ...core import S, I
from ...functions import sqrt, exp


class DFT(MatrixExpr):
    """ Discrete Fourier Transform """

    n = property(lambda self: self.args[0])
    shape = property(lambda self: (self.n, self.n))

    def _entry(self, i, j):
        w = exp(-2*S.Pi*I/self.n)
        return w**(i*j) / sqrt(self.n)

    def _eval_inverse(self):
        return IDFT(self.n)


class IDFT(DFT):
    """ Inverse Discrete Fourier Transform """

    def _entry(self, i, j):
        w = exp(-2*S.Pi*I/self.n)
        return w**(-i*j) / sqrt(self.n)

    def _eval_inverse(self):
        return DFT(self.n)