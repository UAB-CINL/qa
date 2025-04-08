import argparse
import nibabel as nib
import nilearn as nil
import scipy.ndimage as ndi
from scipy.fft import fft, fftfreq
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.dates as mdates
import numpy as np
import os
import glob
import re
from datetime import datetime

# Initialize the parser
parser = argparse.ArgumentParser(description="Process some input parameters.")

# Add arguments
parser.add_argument("bids_dir", type=str, help="Path to the input files")  # Required positional argument

# Parse the arguments
args = parser.parse_args()

# load proxy images from each session
subject_dir = os.path.abspath(os.path.join(args.bids_dir, 'sub-fbirn'))

mean_signal_values = np.zeros(len(os.listdir(subject_dir)))
sfnr_values = np.zeros(len(os.listdir(subject_dir)))
ssnvar_values = np.zeros(len(os.listdir(subject_dir)))
snr_values = np.zeros(len(os.listdir(subject_dir)))
percent_drift_values = np.zeros(len(os.listdir(subject_dir)))
percent_fluctuation_values = np.zeros(len(os.listdir(subject_dir)))

dates = []

for index, session_dir in enumerate(glob.glob(os.path.join(subject_dir, 'ses-Qa*'))):
    nii_file = glob.glob(os.path.join(subject_dir, session_dir, 'func', '*.nii.gz'))
    fates = nib.load(nii_file[0])

    # get the date string from the session directory
    match = re.search(r'\d{8}', nii_file[0])
    if match:
        date_str = match.group()
        try:
            dates.append(datetime.strptime(date_str, '%m%d%Y'))
        except ValueError:
            print("The date format is not correct, trying another order.")
            try:
                dates.append(datetime.strptime(date_str, '%Y%m%d'))
            except ValueError:
                print("The date format is not correct.")

    else:
        print("No 8-digit date string found.")

    # request array data from proxy images
    fates_data = fates.get_fdata()

    # get the size of each dimension in the data array
    x_dim, y_dim, z_dim, t_dim = fates_data.shape

    # region of interest
    roi_x, roi_y, roi_z = 49, 63, 23
    roi_size = 20
    half_size = roi_size // 2

    # coordinate of center slice is roi_z

    # define the bounds of the region of interest and ensure they stay within the image bounds
    x_min = max(roi_x - half_size, 0)
    x_max = min(roi_x + half_size, x_dim - 1)
    y_min = max(roi_y - half_size, 0)
    y_max = min(roi_y + half_size, y_dim - 1)
    # z_min = max(roi_z - half_size, 0)
    # z_max = min(roi_z + half_size, z_dim - 1)

    # ------- MEAN SIGNAL -------
    # calculate signal image (simple average)
    # take center slice only
    signal_img = np.mean(fates_data[:,:,roi_z,:], axis=2)
    # signal summary value
    mean_signal_values[index] = np.mean(signal_img[x_min:x_max, y_min:y_max])

    # ------- FLUCTUATION NOISE -------
    # calculate temporal fluctuation noise image
    # center slice only
    # Initialize an array to store the standard deviation of residuals
    fluctuation_noise_img = np.zeros((x_dim, y_dim))

    # Loop through each voxel
    for i in range(x_dim):
        for j in range(y_dim):
            # Extract the time-series for the current voxel
            time_series = fates_data[i, j, roi_z, :]

            # Fit a second-order polynomial
            time_points = np.arange(t_dim)
            coefficients = np.polyfit(time_points, time_series, 2)
            polynomial = np.poly1d(coefficients)

            # Calculate the residuals (original - fitted)
            fitted_values = polynomial(time_points)
            residuals = time_series - fitted_values

            # Calculate the standard deviation of the residuals
            fluctuation_noise_img[i, j] = np.std(residuals)

    # SIGNAL-TO-FLUCTUATION-NOISE RATIO (SFNR) IMAGE
    # voxelwise division of signal and temporal fluctuation noise image
    sfnr_img = signal_img / fluctuation_noise_img
    # summary SFNR value from ROI
    sfnr_values[index] = np.mean(sfnr_img[x_min:x_max, y_min:y_max])

    # STATIC SPATIAL NOISE IMAGE
    sumEven_img = np.sum(fates_data[:, :, roi_z, 0:2:t_dim], axis=2)
    sumOdd_img = np.sum(fates_data[:, :, roi_z, 1:2:t_dim], axis=2)
    diff_img = sumOdd_img - sumEven_img
    # static spatial noise variance summary value
    ssnvar_values[index] = np.var(diff_img[x_min:x_max, y_min:y_max])

    snr_values[index] = mean_signal_values[index] / np.sqrt(ssnvar_values[index])

    # --- DETRENDING ---
    # initialize array to store average roi values
    averages = np.zeros(fates_data.shape[3])

    # compute average of each time point
    for t in range(fates_data.shape[3]):
        region = fates_data[x_min:x_max+1, y_min:y_max+1, roi_z, t]
        averages[t] = np.mean(region)

    # mean signal intensity
    signal_intensity = np.mean(averages)

    # fit polynomal for detrending
    time_points = np.arange(len(averages))
    degree = 2
    coefficients = np.polyfit(time_points, averages, degree)
    p = np.poly1d(coefficients)

    # evaluate polynomial over time range
    t_fit = np.linspace(time_points.min(), time_points.max(), 160)
    y_fit = p(t_fit)

    # calculate residuals (detrended data)
    residuals = averages - y_fit

    # ------- PERCENT DRIFT -------
    percent_drift_values[index] = (max(y_fit) - min(y_fit)) / signal_intensity * 100
    
    # ------- PERCENT FLUCTUATION -------
    percent_fluctuation_values[index] = 100 * np.std(residuals) / signal_intensity


