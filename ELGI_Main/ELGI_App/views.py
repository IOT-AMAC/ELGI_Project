from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import *
import pyodbc

from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('172.17.235.72') #172.17.235.72
conn = client.connect()
print("conn " , conn)

# Create your views here.

def db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=PROD-DF;DATABASE=TT;UID=MEI_DF;PWD=MEI@mac;Trusted_Connection=yes')
    cursor = conn.cursor()
    return cursor


def demo_screen(request):
    # conn = pyodbc.connect('DRIVER={SQL Server};SERVER=  ;DATABASE= ;')
    # cursor = conn.cursor()
    # cursor.execute("""SELECT * FROM TABLE""")
    # data = cursor.fetchall()
    return render(request, 'home.html')


def dashboard(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))
        print("-----------> ", request.POST["scan"])
    station_dropdowns = Stations.objects.all().values()
    station_dropdowns = [obj['station'] for obj in station_dropdowns]
    print("station_dropdown ", station_dropdowns)
    return render(request, "dashboard.html", {'opt_list': station_dropdowns})


# def dashboard(request):
#     return render(request, 'dashboard.html')

def break_display_configuration(request):
    return render(request, 'break_display_configuration.html')


def break_display_configuration(request):
    return render(request, 'break_display_configuration.html')


def holiday(request):
    return render(request, 'holiday.html')


def message(request):
    return render(request, 'message.html')


def message_configuration(request):
    return render(request, 'message_configuration.html')


def shift_and_break(request):
    return render(request, 'shift_and_break.html')


def station_bypass(request):
    cursor = db_connection()

    if request.method == "POST":
        substationcode = request.POST.get('substationcode')
        bypass = request.POST.get('bypass')

        cursor.execute(
            """
            UPDATE [dbo].[Sub_Station]
            SET [By_pass] = ?
            WHERE [Sub_Station_Code] = ?
            """, bypass, substationcode)
        cursor.commit()

    station_bypass_details = cursor.execute(
        """SELECT [Sub_Station_Code],[Station_Name],[Station_Purpose],[By_pass] FROM [TT].[dbo].[Sub_Station]""")

    station_bypass_data = [{
        "Sub_Station_Code": obj[0], "Station_Name": obj[1], "Station_Purpose": obj[2], "Bypass": obj[3]
    } for obj in station_bypass_details]

    # print(station_bypass_data)
    return render(request, 'station_bypass.html', {"station_bypass_data": station_bypass_data})


def tool_maintenance(request):
    cursor = db_connection()
    print(request.POST)
    try:
        if request.POST["submit"] == "Add":
            print("Add group")
        # print(" bc ", Bolt_Count)
        # print(" ct ", request.POST["Cycle_Time"])
        # cursor.execute(
        #        """ INSERT INTO [TT].[dbo].[Process_Master] (
        #     "Line_Code"
        #   ,"Pro_Type_Code"
        #   ,"Process_Desc"
        #   ,"Tool_ID"
        #   ,"Process_Code"
        #   ,"Bolt_Count"
        #   ,"Process_Photo_Path"
        #   ,"Takt_Time"
        #   ,"Torque")VALUES (?,?,?,?,?,?,?,?,?)""","EL1_P1_L1",request.POST["Process_Type"], request.POST["Process_Description"],
        #        Tool_ID,request.POST["Process_Code"],int(Bolt_Count),request.POST["Guide_Pic_Path"],int(Cycle_Time),request.POST["Torque"])
        # cursor.commit()

        elif request.POST["submit"] == "Modify":
            print(request.POST["warning_type"], request.POST["set_frequency"],
                  request.POST["actual_frequency"], request.POST["tool_id"])
            cursor.execute(
                """
                UPDATE [TT].[dbo].[Tools_Warning]
                SET "Warning_Type" = ?
                    ,"Set_Frequency" = ?
                    ,"Act_Frequency" = ?
                WHERE Tool_ID = ?""", request.POST["warning_type"], request.POST["set_frequency"],
                request.POST["actual_frequency"], request.POST["tool_id"])
            cursor.commit()

    # elif request.POST["submit"] == "Delete":
    #     cursor.execute(
    #             """
    #             DELETE FROM [TT].[dbo].[Process_Master]
    #             WHERE Process_Code = ?""", request.POST["Process_Code"])
    #     cursor.commit()

    except:
        pass
    tool_maintenance_details = cursor.execute(
        """SELECT [PK_Code]
      ,[Line_Code]
      ,[Tool_ID]
      ,[Warning_Type]
      ,[Set_Frequency]
      ,[Act_Frequency]
      ,[Created_Date]
      ,[Reset_Date]
      ,[Warning_Status]
      ,[Duration_Date]
        FROM [TT].[dbo].[Tools_Warning]""")

    tool_maintenance_data = [{
        "PK_Code": obj[0], "Line_Code": obj[1], "Tool_ID": obj[2], "Warning_Type": obj[3], "Set_Frequency": obj[4],
        "Act_Frequency": obj[5], "Created_Date": obj[6], "Reset_Date": obj[7], "Warning_Status": obj[8],
        "Duration_Date": obj[9]
    } for obj in tool_maintenance_details]

    return render(request, 'tool_maintenance.html', {"tool_maintenance_data": tool_maintenance_data})


def tool_traceability(request):
    cursor = db_connection()

    tool_traceability_details = cursor.execute(
        """SELECT [PK_Code]
      ,[Line_Code]
      ,[Tool_ID]
      ,[Warning_Type]
      ,[Set_Frequency]
      ,[Act_Frequency]
      ,[Created_Date]
      ,[Reset_Date]
      ,[Warning_Status]
      ,[Duration_Date]
        FROM [TT].[dbo].[Tools_Warning]""")

    tool_traceability_data = [{
        "PK_Code": obj[0], "Line_Code": obj[1], "Tool_ID": obj[2], "Warning_Type": obj[3], "Set_Frequency": obj[4],
        "Act_Frequency": obj[5], "Created_Date": obj[6], "Reset_Date": obj[7], "Warning_Status": obj[8],
        "Duration_Date": obj[9]
    } for obj in tool_traceability_details]

    return render(request, 'tool_traceability.html', {"tool_traceability_data": tool_traceability_data})


def child_part_dropdown(request):
    return render(request, 'child_part_dropdown.html')


