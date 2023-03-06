
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

# # insert
# cursor = db_connection()
# cursor.execute(
#                """ INSERT INTO [TT].[dbo].[LN_CP_Details] (
# 		"TPL_Number"
#       ,"Part_No"
#       ,"Part_No_Rev"
#       ,"Child_Part_Code"
#       ,"Fab_Number"
#       )VALUES (?,?,?,?,?)""","tpl11","B01460641005", "R01",
#            "CP_DRYER","AVGC377434")
# cursor.commit()
#
#
# update
# cursor = db_connection()
# cursor.execute(
#     """
#     UPDATE [TT].[dbo].[Process_Master]
#    SET "Process_Photo_Path" = ?
#  WHERE Process_Code = ?""", "Channel assembly.jpg", "CP_COOLER_PROCESS")
# cursor.commit()

#
# delete
cursor = db_connection()
cursor.execute(
    """
    DELETE FROM [TT].[dbo].[Process_Update_Table]
    """)
cursor.commit()


# update
# cursor = db_connection()
#
# TPL_MASTER = cursor.execute(
#     "SELECT * FROM[TT].[dbo].[Process_Map_Master]")
#
# TPL_MASTER_DATA = [{
#     "tpl": obj[2]
# } for obj in TPL_MASTER]
# print(len(TPL_MASTER_DATA))
#
# for data in TPL_MASTER_DATA:
#     cursor = db_connection()
#     tpl = data["tpl"]
#     print("***** tpl *****",tpl)
#     cursor.execute(
#         """
#         UPDATE [TT].[dbo].[Process_Map_Master]
#        SET "Model_Group" = ?
#      WHERE Model_Code = ? """,tpl[:2] , tpl)
#     cursor.commit()