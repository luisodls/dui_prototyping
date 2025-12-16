from dxtbx.model import ExperimentList


def get_resolution(detector, experiments, x, y, readout=None):
    """
    Determine the resolution of a pixel.
    Arguments are in image pixel coordinates (starting from 1,1).

    this is copy/pasted from Dials Image Viewer
    as a starting point for testing
    """

    #detector = self.raw_image.get_detector()
    #beam = self.raw_image.get_beam()

    beam = experiments.beams()[0]

    if detector is None or beam is None:
        return None

    if readout is None:
        return None

    panel = detector[readout]

    if abs(panel.get_distance()) > 0:
        return panel.get_resolution_at_pixel(beam, (x, y))
    else:
        return None


if __name__ == "__main__":
    # if imported.expt is from a dataset taken at I23
    # it should give a very big resolution result
    experiments_path = "imported.expt"

    experiments = ExperimentList.from_file(experiments_path)
    my_imageset = experiments.imagesets()[0]
    detector = my_imageset.get_detector()

    print("importing from:", experiments_path)

    # this are the coordinates of somewhere very close to the beam center
    # the last 3 parameters are x,y in that panel than panel number
    resolution = get_resolution(
        detector, experiments, 1063.531, 41.597, readout = 12
    )

    print("resolution =", resolution)