def child_part_details(request):
    cursor = db_connection()

    child_part_detail = cursor.execute(
        """SELECT * FROM[TT].[dbo].[LN_CP_Details] WHERE
    Fab_Number IN (
     SELECT TOP(500)[FAB_NO] FROM[TT].[dbo].[LN_Order_Release] ORDER BY[Release_Date] DESC
    )""")

    # child_part_detail = cursor.execute(
    #     """SELECT TOP(?)[TPL_Number], [Part_No], [Part_No_Rev]
    # , [Spec_1_Description] , [Spec_1_Value]    , [Spec_2_Description] , [Spec_2_Value]
    # , [Spec_3_Description]  , [Spec_3_Value]    , [Spec_4_Description], [Spec_4_Value]
    # , [Spec_5_Description], [Spec_5_Value]    , [Spec_6_Description]  , [Spec_6_Value]
    # , [Spec_7_Description], [Spec_7_Value]    , [Spec_8_Description], [Spec_8_Value]
    # , [Spec_9_Description], [Spec_9_Value]    , [Spec_10_Description], [Spec_10_Value]
    # , [Spec_11_Description], [Spec_11_Value]    , [Spec_12_Description], [Spec_12_Value]
    # , [Child_Part_Code]  , [Fab_Number]
    # FROM[TT].[dbo].[LN_CP_Details]""",1000)

    child_part_detail_data = [
        {"TPL_Number": obj[0], "Part_No": obj[1], "Part_No_Rev": obj[2], "Spec_1_Description": obj[3],
         "Spec_1_Value": obj[4],
         "Spec_2_Description": obj[5], "Spec_2_Value": obj[6], "Spec_3_Description": obj[7], "Spec_3_Value": obj[8],
         "Spec_4_Description": obj[9], "Spec_4_Value": obj[10], "Spec_5_Description": obj[11], "Spec_5_Value": obj[12],
         "Spec_6_Description": obj[13], "Spec_6_Value": obj[14]
            , "Spec_7_Description": obj[15], "Spec_7_Value": obj[16], "Spec_8_Description": obj[17],
         "Spec_8_Value": obj[18], "Spec_9_Description": obj[19], "Spec_9_Value": obj[20],
         "Spec_10_Description": obj[21], "Spec_10_Value": obj[22], "Spec_11_Description": obj[23],
         "Spec_11_Value": obj[24], "Spec_12_Description": obj[25], "Spec_12_Value": obj[26]
            , "Child_Part_Code": obj[27], "Fab_Number": obj[28]
         } for obj in child_part_detail]

    return render(request, 'child_part_details.html', {"child_part_detail_data": child_part_detail_data})


def order_release(request):
    cursor = db_connection()
    # order_release_details = cursor.execute(
    #     """SELECT * FROM [TT].[dbo].[LN_Order_Release]""")

    order_release_details = cursor.execute(
        """ SELECT TOP(500) [TPL_No],  [FAB_NO], [pd_no]
    , [Release_Date], [Status], [Model_Code]
    , [Description], [TPL_Description], [Completed_Date]
    FROM [TT].[dbo].[LN_Order_Release] ORDER BY[Release_Date] DESC """)

    order_release_data = [
        {"Release_Date": obj[3], "TPL_No": obj[0], "FAB_NO": obj[1], "pd_no": obj[2],
         "Status": obj[4], "Model_Code": obj[5], "Description": obj[6], "TPL_Description": obj[7],
         "Completed_Date": obj[8]
         } for obj in order_release_details]

    return render(request, 'order_release.html', {"order_release_data": order_release_data})


def order_release_error_table(request):
    cursor = db_connection()
    # order_release_error_details = cursor.execute(
    #     """SELECT * FROM [TT].[dbo].[LN_Order_Release_Error]""")

    order_release_error_details = cursor.execute(
        """ SELECT TOP(500)[TPL_No]
    , [FAB_NO], [Model_Code], [Po_No]
    , [Release_Date], [Description], [TPL_Description]
    FROM[TT].[dbo].[LN_Order_Release_Error] ORDER BY[Release_Date] DESC""")

    order_release_error_data = [
        {"TPL_No": obj[0], "FAB_NO": obj[1], "Model_Code": obj[2], "Po_No": obj[3],
         "Release_Date": obj[4], "Description": obj[5], "TPL_Description": obj[6]
         } for obj in order_release_error_details]

    return render(request, 'order_release_error_table.html', {"order_release_error_data": order_release_error_data})


#################

