"""
MIT License

Street View Image Downloader
Copyright (c) 2025 Jooyoung01 (https://github.com/Jooyoung01/SVI-Collector)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import io
import csv
import argparse
import requests
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def parse_arguments():
    parser = argparse.ArgumentParser(description="📸 Street View Image Downloader")
    parser.add_argument("-k", "--api_key", type=str, required=True, help="🔑 Google API Key")
    parser.add_argument("-csv", "--csv_file_path", type=str, required=True, help="📂 Path to CSV file containing latitude and longitude pairs")
    parser.add_argument("-proj", "--project_area", type=str, required=True, help="🗺️ Project Area Name (e.g., NYC or LA)")
    parser.add_argument("-base", "--base_path", type=str, default='.', help="💾 Base path for saving images and logs")
    parser.add_argument("-s", "--start_row", type=int, default=0, help="🔢 Start row number in the CSV file")
    parser.add_argument("-e", "--end_row", type=int, default=1, help="🔢 End row number in the CSV file")
    parser.add_argument("-v", "--visualize", action="store_true", help="🖼️ Enable visualization of downloaded images")
    return parser.parse_args()

def download_image(url, filename):
    """ 📥 Download an image from a given URL and save it. """
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return Image.open(io.BytesIO(response.content))
    return None

def concatenate_images(img_list):
    """ 🔗 Concatenate images horizontally. """
    total_width = sum(img.width for img in img_list)
    max_height = max(img.height for img in img_list)
    concatenated_img = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for img in img_list:
        concatenated_img.paste(img, (x_offset, 0))
        x_offset += img.width
    return concatenated_img

def log_to_csv(log_file, data):
    """ 📝 Append data to a CSV log file. """
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def show_images_side_by_side(img_list):
    """ 🖼️ Display images in a 2x2 grid. """
    print("🖼️ [INFO] Displaying images side by side...")
    plt.figure(figsize=(10, 10))
    for i, img in enumerate(img_list):
        plt.subplot(2, 2, i + 1)
        plt.imshow(np.array(img))  
        plt.xticks([]), plt.yticks([])
    plt.show(block=True)  

def main():
    args = parse_arguments()

    # 🌍 Setting up configurations
    print("🛠️ [INFO] Setting up configurations...")
    BASE_PATH = args.base_path if args.base_path else f"StreetView_{args.project_area}/data"
    CSV_FILE_PATH = args.csv_file_path
    GOOGLE_API_KEY = args.api_key

    # 🔖 Define paths
    OUTPUT_DIR = os.path.join(BASE_PATH, "street_view_images")
    OUTPUT_CONC_DIR = os.path.join(BASE_PATH, "street_view_concate")
    LOG_FILE_SUCCESS = os.path.join(BASE_PATH, "download_log_add.csv")
    LOG_FILE_FAIL = os.path.join(BASE_PATH, "download_log_fail.csv")

    # 🗂️ Create directories
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_CONC_DIR, exist_ok=True)
    print(f"📂 [INFO] Directories prepared:\n - 📸 Images: {OUTPUT_DIR}\n - 🔗 Concatenated Images: {OUTPUT_CONC_DIR}")

    # 📊 Load CSV file
    print(f"📜 [INFO] Loading CSV file: {CSV_FILE_PATH}")
    df_from_csv = pd.read_csv(CSV_FILE_PATH)

    # ✅ Ensure required columns exist
    if "Latitude" not in df_from_csv.columns or "Longitude" not in df_from_csv.columns:
        raise ValueError("❌ [ERROR] CSV must contain 'Latitude' and 'Longitude' columns.")

    lat_lon_pairs = list(zip(df_from_csv["Latitude"], df_from_csv["Longitude"]))
    print(f"📍 [INFO] Loaded {len(lat_lon_pairs)} location(s) from CSV.")

    # 📍 Process each location
    for num, (lat, lon) in enumerate(lat_lon_pairs[args.start_row:args.end_row + 1], start=args.start_row):
        print(f"📌 [INFO] Processing point {num}: Latitude={lat}, Longitude={lon}")
        img_list, failed_downloads = [], []

        # 📷 Download images from different angles
        HEADINGS = {"left": 270, "front": 0, "right": 90, "back": 180}
        for direction, heading in tqdm(HEADINGS.items(), desc=f"🌍 Point {num}", leave=False):
            print(f"📷 [INFO] Downloading {direction} view image...")
            url = (
                f"https://maps.googleapis.com/maps/api/streetview"
                f"?size=512x512&location={lat},{lon}&fov=90&heading={heading}&pitch=0"
                f"&return_error_code=true&key={GOOGLE_API_KEY}"
            )
            filename = os.path.join(OUTPUT_DIR, f"p{num}_{direction}_{lat}_{lon}.jpg")
            img = download_image(url, filename)
            if img:
                img_list.append(img)
                log_to_csv(LOG_FILE_SUCCESS, [f"p{num}", direction, lat, lon])
                print(f"✅ [SUCCESS] Image saved: {filename}")
            else:
                failed_downloads.append([f"p{num}", direction, lat, lon])
                print(f"❌ [ERROR] Failed to download {direction} view for point {num}.")

        # 📝 Log failed downloads
        for fail in failed_downloads:
            log_to_csv(LOG_FILE_FAIL, fail)

        if not img_list:
            print(f"⚠️ [WARNING] No images downloaded for point {num}. Skipping...")
            continue

        # 🖼️ Show images before concatenation (Only if visualization is enabled)
        if args.visualize:
            show_images_side_by_side(img_list)

        # 🖼️ Concatenate images
        concatenated_img = concatenate_images(img_list)
        if concatenated_img:
            output_image_path = os.path.join(OUTPUT_CONC_DIR, f"p{num}_concate_{lat}_{lon}.jpg")
            concatenated_img.save(output_image_path)
            print(f"🖼️ [SUCCESS] Concatenated image saved: {output_image_path}")

    print("🎉 [INFO] Process completed. Check logs for details.")

if __name__ == "__main__":
    main()
