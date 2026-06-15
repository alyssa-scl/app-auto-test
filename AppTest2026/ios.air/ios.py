# -*- encoding=utf8 -*-
__author__ = "邵翠玲"
import os
# 禁用 Android 相关检测
# os.environ['AIRTEST_NO_ADB'] = '1'
# os.environ['AIRTEST_NO_ANDROID'] = '1'

from airtest.core.api import *
from airtest.aircv import *
import time
import re
from airtest.report.report import LogToHtml
import unittest
import unittestreport

auto_setup(__file__)
from poco.drivers.ios import iosPoco
poco = iosPoco(auto_render_picture=False,screenshot_each_action=False)

def is_element_visible(element):
    """判断元素是否完全在屏幕内（无裁剪） 备用"""
    if not element.exists():
        return False
    
    try:
        bounds = element.get_bounds()
        if not bounds or len(bounds) < 4:
            return False
        
        # 获取屏幕尺寸
        screen_width, screen_height = device().get_current_resolution()
        
        # 解析bounds（假设格式为 [x, y, width, height] 像素单位）
        x, y, w, h = bounds
        # 判断是否完全在屏幕内
        return (x >= 0 and y >= 0 and 
                x + w <= screen_width and 
                y + h <= screen_height)
    except:
        return False
    return False
def add_device_page():
    for i in range(10):
        if poco("添加设备").exists():
            break
        else:
            if poco("iconFunctionNavBottonBack").exists():
                poco("iconFunctionNavBottonBack").click()
            if poco("Common nav back").exists():
                poco("Common nav back").click()
            sleep()            
def button_back(num):
    for i in range(num):
        if poco("iconFunctionNavBottonBack").exists():
            poco("iconFunctionNavBottonBack").click()
        if poco("Common nav back").exists():
            poco("Common nav back").click()            
def key_del(num):
    for i in range(num):
        text("\b", enter=False)
def gentle_reminder(is_agree=True):
    if is_agree:
        try:
            poco(name="同意", type="Button").click()
        except:
            pass
    else:
        try:
            poco(name="不同意", type="Button").click()
        except:
            pass

def InputBoxSetData(data="",btn=""):
    poco("TextField").click()
    data_len = len(poco("TextField").attr("value"))
    if data_len != 0:
        poco("清除文本").click()
    text(str(data),enter=False)
    poco(name="Done").click()
    poco(name=btn,type="Button").click()
    sleep()
def click_cell_switch(keyword, child_name):
    total_element = poco("Window").offspring("Table")
    cells = total_element.child("Cell")
    for i, cell in enumerate(cells):
        try:
            if cell.offspring(keyword).exists():
                cell.child(child_name).click()
                break
        except:
            continue   
def MyDeivice_page():
    for i in range(10):
        if poco("我的设备").exists() or poco("首页").exists():
            break
        else:
            poco("iconFunctionNavBottonBack").click()
            sleep()
def InMyDeivice_page():
    if poco(name="首页").exists():
        poco(name="所有设备").click()
        sleep()
    if poco("向左滑动即可删除设备。").exists():
        poco(name="确定").click()
    MyDeivice_page()
def Device_HomePage():
    sleep(10)
    popups = ["检查更新", "电池维护提醒"]
    close_btn = "iconGeneralOperationCloseBlack"
    for attempt in range(5):
        found = False
        for popup in popups:
            if poco(name=popup).exists():
                poco(close_btn).click()
                found = True
                sleep(2)
                break
        if not found:
            break
        sleep()
def DeviceConfig_page(name=""):
    Device_HomePage()
    poco("Common btn set").click()
    sleep()
def swipe_click_data(deviceSN=""):
    data_set = set() # 使用集合去重
    # 定义一个最大滚动次数，防止死循环
    max_swipes = 20 
    
    for i in range(max_swipes):
#        
        visible_items = poco(name=deviceSN,type="StaticText")
        if visible_items.exists():
            try:
                if is_element_visible(visible_items):
                    return visible_items
            except:
                pass
        if i < max_swipes - 1:
            poco.swipe([0.5, 0.5], [0.5, 0.3], duration=0.5)
            sleep(1.5)
        
    return None