print("Mean signal:", mean_signal_values)
# grand mean
signal_mean = np.mean(mean_signal_values)
# standard deviation (sample)
signal_std = np.std(mean_signal_values, ddof=1)
# upper control limit
signal_UCL = signal_mean + 3 * signal_std
# lower control limit
signal_LCL = signal_mean - 3 * signal_std

print("SFNR:", sfnr_values)
# grand mean
sfnr_mean = np.mean(sfnr_values)
# standard deviation (sample)
sfnr_std = np.std(sfnr_values, ddof=1)
# upper control limit
sfnr_UCL = sfnr_mean + 3 * sfnr_std
# lower control limit
sfnr_LCL = sfnr_mean - 3 * sfnr_std

print("SSNV:", ssnvar_values)
# grand mean
ssnvar_mean = np.mean(ssnvar_values)
# standard deviation (sample)
ssnvar_std = np.std(ssnvar_values, ddof=1)
# upper control limit
ssnvar_UCL = ssnvar_mean + 3 * ssnvar_std
# lower control limit
ssnvar_LCL = ssnvar_mean - 3 * ssnvar_std

print("SNR:", snr_values)
# grand mean
snr_mean = np.mean(snr_values)
# standard deviation (sample)
snr_std = np.std(snr_values, ddof=1)
# upper control limit
snr_UCL = snr_mean + 3 * snr_std
# lower control limit
snr_LCL = snr_mean - 3 * snr_std

print("Percent drift:", percent_drift_values)
# grand mean
percent_drift_mean = np.mean(percent_drift_values)
# standard deviation (sample)
percent_drift_std = np.std(percent_drift_values, ddof=1)
# upper control limit
percent_drift_UCL = percent_drift_mean + 3 * percent_drift_std
# lower control limit
percent_drift_LCL = percent_drift_mean - 3 * percent_drift_std

print("Percent fluctuation:", percent_fluctuation_values)
# grand mean
percent_fluctuation_mean = np.mean(percent_fluctuation_values)
# standard deviation (sample)
percent_fluctuation_std = np.std(percent_fluctuation_values, ddof=1)
# upper control limit
percent_fluctuation_UCL = percent_fluctuation_mean + 3 * percent_fluctuation_std
# lower control limit
percent_fluctuation_LCL = percent_fluctuation_mean - 3 * percent_fluctuation_std

print("Dates:", dates)

combined = list(zip(dates, mean_signal_values, sfnr_values, ssnvar_values, snr_values, percent_drift_values, percent_fluctuation_values))
combined.sort()
sorted_dates, sorted_mean_signal_values, sorted_sfnr_values, sorted_ssnvar_values, sorted_snr_values, sorted_percent_drift_values, sorted_percent_fluctuation_values = zip(*combined)
print(sorted_dates)
print(sorted_mean_signal_values)

# output lists to text file
formatted_dates = np.array([dt.strftime("%Y/%m/%d") for dt in sorted_dates])
sorted_data = np.column_stack([formatted_dates, sorted_mean_signal_values, sorted_sfnr_values, sorted_ssnvar_values, sorted_snr_values, sorted_percent_drift_values, sorted_percent_fluctuation_values])
# define header
header = "Date,MeanSignal,SFNR,SSNV,SNR,PercDrift,PercFluct"

