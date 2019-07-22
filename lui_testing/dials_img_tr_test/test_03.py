from __future__ import absolute_import, division, print_function


class Test:
    def __init__(self):
        from scitbx.array_family import flex

        # Create an image
        self.image = flex.random_double(2000 * 2000, 10)
        self.image.reshape(flex.grid(2000, 2000))
        self.mask = flex.random_bool(2000 * 2000, 0.99)
        self.mask.reshape(flex.grid(2000, 2000))
        self.gain = flex.random_double(2000 * 2000) + 0.5
        self.gain.reshape(flex.grid(2000, 2000))
        self.size = (3, 3)
        self.min_count = 2


    def test_dispersion_debug(self):
        from dials.algorithms.image.threshold import DispersionThresholdDebug

        nsig_b = 3
        nsig_s = 3

        debug = DispersionThresholdDebug(
            self.image,
            self.mask,
            self.gain,
            self.size,
            nsig_b,
            nsig_s,
            0,
            self.min_count,
        )
        result = debug.final_mask()
        return result


if __name__ == "__main__":
    print("Hi")

    test1 = Test()
    a = test1.test_dispersion_debug()

    np_alg = a.as_numpy_array()

    from matplotlib import pyplot as plt
    plt.imshow( np_alg , interpolation = "nearest" )
    plt.show()
