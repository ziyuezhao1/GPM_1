"""
Experiment 3.
"""

import pathlib

import numpy as np

import gpm_sync as dqs



def experiment3(dirpath):
    # Parameters
    TEST_NAME = "experiment3"
    ns = [100]
    sigma_rs = np.arange(1, 20+1)
    sigma_ts = np.linspace(0.01, 0.2, 20, endpoint=True)
    ps = [0.05, 0.3]
    qs = [1.0]
    rep_no = 20

    # Messaging parameter
    trial_no = len(ns) * len(sigma_rs) * len(ps) * len(qs) * rep_no;

    # Set up CSV file
    fields = ["n", "sigma_r", "sigma_t", "p", "q", "rep_no", "dq_mean_rerr", "dq_min_rerr", "dq_max_rerr", "dq_mean_terr", "dq_min_terr", "dq_max_terr", "mat_mean_rerr", "mat_min_rerr", "mat_max_rerr", "mat_mean_terr", "mat_min_terr", "mat_max_terr","gpm_mat_mean_rerr","gpm_mat_min_rerr","gpm_mat_max_rerr","gpm_mat_mean_terr","gpm_mat_min_terr","gpm_mat_max_terr"]
    f, dw = dqs.openCSVFile(dirpath, TEST_NAME, fields = fields)

    # Experimental loop
    row = {}
    count = 0
    for n in ns:
        row['n'] = n

        for sigma_r, sigma_t in zip(sigma_rs, sigma_ts):
            row['sigma_r'] = sigma_r
            row['sigma_t'] = sigma_t

            for p in ps:
                row['p'] = p

                for q in qs:
                    row['q'] = q

                    for rep in range(rep_no):
                        row['rep_no'] = rep

                        # Increase the coutner
                        count += 1

                        # Generate ground truth
                        ground_truth = dqs.generateGroundTruth(n)

                        # Run experiment
                        rerr_dqmat, terr_dqmat, rerr_mat, terr_mat ,rerr_gpm_mat, terr_gpm_mat\
                            = dqs.experiment(ground_truth, \
                                       sigma_r=dqs.angle2radians(sigma_r), sigma_t=sigma_t, \
                                       p=p, q=q)

                        # Process data
                        row["dq_mean_rerr"] = np.mean(rerr_dqmat)
                        row["dq_min_rerr"] = np.min(rerr_dqmat)
                        row["dq_max_rerr"] = np.max(rerr_dqmat)
                        row["dq_mean_terr"] = np.mean(terr_dqmat)
                        row["dq_min_terr"] = np.min(terr_dqmat)
                        row["dq_max_terr"] = np.max(terr_dqmat)

                        row["mat_mean_rerr"] = np.mean(rerr_mat)
                        row["mat_min_rerr"] = np.min(rerr_mat)
                        row["mat_max_rerr"] = np.max(rerr_mat)
                        row["mat_mean_terr"] = np.mean(terr_mat)
                        row["mat_min_terr"] = np.min(terr_mat)
                        row["mat_max_terr"] = np.max(terr_mat)
                        
                        row["gpm_mat_mean_rerr"] = np.mean(rerr_gpm_mat)
                        row["gpm_mat_min_rerr"] = np.min(rerr_gpm_mat)
                        row["gpm_mat_max_rerr"] = np.max(rerr_gpm_mat)
                        row["gpm_mat_mean_terr"] = np.mean(terr_gpm_mat)
                        row["gpm_mat_min_terr"] = np.min(terr_gpm_mat)
                        row["gpm_mat_max_terr"] = np.max(terr_gpm_mat)

                        dw.writerow(row)

                        #dqs.logmsg("Trial {:d} of {:d} completed.\n\t\tmean rerr\tmean terr\n\tDQ\t{:.3}\t\t{:.3}\n\tMAT\t{:.3}\t\t{:.3}".format(count, trial_no, row["dq_mean_rerr"], row["dq_mean_terr"], row["mat_mean_rerr"], row["mat_mean_terr"]))
                        dqs.logmsg("Trial {:d} of {:d} completed.\n\t\tmean rerr\tmean terr\n\tDQ\t{:.3}\t\t{:.3}\n\tMAT\t{:.3}\t\t{:.3}\n\tGPM\t{:.3}\t\t{:.3}".format(count, trial_no, row["dq_mean_rerr"], row["dq_mean_terr"], row["mat_mean_rerr"], row["mat_mean_terr"], row["gpm_mat_mean_rerr"], row["gpm_mat_mean_terr"]))

    f.close()


if __name__=="__main__":
    dirpath = pathlib.Path(__file__).parent.resolve()
    print("Writing directory: \t", str(dirpath))
    experiment3(dirpath=str(dirpath))

