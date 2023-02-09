
import pyodbc

def db_connection():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=PROD-DF;DATABASE=TT;UID=MEI_DF;PWD=MEI@mac;Trusted_Connection=yes')
    cursor = conn.cursor()
    return cursor

#
#
# # select data from db
# cursor = db_connection()
# process_master_details = cursor.execute(
#     "SELECT * FROM[TT].[dbo].[Process_Master]")
#
# process_master_data = [{
#     "Line_Code": obj[0], "Pro_Type_Code": obj[1], "Process_Desc": obj[2], "Tool_ID": obj[3],
#     "Process_Code": obj[4], "Bolt_Count": obj[5], "Process_Photo_Path": obj[6], "Takt_Time": obj[7],
#     "Torque": obj[8]
# } for obj in process_master_details]
# print(process_master_data)
#
#
# # insert
# cursor = db_connection()
# cursor.execute(
#                """ INSERT INTO [TT].[dbo].[Process_Master] (
# 		"Line_Code"
#       ,"Pro_Type_Code"
#       ,"Process_Desc"
#       ,"Tool_ID"
#       ,"Process_Code"
#       ,"Bolt_Count"
#       ,"Process_Photo_Path"
#       ,"Takt_Time"
#       ,"Torque")VALUES (?,?,?,?,?,?,?,?,?)""","EL1_P1_L1","CP_AIREND", "Process_Desc",
#            "C1-T01-AP02","harsha3",int(10),"",int(10),"10")
# cursor.commit()
#
#
# # # update
# # cursor = db_connection()
# # cursor.execute(
# #     """
# #     UPDATE [TT].[dbo].[Process_Master]
# #    SET "Line_Code" = ?
# #       ,"Pro_Type_Code" = ?
# #       ,"Process_Desc" = ?
# #       ,"Tool_ID" = ?
# #       ,"Process_Code" = ?
# #       ,"Bolt_Count" = ?
# #       ,"Process_Photo_Path" = ?
# #       ,"Takt_Time" = ?
# #       ,"Torque" = ?
# #  WHERE Process_Code = ?""", "EL1_P1_L1", "SUBMIT","asdghjkl","RIO-DI-1-T01", "Process_Code",10,"png",20,"34","Process_Code")
# # cursor.commit()
#
#
# # delete
# # cursor = db_connection()
# # cursor.execute(
# #     """
# #     DELETE FROM [TT].[dbo].[Process_Master]
# #     WHERE Process_Code = ?""", "gvk")
# cursor.commit()


# update
cursor = db_connection()

TPL_MASTER = cursor.execute(
    "SELECT * FROM[TT].[dbo].[Process_Map_Master]")

TPL_MASTER_DATA = [{
    "tpl": obj[2]
} for obj in TPL_MASTER]
print(len(TPL_MASTER_DATA))

for data in TPL_MASTER_DATA:
    cursor = db_connection()
    tpl = data["tpl"]
    print("***** tpl *****",tpl)
    cursor.execute(
        """
        UPDATE [TT].[dbo].[Process_Map_Master]
       SET "Model_Group" = ?
     WHERE Model_Code = ? """,tpl[:2] , tpl)
    cursor.commit()