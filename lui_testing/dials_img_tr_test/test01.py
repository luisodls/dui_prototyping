from dials.algorithms.spot_finding.threshold import DispersionThresholdStrategy
from dxtbx.datablock import DataBlockFactory



n_json_file_path = "/tmp/dui_run/dui_files/1_datablock.json"
datablocks = DataBlockFactory.from_json_file(n_json_file_path)
# TODO check length of datablock for safety
datablock = datablocks[0]
my_sweep = datablock.extract_sweeps()[0]

tmp_off = '''
algorithm = DispersionThresholdStrategy(
    kernel_size=params.spotfinder.threshold.dispersion.kernel_size,
    gain=params.spotfinder.threshold.dispersion.gain,
    mask=params.spotfinder.lookup.mask,
    n_sigma_b=params.spotfinder.threshold.dispersion.sigma_background,
    n_sigma_s=params.spotfinder.threshold.dispersion.sigma_strong,
    min_count=params.spotfinder.threshold.dispersion.min_local,
    global_threshold=params.spotfinder.threshold.dispersion.global_threshold,
)

print algorithm(image, mask)
'''
