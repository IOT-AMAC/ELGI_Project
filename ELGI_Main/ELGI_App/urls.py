from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path('', views.demo_screen, name="demo_screen"),
    path('dashboard', views.dashboard, name="dashboard page"),
    path('company', views.company, name="company page"),
    path('breakdisplayconfiguration', views.break_display_configuration, name="break_display_configuration page"),
    path('holiday', views.holiday, name="holiday page"),
    path('message', views.message, name="message page"),
    path('messageconfiguration', views.message_configuration, name="messageconfiguration page"),
    path('shiftandbreak', views.shift_and_break, name="shift_and_break page"),
    path('stationbypass', views.station_bypass, name="station_bypass page"),
    path('toolmaintenance', views.tool_maintenance, name="tool_maintenance page"),
    path('tooltraceability', views.tool_traceability, name="tool_traceability page"),
    path('childpartdropdown', views.child_part_dropdown, name="child_part_dropdown page"),
    path('childpartdetails', views.child_part_details, name="child_part_details page"),
    path('orderrelease', views.order_release, name="order_release page"),
    path('orderreleaseerrortable', views.order_release_error_table, name="order_release_error_table page"),
    path('company', views.company, name="company page"),
    path('tplmaster', views.tpl_master, name="Tpl Master"),
    path('toolmaster', views.tool_master, name="Tool Master"),
    path('processmaster', views.process_master, name="Process Master"),
    path('employee', views.employee, name="Employee"),
    path('toolwarningmaster', views.tool_warning_master, name="Tool Warning Master"),
    path('packing', views.packing, name="Packing"),
    path('drivecouplingmaster', views.drive_coupling_master, name="Drive Coupling Master"),
    path('process', views.process, name="Process Screen development"),
    path('process_p', views.process_p, name="Process Screen development"),
    path('dmi', views.dmi, name="dmi"),
    path('login', views.login, name="login"),
    path('pdi', views.pdi, name="pdi"),
    path('testboothmaster', views.test_booth_master, name="Test Booth Master"),
    path('testcertificate1', views.test_certificate_1, name="Test Certificate 1"),
    path('testcertificate2', views.test_certificate_2, name="Test Certificate 2"),
    path('testcertificate3', views.test_certificate_3, name="Test Certificate 3"),
    path('testcertificate4', views.test_certificate_4, name="Test Certificate 4"),
    path('testcertificate5', views.test_certificate_5, name="Test Certificate 5"),
    path('testcertificate6', views.test_certificate_6, name="Test Certificate 6"),
    path('testcertificate7', views.test_certificate_7, name="Test Certificate 7"),
    path('testcertificate8', views.test_certificate_8, name="Test Certificate 8"),
    path('listoffabnumber', views.list_of_fab_number, name="List Of Fab Number"),
    path('scanfabnumber', views.scan_fab_number, name="Scan Fab Number"),
    path('starttest', views.start_test, name="Start Test"),
    path('pdi_2', views.pdi_2, name="pdi_2"),
    path('pdi_3', views.pdi_3, name="pdi_3"),

    path('reports', views.reports, name="reports"),
    path('compressprocessstatus', views.compressprocessstatus, name="compressprocessstatus"),
    path('lnserverstatus', views.lnserverstatus, name="lnserverstatus"),
    path('processstatus', views.processstatus, name="processstatus"),
    path('lnerpstatus', views.lnerpstatus, name="lnerpstatus"),
    path('tpldetails', views.tpldetails, name="tpldetails"),
    path('processsequence', views.processsequence, name="processsequence"),
    path('activetpllist/<str:tpl_code>/<str:operation_code>', views.active_tpl_list, name="activetpllist"),

    path('alphaline', views.alpha_line, name="alpha_line page"),
    path('station_order_release', views.station_order_release, name="station_order_release"),
    path('substation/<str:tplno>/<str:fabno>', views.substation, name="substation"),
    path('station20', views.station20, name="station20"),
    path('alphalinesample', views.alphalinesample, name="alphalinesample page"),


    path('torque', views.torque_test, name="torque_test_page"),
    # path('del_record/<str:db>/<str:uid>', views.del_record, name="del_record"),
#
]

if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
