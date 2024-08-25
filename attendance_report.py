# 1. Keep email and join time
# 2. Drop duplicates keeping Min join time
# 3. Check who came before 17:05
# 4. Base score on join time
# 5. Export to csv using Gradebook template format

import pandas as pd

def gen_attendance_report(attendance_report_path: str, output_path: str, output_name: str):
    """
    Generates attendance scores from a Zoom meeting report
    """

    # load data
    df = pd.read_csv(attendance_report_path)
    df = df[["User Name", "User Email", "Join time"]]

    df["Join time"] = pd.to_datetime(df["Join time"])

    # check who came before 17:05
    df["Join time"] = df["Join time"].apply(lambda x: x.time())
    df["day_month_year"] = df["Join time"].dt.date
    df["before_1705"] = df["Join time"].apply(lambda time_var: int(time_var < pd.to_datetime("18:05:00").time()))

    # email split
    # keep obs if User Email is not empty
    email_df = df[df["User Email"].notnull()]

    # drop duplicates keeping min join time
    email_df = email_df.sort_values("Join time").drop_duplicates("User Email", keep="first")
    
    # export to csv using gradebook template format
    df.to_csv(output_path + "/" + output_name + ".csv", index=False)
    
    # name split
    # keep obs if User Email is empty
    name_df = df[~df["User Email"].notnull()]

    # drop duplicates keeping min join time
    name_df = name_df.sort_values("Join time").drop_duplicates("User Name", keep="first")

    # export to csv using gradebook template format
    df = pd.concat([email_df, name_df])
    pd.to_csv(output_path + "/" + output_name + ".csv", index=False)


if __name__ == "__main__":
    gen_attendance_report(r"C:\Users\Gigabyte\Desktop\zoomus_meeting_report_93025893520.csv", r"D:\Accesos directos\Trabajo\UVA\Projects\misc_tools", "attendance_report")