def find_device_by_name(device_name=""):
    max_attempts = 20  # 最大尝试次数
    attempt = 0
    while attempt < max_attempts: 
        if poco(name=device_name).exists():
            devices = poco("Window").offspring("CollectionView").child("Cell")
            for index, device in enumerate(devices):
                try:
                    name_element = device.offspring(device_name).get_name()
                    if device_name == name_element:
                        print(f"找到设备 '{device_name}' 在索引 {index}，返回{device}")
                        return {'index':index,'name':device_name,'element':device}
                except Exception as e:
                    print(f"检查设备索引{index}中出错：{e}")
                    continue
            break
        else:
            poco("CollectionView").swipe([0.5, 0.5], [0.5, 0.3], duration=0.5)
            sleep()
            attempt += 1
            continue
def move_slider_to(bar_id,min_id,max_id,value_id,*data):
    # 可能会出现滑动数值偏差问题，后期优化
    slider_pos = poco(bar_id).get_position()  # [x,y]
    slider_size = poco(bar_id).get_size() # [w,h]
    min_range = int(re.search(r"(\d+)[%AV]",poco(min_id).get_text()).group(1))
    max_range = int(re.search(r"(\d+)[%AV]",poco(max_id).get_text()).group(1))    
    total_range = max_range - min_range
    margin_ratio = 0.001
    absolute_left_x = slider_pos[0] - (slider_size[0] / 2)
    real_start_x = absolute_left_x + (slider_size[0] * margin_ratio)
    real_track_width = slider_size[0] * (1 - margin_ratio * 2)
    value_text = poco(value_id).get_text()
    val = re.findall(r"\d+(?=[%AV])",value_text)
    if "-" in value_text:
        min_val = int(val[0])
        max_val = int(val[1])
        print("data:",data)
        left_start_x =  real_start_x + real_track_width * ((min_val - min_range)/total_range)
        left_target_x = real_start_x + real_track_width * ((data[0] - min_range)/total_range)
        right_start_x =  real_start_x + real_track_width * ((max_val - min_range)/total_range)
        right_target_x = real_start_x + real_track_width * ((data[1] - min_range)/total_range)
        poco.swipe([left_start_x,slider_pos[1]],[left_target_x,slider_pos[1]],duration=2.0) 
        sleep()
        poco.swipe([right_start_x,slider_pos[1]],[right_target_x,slider_pos[1]],duration=2.0) 
    else:
        value = int(val[0])
        start_x =  real_start_x + real_track_width * ((value - min_range)/total_range)
        target_x = real_start_x + real_track_width * ((data[0] - min_range)/total_range)
        poco.swipe([start_x,slider_pos[1]],[target_x,slider_pos[1]],duration=2.0)
def network_config(pwd=""):
    if poco("更换网络").exists():
        poco("更换网络").click()
    poco("SecureTextField").click()
    text(pwd,enter=False)
    poco(name="Done").click()
    if poco("提交").exists():
        poco("提交").click()
        sleep(10)
    elif poco("提交配置").exists():
        poco("提交配置").click()
        sleep(15)
    if poco(name="更新", type="Button").exists():
        poco(name="更新", type="Button").click()
    try:
        poco("已联网").wait_for_appearance(timeout=60)
        poco("已连接").wait_for_appearance(timeout=120)
        poco("下一步").wait(timeout=30).click()
    except Exception as e:
        print(f"网络配置-等待超时或出现错误：{e}")
def add_device(is_manual=True,model="",deviceSN="",name="",network_pwd="DLcs2023"):
    poco("添加设备").click()
    sleep()
    if poco("我知道了").exists():
        poco("我知道了").click()
    if is_manual:
        poco("手动添加设备").click()
        poco("TextField").click()
        text(deviceSN,enter=False)
        poco(name="Done").click()
        poco("确定").click()
        sleep()
    else:
        element = swipe_click_data(deviceSN)
        element.click()
        poco(name="确定",type="Button").click()
        sleep(3)
    if poco("iconGeneralOperationCloseBlack").exists():
        poco("iconGeneralOperationCloseBlack").click()
    if poco(name="配置网络").exists():
        network_config(network_pwd) # 默认配置DLCSASUS网络
    if poco("绑定成功").exists():
        InputBoxSetData(name,"开始使用设备")