np.savetxt("output.txt", sorted_data, fmt="%s", delimiter=",", header=header)

print("Lists saved as columns in output.txt")

fig, axs = plt.subplots(3, 2, sharex=True)
axs[0,0].plot(sorted_dates, sorted_mean_signal_values, marker='o')
axs[0,0].set_title("Mean Signal", fontsize=18)
axs[0,0].axhline(signal_mean, color='g', linestyle='--', label=f'Center Line (Mean={signal_mean:.2f})', linewidth=1)
axs[0,0].axhline(signal_UCL, color='r', linestyle='--', label=f'UCL ({signal_UCL:.2f})', linewidth=1)
axs[0,0].axhline(signal_LCL, color='r', linestyle='--', label=f'LCL ({signal_LCL:.2f})', linewidth=1)


axs[0,1].plot(sorted_dates, sorted_sfnr_values, marker='o')
axs[0,1].set_title("Signal-to-Fluctuation Noise Ratio", fontsize=18)
axs[0,1].axhline(sfnr_mean, color='g', linestyle='--', label=f'Center Line (Mean={sfnr_mean:.2f})', linewidth=1)
axs[0,1].axhline(sfnr_UCL, color='r', linestyle='--', label=f'UCL ({sfnr_UCL:.2f})', linewidth=1)
axs[0,1].axhline(sfnr_LCL, color='r', linestyle='--', label=f'LCL ({sfnr_LCL:.2f})', linewidth=1)


axs[1,0].plot(sorted_dates, sorted_ssnvar_values, marker='o')
axs[1,0].set_title("Static Spatial Noise Variance", fontsize=18)
axs[1,0].axhline(ssnvar_mean, color='g', linestyle='--', label=f'Center Line (Mean={ssnvar_mean:.2f})', linewidth=1)
axs[1,0].axhline(ssnvar_UCL, color='r', linestyle='--', label=f'UCL ({ssnvar_UCL:.2f})', linewidth=1)
axs[1,0].axhline(ssnvar_LCL, color='r', linestyle='--', label=f'LCL ({ssnvar_LCL:.2f})', linewidth=1)


axs[1,1].plot(sorted_dates, sorted_snr_values, marker='o')
axs[1,1].set_title("Signal-to-Noise Ratio", fontsize=18)
axs[1,1].axhline(snr_mean, color='g', linestyle='--', label=f'Center Line (Mean={snr_mean:.2f})', linewidth=1)
axs[1,1].axhline(snr_UCL, color='r', linestyle='--', label=f'UCL ({snr_UCL:.2f})', linewidth=1)
axs[1,1].axhline(snr_LCL, color='r', linestyle='--', label=f'LCL ({snr_LCL:.2f})', linewidth=1)


axs[2,0].plot(sorted_dates, sorted_percent_drift_values, marker='o')
axs[2,0].set_title("Percent Drift", fontsize=18)
axs[2,0].axhline(percent_drift_mean, color='g', linestyle='--', label=f'Center Line (Mean={percent_drift_mean:.2f})', linewidth=1)
axs[2,0].axhline(percent_drift_UCL, color='r', linestyle='--', label=f'UCL ({percent_drift_UCL:.2f})', linewidth=1)
axs[2,0].axhline(percent_drift_LCL, color='r', linestyle='--', label=f'LCL ({percent_drift_LCL:.2f})', linewidth=1)


axs[2,1].plot(sorted_dates, sorted_percent_fluctuation_values, marker='o')
axs[2,1].set_title("Percent Fluctuation", fontsize=18)
axs[2,1].axhline(percent_fluctuation_mean, color='g', linestyle='--', label=f'Center Line (Mean={percent_fluctuation_mean:.2f})', linewidth=1)
axs[2,1].axhline(percent_fluctuation_UCL, color='r', linestyle='--', label=f'UCL ({percent_fluctuation_UCL:.2f})', linewidth=1)
axs[2,1].axhline(percent_fluctuation_LCL, color='r', linestyle='--', label=f'LCL ({percent_fluctuation_LCL:.2f})', linewidth=1)

for ax in axs.flat:
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Value', fontsize=14)
    ax.legend(fontsize=12)
    ax.tick_params(axis='both', labelsize=14)

plt.gcf().autofmt_xdate()
plt.show()