def company(request):
    cursor = db_connection()
    # st_operation_tab

    if request.method == "POST":
        print("******************************")
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))

        if request.POST["submit"] == "update":
            cursor.execute(
                """ UPDATE [TT].[dbo].[Operator]
               SET "Skill_Required" = ?
                  ,"Reponsible_For" = ?
                  ,"Screen_text" = ?
             WHERE Sub_Station_Code = ? and Operator_Code = ? """, request.POST["skill_required"],
                request.POST["responsible_for"],
                request.POST["screen_text"], request.POST["sub_station_code"], request.POST["st_operator_code"])
            cursor.commit()

    st_operation_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Operator]""")
    st_operation_tab = [
        {"Sub_Station_Code": obj[0], "Operator_Code": obj[1], "Skill_Required": obj[2], "Reponsible_For": obj[3],
         "Screen_text": obj[4]} for obj in st_operation_tab]

    # state_tab
    state_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[State]""")
    state_tab = [
        {"Country_Code": obj[0], "State_Code": obj[1], "State_Name": obj[2]} for obj in
        state_tab]

    # city_tab
    city_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[City]""")
    city_tab = [
        {"State_Code": obj[0], "City_Code": obj[1], "City_Name": obj[2]} for obj in
        city_tab]

    # address_tab
    address_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Address]""")
    address_tab = [
        {"City_Code": obj[0], "Address_Code": obj[1], "Address": obj[2]} for obj in
        address_tab]

    # company tab
    company_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Company]""")
    company_tab = [
        {"Address_Code": obj[0], "Company_Code": obj[1], "Company_Name": obj[2], "Latitude": obj[3],
         "Longitude": obj[4]} for obj in
        company_tab]

    # plant_tab
    plant_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Plant]""")
    plant_tab = [
        {"Company_Code": obj[0], "Plant_Code": obj[1], "Plant_Name": obj[2]} for obj in
        plant_tab]

    # line tab
    line_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Line]""")
    line_tab = [
        {"Plant_Code": obj[0], "Line_Code": obj[1], "Line_Name": obj[2]} for obj in
        line_tab]

    # station tab
    station_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Station]""")
    station_tab = [
        {"Line_Code": obj[0], "Station_Code": obj[1], "Station_name": obj[2], "Station_Purpose": obj[3]} for obj in
        station_tab]

    # substation tab
    substation_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Sub_Station]""")
    substation_tab = [
        {"Station_Code": obj[0], "Sub_Station_Code": obj[1], "Station_Name": obj[2], "Station_Purpose": obj[3],
         "By_pass": obj[4]} for obj in substation_tab]

    # country tab
    country_tab = cursor.execute(
        """SELECT [Country_Code], [Country_Name] FROM[TT].[dbo].[Country]""")
    country_data = [{"Country_Code": obj[0], "Country_Name": obj[1]} for obj in country_tab]

    return render(request, 'company.html',
                  {'st_operation_tab': st_operation_tab, 'state_tab': state_tab, 'city_tab': city_tab,
                   'address_tab': address_tab, 'company_tab': company_tab, 'plant_tab': plant_tab, 'line_tab': line_tab,
                   'station_tab': station_tab, 'substation_tab': substation_tab, 'country_data': country_data})


def tpl_master(request):
    cursor = db_connection()

    if request.method == "POST":
        print("******************************")
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))

        if request.POST["submit"] == "Add":
            cursor.execute(
                """ INSERT INTO [TT].[dbo].[TPL_Master] (
                        "TPL_No"
                      ,"Model_Group"
                      ,"TPL_Description"
                      ,"Machines_on_AGV")
                      VALUES (?,?,?,?)""", request.POST["TPL_Code"],
                request.POST["Group"], request.POST["TPL_Description"], request.POST["AGV"])
            cursor.commit()

        elif request.POST["submit"] == "Modify":
            cursor.execute(
                """ UPDATE [TT].[dbo].[TPL_Master]
               SET "TPL_No" = ?
                  ,"Model_Group" = ?
                  ,"TPL_Description" = ?
                  ,"Machines_on_AGV" = ?
             WHERE TPL_No = ?""", request.POST["TPL_Code"],
                request.POST["Group"], request.POST["TPL_Description"], request.POST["AGV"], request.POST["TPL_Code"])
            cursor.commit()

    tpl_master_details = cursor.execute(
        "SELECT * FROM[TT].[dbo].[TPL_Master]")

    tpl_master_data = [{
        "TPL_Code": obj[0], "Model_Group": obj[1],
        "TPL_Description": obj[2], "Machines_on_AGV": obj[3]
    } for obj in tpl_master_details]
    # print(tpl_master_data)

    return render(request, 'tpl_master.html', {"tpl_master_data": tpl_master_data})


def tool_master(request):
    cursor = db_connection()
    tools_type_master_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Tools_Type_Master]""")
    tools_type_master_data = [{"Line_Code": obj[2], "Tool_Type_ID": obj[0], "Tool_Type": obj[2]
                               } for obj in tools_type_master_details]

    tool_master_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[TPL_Master]""")
    tool_master_data = [{
        "[TPL_Code]": obj[0], "Model_Code": obj[1], "TPL_Description": obj[2], "Machines_on_AGV": obj[3]
    } for obj in tool_master_details]

    return render(request, 'tool_master.html', {'tools_type_master_data': tools_type_master_data})


# Process master
def process_master(request):
    cursor = db_connection()

    if request.method == "POST":
        print("******************************")
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))
        try:
            if request.POST["Bolt_Count"] == "":
                Bolt_Count = 0
            else:
                Bolt_Count = request.POST["Bolt_Count"]

            if request.POST["Cycle_Time"] == "":
                Cycle_Time = 0
            else:
                Cycle_Time = request.POST["Cycle_Time"]

            if request.POST["Tool_ID"] == "":
                Tool_ID = "NULL"
            else:
                Tool_ID = request.POST["Tool_ID"]

        except:
            pass

        if request.POST["submit"] == "Add":
            # print(" bc ", Bolt_Count)
            # print(" ct ", request.POST["Cycle_Time"])
            cursor.execute(
                """ INSERT INTO [TT].[dbo].[Process_Master] (
             "Line_Code"
           ,"Pro_Type_Code"
           ,"Process_Desc"
           ,"Tool_ID"
           ,"Process_Code"
           ,"Bolt_Count"
           ,"Process_Photo_Path"
           ,"Takt_Time"
           ,"Torque")VALUES (?,?,?,?,?,?,?,?,?)""", "EL1_P1_L1", request.POST["Process_Type"],
                request.POST["Process_Description"],
                Tool_ID, request.POST["Process_Code"], int(Bolt_Count), request.POST["Guide_Pic_Path"], int(Cycle_Time),
                request.POST["Torque"])
            cursor.commit()

        elif request.POST["submit"] == "Modify":
            cursor.execute(
                """
                UPDATE [TT].[dbo].[Process_Master]
               SET "Line_Code" = ?
                  ,"Pro_Type_Code" = ?
                  ,"Process_Desc" = ?
                  ,"Tool_ID" = ?
                  ,"Process_Code" = ?
                  ,"Bolt_Count" = ?
                  ,"Process_Photo_Path" = ?
                  ,"Takt_Time" = ?
                  ,"Torque" = ?
             WHERE Process_Code = ?""", "EL1_P1_L1", request.POST["Process_Type"], request.POST["Process_Description"],
                Tool_ID, request.POST["Process_Code"], int(Bolt_Count), request.POST["Guide_Pic_Path"], int(Cycle_Time),
                request.POST["Torque"], request.POST["Process_Code"])
            cursor.commit()

        elif request.POST["submit"] == "Delete":
            cursor.execute(
                """
                DELETE FROM [TT].[dbo].[Process_Master]
                WHERE Process_Code = ?""", request.POST["Process_Code"])
            cursor.commit()
        try:
            if request.POST["Process_code_radio"] == "on":
                if request.POST["submit"] == "PM_Add":
                    cursor.execute(
                        """ INSERT INTO [TT].[dbo].[Process_Master_Mapping] (
                         "Model_Group"
                         ,"TPL_No"
                       ,"Operator_Code"
                       ,"Process_Code"
                       ,"Process_Seq_No"
                       ,"Line_Code")VALUES (?,?,?,?,?,?)""", request.POST["group"], request.POST["tpl_code"],
                        request.POST["operator_code"],
                        request.POST["process_code"], request.POST["sequence_no"], "EL1_P1_L1")
                    cursor.commit()

        except:
            pass

        # elif request.POST["submit"] == "PM_Modify":
        #     cursor.execute(
        #         """
        #         UPDATE [TT].[dbo].[Process_Map_Master]
        #         SET "Model_Group" = ?
        #           ,"Model_Code" = ?
        #           ,"Operator_Code" = ?
        #           ,"Process_Code" = ?
        #           ,"Process_Seq_No" = ?
        #           ,"Line_Code" = ?
        #         WHERE PMMKEY = ?""", request.POST["group"], request.POST["model_code"], request.POST["operator_code"],
        #         request.POST["process_code"], request.POST["sequence_no"],"EL1_P1_L1",request.POST["pmmkey"])
        #     cursor.commit()
        #
        # elif request.POST["submit"] == "PM_Delete":
        #     cursor.execute(
        #         """
        #         DELETE FROM [TT].[dbo].[Process_Map_Master]
        #         WHERE PMMKEY = ?""", request.POST["pmmkey"])
        #     cursor.commit()

    process_library_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Process_Master]""")

    process_library_data = [{
        "Line_Code": obj[0], "Pro_Type_Code": obj[1], "Process_Desc": obj[2], "Tool_ID": obj[3],
        "Process_Code": obj[4], "Bolt_Count": obj[5], "Process_Photo_Path": obj[6], "Takt_Time": obj[7],
        "Torque": obj[8]
    } for obj in process_library_details]
    # print({"process_master_data":process_master_data})

    process_type_details = cursor.execute(
        """SELECT [Pro_Type_Code] FROM [TT].[dbo].[Process_Type_Master]""")
    process_type_data = [i[0] for i in process_type_details]
    # print("process_type_data  ",process_type_data)

    tool_id_details = cursor.execute(
        """SELECT [Tool_ID] FROM [TT].[dbo].[Tools_Master]""")
    tool_id_data = [j[0] for j in tool_id_details]
    # print("tool_ids ", tool_id_data)

    operator_code_details = cursor.execute(
        """SELECT [Operator_Code] FROM[TT].[dbo].[Operator]""")
    operator_code_data = [obj[0] for obj in operator_code_details]
    # print("operator_code_data",operator_code_data)

    process_code_details = cursor.execute(
        """SELECT [Process_Code] FROM[TT].[dbo].[Process_Master]""")
    process_code_data = [obj[0] for obj in process_code_details]
    # print("process_code_data",process_code_data)

    tpl_code_details = cursor.execute(
        """SELECT DISTINCT  [TPL_No] FROM [TT].[dbo].[TPL_Master]""")
    tpl_code_data = [obj[0] for obj in tpl_code_details]
    # print("model_code_data",model_code_data)

    active_tpls_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Active_TPL_List]""")
    active_tpls_data = [{
        "TPL_Code": obj[0], "TPL_Description": obj[1], "Operation_Code": obj[2], "No_of_Processes": obj[7]
    } for obj in active_tpls_details]
    print("active_tpls_data ", active_tpls_data)

    return render(request, 'process_master.html',
                  {"tpl_code_data": tpl_code_data, "process_code_data": process_code_data,
                   "operator_code_data": operator_code_data, "process_type_data": process_type_data,
                   "tool_id_data": tool_id_data, "process_library_data": process_library_data,
                   "active_tpls_data": active_tpls_data})