def del_device(name=""):
    InMyDeivice_page()
    device = find_device_by_name(name)
    device['element'].swipe(direction="left", duration=0.3)
    poco(name="iconGeneralOperationDeleteWhit").click()
    poco(name="确定",type="Button").click()
def _connect_more(name="",operation=""):
    if operation == "云端" or operation == "蓝牙":
        poco(name=name).click()
    elif operation == "更换网络" or operation == "固件升级":
        device = find_device_by_name(name)
        device['element'].offspring("iconGeneralOperationEllipsisBl").click()
        poco(name=operation).click()
    
#     if poco(name="主图风格设置").exists():
#         theme_style_set()
    if poco(name="同意").exists():
        gentle_reminder()    
def Bluetooth_connect_pwd(pwd=""):
    poco(name="蓝牙连接密码").click()
    if pwd == "":
        if poco(name="不设密码").exists():
            poco(name="不设密码").click()
            poco(name="确定",type="Button").click()
        if poco(name="请输入6位英文或数字密码。").exists():
            poco("iconGeneralOperationCloseBlack").click()
    else:
        if poco(name='重置密码').exists():
            poco(name='重置密码').click()
        if poco("请输入6位英文或数字密码。").exists():
            poco("Window").child("Other")[1].child("Other")[1].child("Other")[1].offspring("SecureTextField").click()
            text(pwd,enter=False)
            poco(name="Done").click()
            poco("Window").child("Other")[1].child("Other")[1].child("Other")[2].offspring("SecureTextField").click()
            text(pwd,enter=False)
            poco(name="Done").click()
            poco(name="确定",type="Button").click()
def Bluetooth_device(deviceSN="",pwd=""):
    if not poco(name="蓝牙直连").exists():
        poco.swipe([0.5, 0.2], [0.5, 0.8],duration=0.5)
        sleep()
    poco(name="蓝牙直连").click()
    gentle_reminder()
    if poco(name="说明").exists():
        poco(name="我知道了",type="Button").click()
    poco("TextField").click()
    data_len = len(poco("TextField").attr("value"))
    if data_len != 0:
        poco("清除文本").click()
    text(deviceSN,enter=False)
    poco(name="Search").click()
    sleep(3)
    poco(name=deviceSN).click()
    if poco(name="蓝牙连接密码").exists():
        InputBoxSetData(pwd,"确定")
    sleep()
def Default_Connect_Method(method=1):
    poco(name="默认连接方式").click()
    if method:
        poco(name="云端").click()
    else:
        poco(name="蓝牙").click()
def RestoreFactorySet():
    poco.swipe([0.5,0.5],[0.5,0.3],duration=1.5)
    poco(name="高级设置").click()
    poco(name="恢复出厂设置").click()
    poco(name="确定").click()
def CarbonEmissionCoefficient_config(factor):
    poco(name="碳排量系数").click()
    if factor == 0.959:
        if poco(name="Done").exists():
            poco(name="Done").click()
        poco(name="重置").click()
    else:
        InputBoxSetData(factor, "设置")
def VisitorControlAuthor_config(is_open = 1):
    poco(name="访客控制授权").click()
    if is_open:
        click_cell_switch('访客控制授权',"Common switch nor")
        poco(name="确定",type="Button").click()
    else:
        click_cell_switch('访客控制授权',"Common switch nor")
    button_back(1)
def DisasterWarning_config(is_open = 1):
    poco(name="灾害预警").click() 
    if is_open:
        if poco(name="灾害预警已关闭").exists():
            poco(name="Common switch nor").click() 
    else:
        if poco(name="灾害预警已开启").exists():
            poco(name="Common switch nor").click() 
def StrongmanMode_config(is_open = 1):
    poco(name="大力士模式").click()
    if is_open:
        click_cell_switch('大力士模式',"Common switch nor")
#         sleep(2)
#         poco(name="iconGeneralContentHighPowerModeyellow",type="Image").click()
    else:
        click_cell_switch('大力士模式',"Common switch nor")
