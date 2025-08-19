#!/usr/bin/python

import os
import requests
import hashlib
import sys

# ZTP Server URL for retrieving configuration
ZTP_SERVER_URL = "tftp://192.168.4.199"/srv/tftp/initialconfig.cfg"

# EOS Image Server URL for downloading images
EOS_IMAGE_SERVER_URL = "tftp://192.168.4.199"/srv/tftp/images"

# Desired EOS image filename
DESIRED_EOS_IMAGE = "EOS-4.34.2F.swi"

# Known-good checksum for the desired EOS image (replace with the actual value from Arista website)
# For example, using SHA256 (recommended over MD5 for better security)
KNOWN_EOS_CHECKSUM = "2a6d868f979cccb085fe92c7732ab4af vEOS-lab-4.34.2F.swi"  # <<<<<<<<<< IMPORTANT: Replace this

# --- Request Configuration from ZTP Server (as before) ---
try:
    response = requests.get(f"{ZTP_SERVER_URL}")
    response.raise_for_status()
    config_data = response.text
except requests.exceptions.RequestException as e:
    print(f"Error fetching configuration from ZTP server: {e}")
    exit()

# --- Apply Configuration (as before) ---
with open('/mnt/flash/startup-config', 'w') as f:
    f.write(config_data)

# --- Download and Install EOS Image ---
image_download_url = f"{EOS_IMAGE_SERVER_URL}/{DESIRED_EOS_IMAGE}"
image_destination_path = f"/mnt/flash/{DESIRED_EOS_IMAGE}"

print(f"Attempting to download EOS image from: {image_download_url}")

try:
    image_response = requests.get(image_download_url, stream=True)
    image_response.raise_for_status()

    with open(image_destination_path, 'wb') as f:
        for chunk in image_response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Successfully downloaded EOS image to: {image_destination_path}")

    # --- Verify Image Integrity ---
    print("Verifying downloaded EOS image integrity...")
    calculated_checksum = hashlib.sha256()  # Use SHA256 for better security
    with open(image_destination_path, 'rb') as f:
        while chunk := f.read(8192):
            calculated_checksum.update(chunk)

    calculated_checksum_hex = calculated_checksum.hexdigest()

    if calculated_checksum_hex == KNOWN_EOS_CHECKSUM:
        print("EOS image integrity verified successfully.")

        # Install and boot system (only if checksum matches)
        os.system(f"FastCli -p 15 -c 'copy {image_destination_path} flash:'")
        os.system(f"FastCli -p 15 -c 'install image flash:{DESIRED_EOS_IMAGE}'")
        os.system(f"FastCli -p 15 -c 'boot system flash:{DESIRED_EOS_IMAGE}'")
        print("EOS image installation and boot system update commands executed.")
    else:
        print(f"Error: EOS image integrity check failed!")
        print(f"Expected Checksum: {KNOWN_EOS_CHECKSUM}")
        print(f"Calculated Checksum: {calculated_checksum_hex}")
        # Log the error and potentially exit or attempt alternative provisioning
        exit()

except requests.exceptions.RequestException as e:
    print(f"Error downloading or installing EOS image: {e}")
    exit()
except Exception as e:
    print(f"An unexpected error occurred during image processing: {e}")
    exit()

# --- Reload the switch (only after successful image verification and installation) ---
os.system("FastCli -p 15 -c 'reload now'")