def active_tpl_list(request, tpl_code, operation_code):
    cursor = db_connection()

    if request.method == "POST":
        print("******************************")
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))

        if request.POST["submit"] == "update":
            cursor.execute(
                """
                UPDATE [TT].[dbo].[Process_Master_Mapping]
               SET "Operator_Code" = ?
                  ,"Process_Seq_No" = ?
             WHERE PMKEY = ? """,
                request.POST["station"], request.POST["sequence"], request.POST["pmkey"])
            cursor.commit()

        if request.POST["submit"] == "delete":
            cursor.execute(
                """DELETE FROM [TT].[dbo].[Process_Master_Mapping]
                WHERE PMKEY = ?""", request.POST["pmkey"])
            cursor.commit()
    print(tpl_code,operation_code)
    process_details = cursor.execute(
        """select * FROM[TT].[dbo].[Process_Master_Mapping] WHERE TPL_No = ? and Operator_Code = ? """, tpl_code,
        operation_code)

    processes_list_data = [{"Model_Group": obj[0], "TPL_No": obj[1], "Operation_Code": obj[2],
                            "Process_Code": obj[3], "Sequence_No": obj[4], "Line_Code": obj[5], "PMKEY": obj[6]} for obj
                           in
                           process_details]
    print(processes_list_data)
    return render(request, 'active_tpl_list.html', {"processes_list_data": processes_list_data})


def employee(request):
    cursor = db_connection()

    employee_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Employee_Details_UPD]""")
    employee_data = [{"Company_Code": obj[0], "Emp_ID": obj[1], "Emp_Name": obj[2], "Role_Code": obj[3],
                      "Emp_Photo_Path": obj[4], "User_Name": obj[5], "Password": obj[6]} for obj in employee_details]

    return render(request, 'employee.html', {'employee_data': employee_data})


def tool_warning_master(request):
    cursor = db_connection()
    twm_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Tools_Warning]""")
    twm_data = [{"Line_Code": obj[1], "PK_Code": obj[0], "Tool_ID": obj[2],
                 "Warning_Type": obj[3], "Set_Frequency": obj[4], "Act_Frequency": obj[5],
                 "Created_Date": obj[6], "Reset_Date": obj[7], "Warning_Status": obj[8],
                 "Duration_Date": obj[9]} for obj in twm_details]

    return render(request, 'tool_warning_master.html', {'twm_data': twm_data})


def packing(request):
    cursor = db_connection()
    packing_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Packing_DD]""")
    packing_data = [{"Package_Code": obj[0]} for obj in packing_details]

    return render(request, 'packing.html', {'packing_data': packing_data})


def drive_coupling_master(request):
    cursor = db_connection()

    if request.method == "POST":
        print("******************************")
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))

    dcp_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Drive_Coupling_Master]""")
    dcm_data = [{"TPL_No": obj[0], "Model_Description": obj[1], "Model_Code": obj[2],
                 "Distance": obj[3], "Sensor_No": obj[4], "Test_Certificate": obj[5]
                 } for obj in dcp_details]

    return render(request, 'drive_coupling_master.html', {'dcm_data': dcm_data})


def process(request):
    return render(request, 'process.html')


def process_p(request):
    return render(request, 'process_p.html')


def dmi(request):
    return render(request, 'dmi.html')


def login(request):
    return render(request, 'login.html')


def pdi(request):
    return render(request, 'pdi.html')


def test_booth_master(request):
    return render(request, 'test_booth_master.html')


def test_certificate_1(request):
    return render(request, 'test_certificate_1.html')


def test_certificate_2(request):
    return render(request, 'test_certificate_2.html')


def test_certificate_3(request):
    return render(request, 'test_certificate_3.html')


def test_certificate_4(request):
    return render(request, 'test_certificate_4.html')


def test_certificate_5(request):
    return render(request, 'test_certificate_5.html')


def test_certificate_6(request):
    return render(request, 'test_certificate_6.html')


def test_certificate_7(request):
    return render(request, 'test_certificate_7.html')


def test_certificate_8(request):
    return render(request, 'test_certificate_8.html')


def list_of_fab_number(request):
    return render(request, 'list_of_fab_number.html')


def scan_fab_number(request):
    return render(request, 'scan_fab_number.html')


def start_test(request):
    return render(request, 'start_test.html')


def pdi_2(request):
    return render(request, 'pdi_2.html')


############################################################
def reports(request):
    return render(request, 'reports.html')


def compressprocessstatus(request):
    return render(request, 'compressprocessstatus.html')


def lnserverstatus(request):
    return render(request, 'lnserverstatus.html')


def processstatus(request):
    return render(request, 'processstatus.html')


def lnerpstatus(request):
    return render(request, 'lnerpstatus.html')


def tpldetails(request):
    return render(request, 'tpldetails.html')


def processsequence(request):
    return render(request, 'processsequence.html')


###################################################################
def pdi_3(request):
    return render(request, 'pdi_3.html')

def alpha_line(request):
    cursor = db_connection()
    station = "Sub1_OP1"
    Emp_ID = 100213

    Emp_details = cursor.execute(
        """SELECT [Emp_ID],[Emp_Name]
        ,[Skill_Level],[Emp_Photo_Path] FROM [TT].[dbo].[Employee_Details_View]
        WHERE [Emp_ID] = ?""",Emp_ID
    )

    initial_screen_details = cursor.execute(
        """SELECT  [TPL_No],[FAB_NO]
        ,[Release_Date],[TPL_Description]
        FROM [TT].[dbo].[Sub1_OP1_Fab_Init_View]"""
    )

    Emp_details_data = [{"Emp_ID":obj[0], "Emp_Name":obj[1],"Skill_Level":obj[2],"Emp_Photo_Path":obj[3]} for obj in Emp_details]
    print("Emp_details_data ",Emp_details_data)

    initial_screen_data = [{"TPL_No":obj[0],"FAB_NO":obj[1],"Release_Date":obj[2],"TPL_Description":obj[3]} for obj in initial_screen_details]
    print("initial_screen_data ",initial_screen_data)

    #
    # station_details = cursor.execute(
    #     """SELECT * FROM[TT].[dbo].[ST_IT] WHERE [Station_Code] = ?""",station)
    # station_data = [{"Station_Code": obj[0], "Emp_Name": obj[1], "EMP_ID": obj[2],
    #              "Emp_Path": obj[3], "Emp_Skill": obj[4], "Req_Skill": obj[5],"Line_name":obj[6],
    #              "Station_Name":obj[7],"Fab_no":obj[8],"TPL_No":obj[9],"Model_No":obj[10],
    #              "Model_no_Display":obj[11],"Pro_Tack_Time":obj[12],"Pro_Description":obj[13],
    #              "Pro_Photo_Path":obj[17],"Pro_Type_Code":obj[18],"Pro_Process_Code":obj[23],
    #              "Pro_Process_Seq_No":obj[24],"Pro_Screen_Count":obj[31],
    #              } for obj in station_details]
    # print("station details",station_data)
    return render(request, 'alpha_line.html')

