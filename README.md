# SVI-Collector
A Python tool for downloading and visualizing **Google Street View images** based on latitude and longitude coordinates.
> 📢 **Notice:** Please refer to `SVI_Collector.ipynb` for sample usage and implementation details. 🚀

## 📌 Step 1: Install Dependencies

### Install using `requirements.txt`
Run the following command to install all required dependencies:

```bash
pip install -r requirements.txt
```

```bash
pandas
matplotlib
numpy
Pillow
tqdm
requests
```

## 📌 Step 2: Run the Script
```bash
python streetView_collector.py -k "YOUR_Google_API_KEY" -csv "YOUR_CSV_FILE_LOCATION" -proj "YOUR_PROJECT_NAME"
```
Example
```bash
python streetView_collector.py -k AIzaSyEXAM_PLE -csv locations.csv -proj NYC
```
### 🖥️ Alternative: Run in Jupyter Notebook
```bash
!git clone https://github.com/Jooyoung01/SVI-Collector.git
%cd SVI-Collector
!python script.py -k [YOUR_API_KEY] -csv [CSV FILE LOCATION] -proj [YOUR PROJECT NAME]
```

## 📌 CSV File Format for SVI-Collector
For this project (SVI-Collector), the CSV file must contain latitude and longitude coordinates in the WGS 84 (EPSG:4326) coordinate reference system.
### ✅ CSV File Format (Required Columns)
Your CSV file should contain two columns:
Latitude (float)
Longitude (float)

📍 Example (*locations.csv*)
```bash
Longitude,Latitude
-73.98,40.69
-118.25,34.05
-0.1276,51.5074
139.6917,35.6895
```
✅ CRS: WGS 84 (EPSG:4326)
✅ Units: Degrees (°)

### 📌 Key Points
- Ensure column headers are `Longitude,Latitude` (not swapped). <br>
- Values must be in **decimal degrees (°)**, not projected coordinates. <br>
- Do not include additional columns unless explicitly required. <br>
- Use a **comma (`,`) as the delimiter** (not spaces or semicolons).