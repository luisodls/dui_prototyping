
        from dials.algorithms.spot_finding.threshold import DispersionThresholdStrategy

        self._algorithm = DispersionThresholdStrategy(
            kernel_size=params.spotfinder.threshold.dispersion.kernel_size,
            gain=params.spotfinder.threshold.dispersion.gain,
            mask=params.spotfinder.lookup.mask,
            n_sigma_b=params.spotfinder.threshold.dispersion.sigma_background,
            n_sigma_s=params.spotfinder.threshold.dispersion.sigma_strong,
            min_count=params.spotfinder.threshold.dispersion.min_local,
            global_threshold=params.spotfinder.threshold.dispersion.global_threshold,
        )

        return self._algorithm(image, mask)