def alphaline3(request):
    TPL_NO = 'tpl11'
    FAB_N0 = 'AVGC377434'

    cursor = db_connection()

    order_release_query = """SELECT * FROM [TT].[dbo].[Sub1_OP1_Fab_Init_View] WHERE Release_Date >= DATEADD(day, -7, GETDATE()) AND Status = 'R'"""
    order_release_table = [{
        "TPL_No":obj[0],
        "FAB_No":obj[1],
        "Release_Date":obj[3],
        "TPL_Description":obj[7]
    }for obj in cursor.execute(order_release_query)]

    order_release_error_query = """SELECT * FROM [TT].[dbo].[Sub1_OP1_Fab_Init_View] WHERE Release_Date >= DATEADD(day, -7, GETDATE()) AND Status = NULL """
    order_release_error_table = [{
        "TPL_No": obj[0],
        "FAB_No": obj[1],
        "Release_Date": obj[3],
        "TPL_Description": obj[7]
    } for obj in cursor.execute(order_release_error_query)]
    #print("order_release_table",order_release_table)
    #print("order release error table", order_release_error_table)

    employee_details_query = """ SELECT * FROM [TT].[dbo].[Employee_Details_View] WHERE User_Name='100213' """
    employee_details_list = [{
        "Emp_ID": obj[0],
        "Emp_Name": obj[1],
        "Skill_Level": obj[2]
    } for obj in cursor.execute(employee_details_query)]

    process_seq = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Sub_Station_Screens_Data_View] WHERE TPL_No = ? AND FAB_NO = ?""", TPL_NO, FAB_N0)

    process_seq_data = [{"FAB_NO": obj[0]
                            , "TPL_No": obj[1]
                            , "Operator_Code": obj[2]
                            , "Process_Seq_No": obj[3]
                            , "Pro_Type_Code": obj[4]
                            , "Process_Desc": obj[5]
                            , "Process_Photo_Path": obj[6]
                            , "Torque": obj[7]
                            , "Tool_ID": obj[8]
                            , "Bolt_Count": obj[9]
                            , "Takt_Time": obj[10]
                            , "Total_Processes": obj[11]} for obj in process_seq]
    print("process_name", process_seq_data[0])

    json = {
        "page_type": "home",
        "page_details":{
            "order_release_table": order_release_table,
            "order_release_error_table": order_release_error_table
        },
        "employee_details": {
            "Emp_Name":employee_details_list[0]["Emp_Name"],
            "Emp_ID": employee_details_list[0]["Emp_ID"],
            "Skill_level": employee_details_list[0]["Skill_Level"]
        },
        "CP_AIREND":True,
        "process_seq":process_seq_data[0]
    }
    print("Final Json",json)

    if request.method == "POST" and "cp_airend" in request.POST:
        partno = request.POST["partno"]
        revno = request.POST["revno"]
        serialno = request.POST["serialno"]

        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_AIREND'"""

        ln_cp_details = order_release_error_table = [{
        "Part_No": obj[1],
        "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]
        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Type],[Part_No],[Rev_No],[Serial_No],[Status]) values (?,?,?,?,?,?,?,?,?)",
                order_release_table[0]["TPL_No"],order_release_table[0]["FAB_No"],employee_details_list[0]["Emp_Name"],employee_details_list[0]["Emp_ID"],process_seq_data[0]["Pro_Type_Code"],partno,revno,serialno,"c")
            cursor.commit()
            cursor.close()
            json = {
                "page_type": "home",
                "page_details": {
                    "order_release_table": order_release_table[0],
                    "order_release_error_table": order_release_error_table
                },
                "employee_details": {
                    "Emp_Name": employee_details_list[0]["Emp_Name"],
                    "Emp_ID": employee_details_list[0]["Emp_ID"],
                    "Skill_level": employee_details_list[0]["Skill_Level"]
                },
                "CP_COOLER": True,
                "process_seq": process_seq_data[0]
            }
            return render(request, 'alphaline3.html', json)
        else:
            json = {
                "page_type": "home",
                "page_details": {
                    "order_release_table": order_release_table[0],
                    "order_release_error_table": order_release_error_table
                },
                "employee_details": {
                    "Emp_Name": employee_details_list[0]["Emp_Name"],
                    "Emp_ID": employee_details_list[0]["Emp_ID"],
                    "Skill_level": employee_details_list[0]["Skill_Level"]
                },

                "CP_AIREND": True,
                "process_seq": process_seq_data[0]
            }
            return render(request, 'alphaline3.html', json)

    if request.method == "POST" and "cp_cooler" in request.POST:
        partno = request.POST["partno"]
        revno = request.POST["revno"]
        serialno = request.POST["serialno"]

        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_COOLER'"""

        ln_cp_details = order_release_error_table = [{
            "Part_No": obj[1],
            "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]

        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Type],[Part_No],[Rev_No],[Serial_No],[Status]) values (?,?,?,?,?,?,?,?,?)",
                order_release_table[0]["TPL_No"], order_release_table[0]["FAB_No"],
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"],
                "CP_COOLER", partno, revno, serialno, "c")
            cursor.commit()
            cursor.close()
            json = {
                "page_type": "home",
                "page_details": {
                    "order_release_table": order_release_table[0],
                    "order_release_error_table": order_release_error_table
                },
                "employee_details": {
                    "Emp_Name": employee_details_list[0]["Emp_Name"],
                    "Emp_ID": employee_details_list[0]["Emp_ID"],
                    "Skill_level": employee_details_list[0]["Skill_Level"]
                },

                "process_seq": process_seq_data[0]
            }
            return render(request, 'alphaline3.html', json)
        else:
            json = {
                "page_type": "home",
                "page_details": {
                    "order_release_table": order_release_table[0],
                    "order_release_error_table": order_release_error_table
                },
                "employee_details": {
                    "Emp_Name": employee_details_list[0]["Emp_Name"],
                    "Emp_ID": employee_details_list[0]["Emp_ID"],
                    "Skill_level": employee_details_list[0]["Skill_Level"]
                },
                "CP_COOLER": True,
                "process_seq": process_seq_data[0]
            }
            return render(request, 'alphaline3.html', json)

    return render(request, 'alphaline3.html',json)

def process_cycle(request):
    cursor = db_connection()
    # if request.method == 'POST' and 'form1' in request.POST:

def station_order_release(request):
    cursor = db_connection()

    order_release_query = """SELECT * FROM [TT].[dbo].[Sub1_OP1_Fab_Init_View] WHERE Release_Date >= DATEADD(day, -20, GETDATE()) AND Status = 'R'"""
    order_release_table = [{
        "TPL_No": obj[0],
        "FAB_No": obj[1],
        "Release_Date": obj[3],
        "TPL_Description": obj[7]
    } for obj in cursor.execute(order_release_query)]

    order_release_error_query = """SELECT * FROM [TT].[dbo].[Sub1_OP1_Fab_Init_View] WHERE Release_Date >= DATEADD(day, -12, GETDATE()) AND Status = NULL """
    order_release_error_table = [{
        "TPL_No": obj[0],
        "FAB_No": obj[1],
        "Release_Date": obj[3],
        "TPL_Description": obj[7]
    } for obj in cursor.execute(order_release_error_query)]
    #print("order_release_table",order_release_table)
    #print("order release error table", order_release_error_table)

    employee_details_query = """ SELECT * FROM [TT].[dbo].[Employee_Details_View] WHERE User_Name='100213' """
    employee_details_list = [{
        "Emp_ID": obj[0],
        "Emp_Name": obj[1],
        "Skill_Level": obj[2]
    } for obj in cursor.execute(employee_details_query)]

    json = {
        "order_release_table":order_release_table,
        "order_release_error_table":order_release_error_table,
        "employee_details_list":employee_details_list,
        "tplno":"tpl11",
        "fabno":"AVGC377434"
    }
    print(json)
    return render(request,'stations/station_home.html',json)

