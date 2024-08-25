# Attendance Report

## Overview
Creates a file ready to be uploaded to Canvas w the Participation/Attendance score for each session.

Input: 

- Zoom attendance report
- Gradebook template for Canvas upload

Output:
- Updated gradebook w attendance scores

The current version updates the latest session found on the Gradebook without Participation scores

## Usage

1. Create a virtual environment using the packages specified on requirements.txt for a python version equal or above the one in runtime.txt
2. Activate the environment
3. Move to the directory with the downloaded tool
4. Create a json called `parameters.json` with all the required paths
```json
{
    "template_path": "path/2024-08-19T2039_Grades-DS_5001-001.csv",
    "attendance_report_path": "path_2/zoomus_meeting_report_93025893520.csv",
    "output_path": "output/path",
    "output_name": "attendance_report"
}
```
5. Run `python attendance_report.py`