# import Test_1


def Test_1():
    print("starting test_1")
    print("'WiFi_Connect' import and 'sync_time' start === >>>>>>>>>>>>>>>>>>>>")
    from wifi_connect import wifi_connect_time_sync, sync_time

    wifi_connect_time_sync()
    print("'WiFi_Connect' import and 'sync_time' end   === <<<<<<<<<<<<<<<<<<<<")
    print("1 @ 10")
    print("test_1 complate")


Test_1()