def substation(request,tplno, fabno):
    cursor = db_connection()
    process_seq_list  = []


    employee_details_query = """ SELECT * FROM [TT].[dbo].[Employee_Details_View] WHERE User_Name='100213' """
    employee_details_list = [{
        "Emp_ID": obj[0],
        "Emp_Name": obj[1],
        "Skill_Level": obj[2]
    } for obj in cursor.execute(employee_details_query)]

    json = {
        "process_type": "default",
        "employee_details": {
            "Emp_Name": employee_details_list[0]["Emp_Name"],
            "Emp_ID": employee_details_list[0]["Emp_ID"],
            "Skill_level": employee_details_list[0]["Skill_Level"]
        },

    }

    '''
    if request.method == "POST" and "order_release" in request.POST:
        tplno = request.POST["tplno"]
        fabno = request.POST["fabno"]
        print("order release data",tplno, fabno)
    '''

    if request.method == "POST" and "process" in request.POST:
        #print("POST Process data",request.POST)
        process_validate(request, tplno, fabno, employee_details_list)


    process_seq_data = finding_seq(tplno, fabno)

    if process_seq_data == "seq_complete":
        return redirect(station_order_release)

    json = {
            "process_type":process_seq_data["Pro_Type_Code"],
            "employee_details": {
                "Emp_Name": employee_details_list[0]["Emp_Name"],
                "Emp_ID": employee_details_list[0]["Emp_ID"],
                "Skill_level": employee_details_list[0]["Skill_Level"]
            },
            "process_seq": process_seq_data
        }
    return render(request,'stations/substation.html',json)