#         button_back(1)
#         sleep(3)
#         if not poco(name="iconGeneralContentHighPowerModeyellow",type="Image").exists():
#             print("大力士模式关闭成功")
def WorkingMode_config(mode=1,soc_list=None,time_periods=None,offset=120):
    poco(name="工作模式").click()
    if mode == 1:
        target_name = "标准UPS" if poco(name="标准UPS").exists() else "备用电源"
        poco(name=target_name).click()
        sleep(0.5)
    elif mode == 2:
        target_name = "PV优先UPS" if poco(name="PV优先UPS").exists() else "自发自用"
        poco(name=target_name).click()
        sleep(0.5)
        poco(name="SOC设置").click()
#         move_slider_to(slider_bar_id,5,100,soc_val_id,soc_list)
        button_back(1)
    elif mode == 3:
        target_name = "时间控制UPS" if poco(name="时间控制UPS").exists() else "定时充放电"
        poco(name=target_name).click()
    else:
        target_name = "自定义UPS" if poco(name="自定义UPS").exists() else "自定义"
        poco(name=target_name).click()
def ChargingMode_config(mode = 0, current = 3):
    poco(name="充电模式").click()
    if mode == 0:
        poco(name="标准").click()
    elif mode == 1:
        poco(name="静音").click()
    elif mode == 2:
        poco(name="快充").click()
    else:
        poco(name="自定义").click()
        sleep()
        poco("iconGeneralArrowChevronRight").click()
        InputBoxSetData(current,"确定")
def ECOSet_config(is_ac_eco=1):
    poco(name="ECO").click()
    sleep()
    select_l = ["1h","2h","3h","4h"]
    if is_ac_eco:
        if not poco(name="AC-ECO关机时间").exists():
            click_cell_switch('AC-ECO',"Common switch nor")
        for i in range(len(select_l)):
            poco(name="AC-ECO关机时间").click()
            poco(name=select_l[i]).click()
            sleep()
            poco(name="AC-ECO功率设置").click()
            power = 10 * (i + 1)
            InputBoxSetData(power,"确定")
    else:
        if not poco(name="DC-ECO关机时间").exists():
            click_cell_switch('DC-ECO',"Common switch nor")
        for i in range(len(select_l)):
            poco(name="DC-ECO关机时间").click()
            poco(name=select_l[i]).click()
            sleep()
            poco(name="DC-ECO功率设置").click()
            power = 5 * (i + 1)
            InputBoxSetData(power,"确定")
def ScreenSleepTime_config():
    poco(name="屏幕休眠时间").click()
    select_l = ["30秒","1分钟","5分钟","常亮"]
    for i in range(len(select_l)):
        poco(name=select_l[i]).click()
        sleep()
        if i < len(select_l) - 1:
            poco(name="屏幕休眠时间").click()
    sleep(2)
def TimerSwitch(task_type,target="05"):
    poco(name="定时开关").click()
    if task_type == "DC":
        poco(name=task_type).click()
        poco(name="添加").click()
        picker = poco("Window").offspring("Table").offspring("Picker").child("PickerWheel")[0]
        picker.swipe([0.5,0.5],[0.5,0.4],duration=0.5)
        sleep(0.2)

deviceName = "AORA300"
deviceModel = "AORA300"
deviceSN = "AORA3002612110001164"
network_password = "DLcs2023"
bluetooth_con_pwd = "123456"
new_device_name = "AORA300-1164@test20"
# 如果需要跳过某些用例的话再对应方法的上方加上 @unittest.skip("跳过")
# 若其中用例失败的话，可屏蔽其他用例 单独跑失败的用例
class TestHomePage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
    
