# 1. Keep email and join time
# 2. Drop duplicates keeping Min join time
# 3. Check who came before 17:05
# 4. Base score on join time
# 5. Export to csv using Gradebook template format

import pandas as pd

def gen_attendance_report(template_path: str, attendance_report_path: str, output_path: str, output_name: str):
    """
    Generates attendance scores from a Zoom meeting report
    """

    # load data
    df = pd.read_csv(attendance_report_path)
    df = df[["User Name", "User Email", "Join time"]]

    df["Join time"] = pd.to_datetime(df["Join time"])

    # check who came before 17:05
    df["day_month_year"] = df["Join time"].dt.date
    df["Join time"] = df["Join time"].apply(lambda x: x.time())
    df["before_1705"] = df["Join time"].apply(lambda time_var: int(time_var < pd.to_datetime("18:05:00").time()))

    ### erasing duplicates of obs with same code or name

    ## email split: keep obs if User Email is not empty
    email_df = df[df["User Email"].notnull()]

    # drop duplicates keeping min join time
    email_df = email_df.sort_values("Join time").drop_duplicates("User Email", keep="first")
        
    ## name split: keep obs if User Email is empty
    name_df = df[~df["User Email"].notnull()]

    # drop duplicates keeping min join time
    name_df = name_df.sort_values("Join time").drop_duplicates("User Name", keep="first")

    
    ### merge w template
    template = pd.read_csv(template_path)

    ## finding cols w missing values and that contain "Participation" in their name
    missing_cols = template.columns[template.isnull().any()]
    participation_cols = template.columns[template.columns.str.contains("Participation")]
    cols_to_fill = list(missing_cols.intersection(participation_cols))
    print("missing cols: ", missing_cols)
    print("participation cols: ", participation_cols)
    print("cols to fill: ", cols_to_fill)

    ## filling missing values
    ## email df
    email_df = email_df[["User Email", "before_1705"]] # keeping main cols
    email_df = email_df.rename(columns={"User Email": "SIS Login ID", # renaming cols for merge
                                        "before_1705": cols_to_fill[0]})
    email_df["SIS Login ID"] = email_df["SIS Login ID"].apply(lambda id: id.split("@")[0]) # updating id value

    # merging email df w template
    template_w_mail = template.drop(cols_to_fill[0], axis=1).merge(email_df, on="SIS Login ID", how="outer") # merging w template

    ## name df
    name_df = name_df[["User Name", "before_1705"]] # keeping main cols
    name_df = name_df.rename(columns={"User Name": "Student", # renaming cols for merge
                                      "before_1705": cols_to_fill[0]})
    name_df["Student"] = name_df["Student"].apply(lambda name: " ".join(name.split()[1:]) + 
                                                  ", " + name.split()[0]) # updating id value

    # merging name_df w template
    final_template = template_w_mail.merge(name_df, on="Student", how="outer")
    
    # combining cols to fill w same name ("_x" and "_y")
    final_template[cols_to_fill[0]] = final_template.apply(lambda row: row[cols_to_fill[0] + "_x"] if str(row[cols_to_fill[0] + "_x"]) != "nan"     
                                                           else row[cols_to_fill[0] + "_y"], axis=1) 
    
    # fixing value of col to fill for "Points Possible" row
    final_template[cols_to_fill[0]] = final_template.apply(lambda row: row[cols_to_fill[0]] if row["Student"] != "    Points Possible" else 1, axis=1)
    
    # erasing cols w "_x" or "_y" in their name
    final_template = final_template.drop([col for col in final_template.columns if "_x" in col or "_y" in col], axis=1)

    # moving corrected col to fill to its original position
    # finding index of second col to fill
    pos_to_insert = list(final_template.columns).index(cols_to_fill[1])
    final_template = final_template[final_template.columns[:pos_to_insert].tolist() + [cols_to_fill[0]] + final_template.columns[pos_to_insert:-1].tolist()]

    final_template.to_csv(output_path + "/" + output_name + ".csv", index=False)


if __name__ == "__main__":
    # gen_attendance_report(r"C:\Users\Gigabyte\Desktop\2024-08-19T2039_Grades-DS_5001-001.csv", r"C:\Users\Gigabyte\Desktop\zoomus_meeting_report_93025893520.csv", r"D:\Accesos directos\Trabajo\UVA\Projects\misc_tools", "attendance_report")
    gen_attendance_report(r"D:\Accesos directos\Trabajo\UVA\Projects\misc_tools\attendance_report.csv", r"C:\Users\Gigabyte\Desktop\zoomus_meeting_report_93025893520.csv", r"D:\Accesos directos\Trabajo\UVA\Projects\misc_tools", "attendance_report_2")