def finding_seq(tplno, fabno):
    cursor = db_connection()
    base_url = r"images/users/"
    completed_seq_no_query = """ SELECT Process_Seq_No FROM [TT].[dbo].[Process_Update_Table] WHERE TPL_No = ? AND Fab_No = ? AND Process_Status = 'c' ORDER BY Process_Seq_No ASC """
    completed_seq_no_list  = [obj[0] for obj in cursor.execute(completed_seq_no_query,tplno, fabno)]
    process_seq_no_query  = """SELECT Process_Seq_No FROM [TT].[dbo].[Sub_Station_Screens_Data_View] WHERE TPL_No = ? AND FAB_NO = ? ORDER BY Process_Seq_No ASC"""
    process_seq_no_list = [obj[0] for obj in cursor.execute(process_seq_no_query, tplno, fabno)]
    #print("seq_no lists", completed_seq_no_list, process_seq_no_list)

    for i in completed_seq_no_list:
        if i in process_seq_no_list:
            process_seq_no_list.remove(i)
    print("present seq_no",process_seq_no_list)

    if len(process_seq_no_list) == 0:
        return "seq_complete"

    process_seq = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Sub_Station_Screens_Data_View] WHERE TPL_No = ? AND FAB_NO = ? AND Process_Seq_No = ?""",tplno, fabno, process_seq_no_list[0])
    process_seq_list = [{"FAB_NO": obj[0]
                            , "TPL_No": obj[1]
                            , "Operator_Code": obj[2]
                            , "Process_Seq_No": obj[3]
                            , "Pro_Type_Code": obj[4]
                            , "Process_Desc": obj[5]
                            , "Process_Photo_Path": base_url + obj[6]
                            , "Torque": obj[7]
                            , "Tool_ID": obj[8]
                            , "Bolt_Count": obj[9]
                            , "Takt_Time": obj[10]
                            , "Total_Processes": obj[11]} for obj in process_seq]
    if process_seq_list[0]["Pro_Type_Code"] == "CP_CONTROL_PANEL":
        cpdropdown_query = """SELECT Drop_Down_String FROM [TT].[dbo].[CP_Dropdown] WHERE Child_Part_Code = 'CP_CONTROL_PANEL' """
        cpdropdown_list = [obj[0] for obj in cursor.execute(cpdropdown_query)]
        print("cp_dropdown", cpdropdown_list)
        process_seq_list[0].update({"cpdropdown_list":cpdropdown_list})

    if process_seq_list[0]["Pro_Type_Code"] == "CP_BELT_DETAILS":
        cpdropdown_query = """SELECT Drop_Down_String FROM [TT].[dbo].[CP_Dropdown] WHERE Child_Part_Code = 'CP_BELT_DETAILS' """
        cpdropdown_list = [obj[0] for obj in cursor.execute(cpdropdown_query)]
        print("cp_dropdown", cpdropdown_list)
        process_seq_list[0].update({"cpdropdown_list":cpdropdown_list})
    return process_seq_list[0]

def process_validate(request, tplno, fabno, employee_details_list):
    cursor = db_connection()
    result = ""

    if request.method == "POST" and "CP_AIREND" in request.POST["process"]:
        partno = request.POST["airend_partno"]
        revno = request.POST["airend_revno"]
        serialno = request.POST["airend_serialno"]
        process_seqno = int(request.POST["process_seq_no"]) + 1

        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_AIREND'"""

        ln_cp_details = [{
            "Part_No": obj[1],
            "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]
        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Seq_No],[Process_Code],[Part_No],[Rev_No],[Serial_No],[Process_Status]) values (?,?,?,?,?,?,?,?,?,?)",
                tplno, fabno,
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"],process_seqno,
                "CP_AIREND", partno, revno, serialno, "c")
            cursor.commit()
            cursor.close()
            result = "data validated"
        else:
            result = "data not validated"
        print("result",result)

    if request.method == "POST" and "CP_CONTROL_PANEL" in request.POST["process"]:
        partno = request.POST["controlpanel_partno"]
        revno = request.POST["controlpanel_revno"]
        serialno = request.POST["controlpanel_serialno"]
        process_seqno = int(request.POST["process_seq_no"]) + 1
        model = request.POST["controlpanel_model"]

        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_CONTROL_PANEL'"""

        ln_cp_details = [{
            "Part_No": obj[1],
            "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]
        print("post request in CP_CONTROL", request.POST)
        #print("post data",request.POST["part_no"],request.POST["rev_no"])
        print("cp_details", ln_cp_details)
        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Seq_No],[Process_Code],[Part_No],[Rev_No],[Serial_No],[Model],[Process_Status]) values (?,?,?,?,?,?,?,?,?,?,?)",
                tplno, fabno,
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"],process_seqno,
                "CP_CONTROL_PANEL", partno, revno,serialno,model, "c")
            cursor.commit()
            cursor.close()
            result = "data validated"
        else:
            result = "data not validated"
        print("result",result)

    if request.method == "POST" and "CP_COOLER" in request.POST["process"]:
        partno = request.POST["cooler_partno"]
        revno = request.POST["cooler_revno"]
        serialno = request.POST["cooler_serialno"]
        process_seqno = int(request.POST["process_seq_no"]) + 1

        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_COOLER'"""

        ln_cp_details = order_release_error_table = [{
            "Part_No": obj[1],
            "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]
        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Seq_No],[Process_Code],[Part_No],[Rev_No],[Serial_No],[Process_Status]) values (?,?,?,?,?,?,?,?,?,?)",
                tplno, fabno,
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"],process_seqno,
                "CP_COOLER", partno, revno, serialno, "c")
            cursor.commit()
            cursor.close()
            result = "data validated"
        else:
            result = "data not validated"

    if request.method == "POST" and "CP_BELT_DETAILS" in request.POST["process"]:
        partno = request.POST["beltdetails_partno"]
        revno = request.POST["beltdetails_revno"]
        batchone = request.POST["beltdetails_bone"]
        batchtwo = request.POST["beltdetails_btwo"]
        batchthree = request.POST["beltdetails_bthree"]
        make = request.POST["beltdetails_make"]
        process_seqno = int(request.POST["process_seq_no"]) + 1



        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_BELT_DETAILS'"""

        ln_cp_details = [{
            "Part_No": obj[1],
            "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]
        print("post request in CP_BELT_DETAILS", request.POST)
        #print("post data",request.POST["part_no"],request.POST["rev_no"])
        print("cp_details", ln_cp_details)
        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Seq_No],[Process_Code],[Part_No],[Rev_No],[BeltDetails_Batchone],[BeltDetails_Batchtwo],[BeltDetails_Batchthree],[BeltDetails_Make],[Process_Status]) values (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                tplno, fabno,
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"],process_seqno,
                "CP_BELT_DETAILS", partno, revno, batchone, batchtwo, batchthree, make,"c")
            cursor.commit()
            cursor.close()
            result = "data validated"
        else:
            result = "data not validated"
        print("result",result)

    if request.method == "POST" and "CP_DRIVE_PULLEY" in request.POST["process"]:
        partno = request.POST["drivepulley_partno"]
        revno = request.POST["drivepulley_revno"]
        serialno = request.POST["drivepulley_serialno"]
        process_seqno = int(request.POST["process_seq_no"]) + 1

        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_DRIVE_PULLEY'"""

        ln_cp_details = [{
            "Part_No": obj[1],
            "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]
        print("post request in CP_DRIVE_PULLEY", request.POST)
        # print("post data",request.POST["part_no"],request.POST["rev_no"])
        print("cp_details", ln_cp_details)
        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Seq_No],[Process_Code],[Part_No],[Rev_No],[Serial_No],[Process_Status]) values (?,?,?,?,?,?,?,?,?,?)",
                tplno, fabno,
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"], process_seqno,
                "CP_DRIVE_PULLEY", partno, revno, serialno, "c")
            cursor.commit()
            cursor.close()
            result = "data validated"
        else:
            result = "data not validated"
        print("result", result)

    if request.method == "POST" and "CP_DRIVEN_PULLEY" in request.POST["process"]:
        partno = request.POST["drivenpulley_partno"]
        revno = request.POST["drivenpulley_revno"]
        serialno = request.POST["drivenpulley_serialno"]
        process_seqno = int(request.POST["process_seq_no"]) + 1

        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_DRIVEN_PULLEY'"""

        ln_cp_details = [{
            "Part_No": obj[1],
            "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]
        print("post request in CP_BELT_DETAILS", request.POST)
        # print("post data",request.POST["part_no"],request.POST["rev_no"])
        print("cp_details", ln_cp_details)
        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Seq_No],[Process_Code],[Part_No],[Rev_No],[Serial_No],[Model],[Process_Status]) values (?,?,?,?,?,?,?,?,?,?,?)",
                tplno, fabno,
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"], process_seqno,
                "CP_DRIVEN_PULLEY", partno, revno, serialno, model, "c")
            cursor.commit()
            cursor.close()
            result = "data validated"
        else:
            result = "data not validated"
        print("result", result)

    if request.method == "POST" and "CP_DRYER" in request.POST["process"]:
        partno = request.POST["dryer_partno"]
        revno = request.POST["dryer_revno"]
        serialno = request.POST["dryer_serialno"]
        process_seqno = int(request.POST["process_seq_no"]) + 1

        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_DRYER'"""

        ln_cp_details = [{
            "Part_No": obj[1],
            "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]
        print("post request in CP_DRYER", request.POST)
        # print("post data",request.POST["part_no"],request.POST["rev_no"])
        print("cp_details", ln_cp_details)
        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Seq_No],[Process_Code],[Part_No],[Rev_No],[Serial_No],[Process_Status]) values (?,?,?,?,?,?,?,?,?,?)",
                tplno, fabno,
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"], process_seqno,
                "CP_DRYER", partno, revno, serialno, "c")
            cursor.commit()
            cursor.close()
            result = "data validated"
        else:
            result = "data not validated"
        print("result", result)

    if request.method == "POST" and "CP_FAN_MOTOR" in request.POST["process"]:
        partno = request.POST["fanmotor_partno"]
        revno = request.POST["fanmotor_revno"]
        serialno = request.POST["fanmotor_serialno"]
        kw = request.POST["fanmotor_kw"]
        process_seqno = int(request.POST["process_seq_no"]) + 1

        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_FAN_MOTOR'"""

        ln_cp_details = [{
            "Part_No": obj[1],
            "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]
        print("post request in CP_FAN_MOTOR", request.POST)
        # print("post data",request.POST["part_no"],request.POST["rev_no"])
        print("cp_details", ln_cp_details)
        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Seq_No],[Process_Code],[Part_No],[Rev_No],[Serial_No],[FANMOTOR_kw],[Process_Status]) values (?,?,?,?,?,?,?,?,?,?,?)",
                tplno, fabno,
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"], process_seqno,
                "CP_FAN_MOTOR", partno, revno, serialno,kw, "c")
            cursor.commit()
            cursor.close()
            result = "data validated"
        else:
            result = "data not validated"
        print("result", result)

    if request.method == "POST" and "CP_MOTOR" in request.POST["process"]:
        partno = request.POST["motor_partno"]
        revno = request.POST["motor_revno"]
        serialno = request.POST["motor_serialno"]
        motor_efficiency = request.POST["motor_efficiency"]
        process_seqno = int(request.POST["process_seq_no"]) + 1

        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_MOTOR'"""

        ln_cp_details = [{
            "Part_No": obj[1],
            "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]
        print("post request in CP_MOTOR", request.POST)
        # print("post data",request.POST["part_no"],request.POST["rev_no"])
        print("cp_details", ln_cp_details)
        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Seq_No],[Process_Code],[Part_No],[Rev_No],[Serial_No],[Motor_Efficency],[Process_Status]) values (?,?,?,?,?,?,?,?,?,?,?)",
                tplno, fabno,
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"], process_seqno,
                "CP_MOTOR", partno, revno, serialno,motor_efficiency, "c")
            cursor.commit()
            cursor.close()
            result = "data validated"
        else:
            result = "data not validated"
        print("result", result)

    if request.method == "POST" and "CP_NEURON" in request.POST["process"]:
        partno = request.POST["neuron_partno"]
        revno = request.POST["neuron_revno"]
        serialno = request.POST["neuron_serialno"]
        process_seqno = int(request.POST["process_seq_no"]) + 1

        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_NEURON'"""

        ln_cp_details = [{
            "Part_No": obj[1],
            "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]
        print("post request in CP_NEURON", request.POST)
        # print("post data",request.POST["part_no"],request.POST["rev_no"])
        print("cp_details", ln_cp_details)
        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Seq_No],[Process_Code],[Part_No],[Rev_No],[Serial_No],[Process_Status]) values (?,?,?,?,?,?,?,?,?,?)",
                tplno, fabno,
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"], process_seqno,
                "CP_NEURON", partno, revno, serialno, "c")
            cursor.commit()
            cursor.close()
            result = "data validated"
        else:
            result = "data not validated"
        print("result", result)

    if request.method == "POST" and "CP_VFD" in request.POST["process"]:
        partno = request.POST["vfd_partno"]
        revno = request.POST["vfd_revno"]
        serialno = request.POST["vfd_serialno"]
        process_seqno = int(request.POST["process_seq_no"]) + 1

        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_VFD'"""

        ln_cp_details = [{
            "Part_No": obj[1],
            "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]
        print("post request in CP_VFD", request.POST)
        # print("post data",request.POST["part_no"],request.POST["rev_no"])
        print("cp_details", ln_cp_details)
        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Seq_No],[Process_Code],[Part_No],[Rev_No],[Serial_No],[Process_Status]) values (?,?,?,?,?,?,?,?,?,?)",
                tplno, fabno,
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"], process_seqno,
                "CP_VFD", partno, revno, serialno, "c")
            cursor.commit()
            cursor.close()
            result = "data validated"
        else:
            result = "data not validated"
        print("result", result)

    if request.method == "POST" and "CP_TANK" in request.POST["process"]:
        partno = request.POST["tank_partno"]
        revno = request.POST["tank_revno"]
        serialno = request.POST["tank_serialno"]
        process_seqno = int(request.POST["process_seq_no"]) + 1

        ln_cp_details_query = """SELECT * FROM [TT].[dbo].[LN_CP_Details] WHERE Fab_Number='AVGC377434' AND Child_Part_Code = 'CP_TANK'"""

        ln_cp_details = [{
            "Part_No": obj[1],
            "Rev_No": obj[2],
        } for obj in cursor.execute(ln_cp_details_query)]
        print("post request in CP_TANK", request.POST)
        # print("post data",request.POST["part_no"],request.POST["rev_no"])
        print("cp_details", ln_cp_details)
        if revno == ln_cp_details[0]["Rev_No"] and partno == ln_cp_details[0]["Part_No"]:
            cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Seq_No],[Process_Code],[Part_No],[Rev_No],[Serial_No],[Process_Status]) values (?,?,?,?,?,?,?,?,?,?)",
                tplno, fabno,
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"], process_seqno,
                "CP_TANK", partno, revno, serialno, "c")
            cursor.commit()
            cursor.close()
            result = "data validated"
        else:
            result = "data not validated"
        print("result", result)

    if request.method == "POST" and "SUBMIT" in request.POST["process"]:

        process_seqno = int(request.POST["process_seq_no"]) + 1

        cursor.execute(
                "insert into [TT].[dbo].[Process_Update_Table] ([TPL_No],[Fab_No],[Emp_Name],[Emp_ID],[Process_Seq_No],[Process_Code],[SUBMIT],[Process_Status]) values (?,?,?,?,?,?,?,?)",
                tplno, fabno,
                employee_details_list[0]["Emp_Name"], employee_details_list[0]["Emp_ID"], process_seqno,
                "SUBMIT", "SUBMIT" ,"c")
        cursor.commit()
        cursor.close()
        result = "data validated"

    else:
        result = "data not validated"
    print("result", result)
    return result