#     @unittest.skip("跳过")
#     def test01_manually_add_del_device(self):
#         self._testMethodDoc = "验证添加设备，默认配置DLCSASUS网络"
#         add_device_page()
#         add_device(True,deviceModel,deviceSN,deviceName,network_password)
#     def test02_RestoreFactorySet(self):
#         self._testMethodDoc = "恢复出厂初始化设置"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         RestoreFactorySet()
#     @unittest.skip("跳过")    
#     def test03_BluetoothDirectConnect_not_pwd(self):
#         self._testMethodDoc = "验证蓝牙直连功能-无密码"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         Bluetooth_connect_pwd("")
#     def test04_BluetoothDirectConnect_input_pwd(self):
#         self._testMethodDoc = "验证蓝牙直连功能-有密码"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         Bluetooth_connect_pwd(bluetooth_con_pwd)
#     def test05_DefaultConnectMethod_Bluetooth(self):
#         self._testMethodDoc = "验证默认连接方式功能-蓝牙"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         Default_Connect_Method(0)
#         button_back(2)
#         _connect_more(deviceName,"蓝牙")
#     def test06_DefaultConnectMethod_Cloud(self):
#         self._testMethodDoc = "验证默认连接方式功能-云端"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         Default_Connect_Method()
#         button_back(2)
#         sleep()
#         _connect_more(deviceName,"云端")
#     def test07_CarbonEmissionCoefficient_Set(self):
#         self._testMethodDoc = "验证碳排量系数配置功能-设置"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         CarbonEmissionCoefficient_config(1.2)
#     def test08_CarbonEmissionCoefficient_Reset(self):
#         self._testMethodDoc = "验证碳排量系数配置功能-重置"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         CarbonEmissionCoefficient_config(0.959)
#     def test09_VisitorControlAuthorization_Close(self):
#         self._testMethodDoc = "验证访客控制授权功能-关闭"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         VisitorControlAuthor_config(0)
    
#     def test10_VisitorControlAuthorization(self):
#         self._testMethodDoc = "验证访客控制授权功能-打开"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         VisitorControlAuthor_config()
#     def test11_DisasterWarning_Open(self):
#         self._testMethodDoc = "验证灾害预警功能-打开"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         DisasterWarning_config()

#     def test12_DisasterWarning_Close(self):
#         self._testMethodDoc = "验证灾害预警功能-关闭"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         DisasterWarning_config(0)

    def test13_StrongmanMode_Open(self):
        self._testMethodDoc = "验证大力士模式功能-打开"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        StrongmanMode_config(1)

    def test14_StrongmanMode_Close(self):
        self._testMethodDoc = "验证大力士模式功能-关闭"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        StrongmanMode_config(0)

#     def test15_WorkingMode_standard(self):
#         self._testMethodDoc = "验证工作模式功能-标准UPS-备用电源"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         WorkingMode_config(1)
#         button_back(1)  
#     def test16_WorkingMode_PVPriority(self):
#         self._testMethodDoc = "验证工作模式功能-PV优先UPS-自发自用"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         WorkingMode_config(2,64) # 64为soc值

#     def test17_WorkingMode_TimeControlled(self):
#         self._testMethodDoc = "验证工作模式功能-时间控制UPS-定时充放电"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         WorkingMode_config(3,64) # 64为soc值
#     def test18_WorkingMode_Customed(self):
#         self._testMethodDoc = "验证工作模式功能-自定义UPS-自定义"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         WorkingMode_config(4,64) # 64为soc值
    def test19_ChargingMode_standard(self):
        self._testMethodDoc = "验证充电模式设置功能-标准-mode=0"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ChargingMode_config(0)
    def test20_ChargingMode_mute(self):
        self._testMethodDoc = "验证充电模式设置功能-静音-mode=1"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ChargingMode_config(1)
    def test21_ChargingMode_fastcharging(self):
        self._testMethodDoc = "验证充电模式设置功能-快充-mode=2"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ChargingMode_config(2)
    def test22_ChargingMode_customize(self):
        self._testMethodDoc = "验证充电模式设置功能-自定义-mode=3"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ChargingMode_config(3,6)
    def test23_ECOSetAC(self):
        self._testMethodDoc = "验证AC-ECO设置功能-设置关机时间1/2/3/4h-功率10-40W"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ECOSet_config(1)
    def test24_ECOSetDC(self):
        self._testMethodDoc = "验证DC-ECO设置功能-设置关机时间1/2/3/4h-功率5-20W"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ECOSet_config(0)
    def test25_ScreenSleepTime(self):
        self._testMethodDoc = "验证屏幕休眠时间功能-30秒/1分钟/5分钟/常亮"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ScreenSleepTime_config()
#     def test33_TimerSwitch_DC(self):
#         self._testMethodDoc = "验证定时开关-DC"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         TimerSwitch("DC")

def load_suite():
    loaderer = unittest.TestLoader()
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestHomePage)
    suite = unittest.TestSuite([suite1])
    return suite

suite = load_suite()
runner = unittestreport.TestRunner(suite)
runner.run()

