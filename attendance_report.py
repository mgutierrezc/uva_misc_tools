# 1. Keep email and join time
# 2. Drop duplicates keeping Min join time
# 3. Check who came before 17:05
# 4. Base score on join time
# 5. Export to csv using Gradebook template format

import pandas as pd

def main(attendance_report_path: str, output_path: str, output_name: str):
    # load data
    df = pd.read_csv(attendance_report_path)
    df = df[["User Email", "Join time"]]

    df["Join time"] = pd.to_datetime(df["Join time"])

    # drop duplicates keeping min join time
    df = df.sort_values("Join time").drop_duplicates("email", keep="first")

    # check who came before 17:05
    df["before_1705"] = df["Join time"] < pd.to_datetime("17:05:00")

    # base score on join time
    df["score"] = df["Join time"].apply(lambda x: 1 if x < pd.to_datetime("17:05:00") else 0)

    # export to csv using gradebook template format
    df.to_csv(output_path + "/" + output_name + "csv", index=False)


if __name__ == "__main__":
    main("C:\Users\Gigabyte\Desktop\zoomus_meeting_report_93025893520.csv", "D:\Accesos directos\Trabajo\UVA\Projects\misc_tools", "attendance_report")