def station20(request):
    return render(request,'stations/station20.html')

def alphalinesample(request):
    return render(request,'alphaline3.html')

###############################################

def pdi_master(request):
    cursor = db_connection()

    pdi_library_details = cursor.execute(
        "SELECT * FROM[TT].[dbo].[PDI_CL_Master]")

    pdi_library_data = [{
        "CL_Code": obj[0], "CL_Type_Code": obj[1], "Check_List_description": obj[2],
        "OK_Photo_Path": obj[3], "NOT_OK_Photo_Path": obj[4], "Check_point_delay": obj[5],
        "Sample_Image_Capture": obj[6], "Line_Code": obj[7], "Tack_Time": obj[8]
    } for obj in pdi_library_details]
    # print(pdi_master_data)

    pdi_master_details = cursor.execute(
        "SELECT * FROM [TT].[dbo].[PDI_CL_Map_Master]")

    pdi_master_data = [{
        "PMMKEY": obj[0], "Model_Code": obj[1], "PDI_CL_Code": obj[2], "Order_No": obj[3], "Line_Code": obj[4]
    } for obj in pdi_master_details]

    return render(request, 'pdi_master.html',
                  {"pdi_library_data": pdi_library_data, "pdi_master_data": pdi_master_data})




def torque_test(request):
    global conn
    print("connection ", conn)

    controller = client.write_register(28,1)
    # tool = client.write_register(29,1)
    # app = client.write_register(30,1)

    Torque = client.read_holding_registers(12017,1)
    Angle = client.read_holding_registers(12019,1) # D12019      - Angle
    Pass = client.read_holding_registers(20,1) # D12350      - Tool Pass
    Fail = client.read_holding_registers(21,1) # D12352      - Tool Fail
    Completed = client.read_holding_registers(22,1) # D12354      - Tool Completed
    Appmatch = client.read_holding_registers(23,1) # D12356      - Tool Appmatch
    Enable = client.read_holding_registers(24,1) # D12358      - Tool Enable
    online = client.read_holding_registers(25,1) # D12360      - Tool online
    Running = client.read_holding_registers(26,1) # D12362      - Tool Running
    # print("Torque    ",Torque.registers[0])
    # print("Angle     ",Angle.registers[0])
    # # print("Pass      ",Pass.registers)
    # # print("Fail      ",Fail.registers)
    # print("Completed ",Completed.registers)
    # print("Appmatch  ",Appmatch.registers)
    # print("Enable    ",Enable.registers)
    # print("online    ",online.registers)
    # print("Running   ",Running.registers)

    if Pass.registers[0] == 1:
        pf = "Pass"
    elif Fail.registers[0] == 1:
        pf = "Fail"
    else:
        pf = " "

    if Appmatch.registers[0] == 1:
        app = "App Matched"
    if Appmatch.registers[0] == 0:
        app = "App Not Matched"


    if Enable.registers[0] == 1:
        en_dis = "Enable"
    if Enable.registers[0] == 0:
        en_dis = "Disable"


    if online.registers[0] == 1:
        on_off = "Online"
    if online.registers[0] == 0:
        on_off = "Offline"

    if Running.registers[0] == 1:
        run_stop = "Running"
    if Running.registers[0] == 0:
        run_stop = "Stopped"


    print("torque ",Torque.registers)

    data = {"Offline":on_off,"App_Matched":app,"Disabled":en_dis,"Stopped":run_stop,"Pass":pf,"actual_torque":Torque.registers[0]/10}
    return render(request,'toolscreen.html',{"data":data})


