import os

def available_cores() -> int:
    """
    Determine the number of available processor cores.
    There are a number of different methods to get this information, some of
    which may not be available on a specific OS and/or version of Python. So try
    them in order and return the first successful one.
    """

    # https://htcondor.readthedocs.io/en/latest/users-manual/services-for-jobs.html#extra-environment-variables-htcondor-sets-for-jobs
    condor_job_ad = os.environ.get("_CONDOR_JOB_AD")
    if condor_job_ad:
        try:
            classad = dials.util.parse_htcondor_job_classad(pathlib.Path(condor_job_ad))
        except Exception as e:
            logger.error(
                f"Error parsing _CONDOR_JOB_AD {condor_job_ad}: {e}",
                exc_info=True,
            )
        else:
            if classad.cpus_provisioned:
                print("returning classad.cpus_provisioned")
                return classad.cpus_provisioned

    nproc = os.environ.get("NSLOTS", 0)
    try:
        nproc = int(nproc)
        if nproc >= 1:
            print("returning os.environ.get(\"NSLOTS\", 0)")
            return nproc

    except ValueError:
        pass

    try:
        print("returning len(os.sched_getaffinity(0))")
        return len(os.sched_getaffinity(0))
    except AttributeError:
        pass

    try:
        print("returning len(psutil.Process().cpu_affinity())")
        return len(psutil.Process().cpu_affinity())
    except AttributeError:
        pass

    nproc = os.cpu_count()
    if nproc is not None:
        print("returning os.cpu_count")
        return nproc

    nproc = psutil.cpu_count()
    if nproc is not None:
        print("returning psutil.cpu_count()")
        return nproc

    print("returning default 1")
    return 1


if __name__ == "__main__":
    print("available cores =", available_cores())
