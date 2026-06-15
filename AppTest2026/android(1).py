# -*- encoding=utf8 -*-
__author__ = "邵翠玲"

from airtest.core.api import *
from airtest.aircv import *
import time
import re
import logging
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)
from airtest.report.report import LogToHtml
import unittest
import unittestreport

auto_setup(__file__,logdir=True)
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

PACKAGE_NAME = "net.poweroak.bluetticloud.debug"

def swipe_up(target_text="",id=""):
    max_attempts = 20  # 最大尝试次数
    attempt = 0
    while attempt < max_attempts:
        if poco(text=target_text).exists():
            poco(text=target_text).click()
            sleep()
            break
        else:
            poco("android.widget.ScrollView").focus([0.5, 0.9]).swipe([0,-0.5])
            sleep()
            attempt += 1
            continue
#首次安装打开APP
def operation_before_login(is_agree=True):
    if is_agree:
        try:
            poco(text="允许").click()
            poco(text="跳过").click()
        except:
            pass
    else:
        try:
            poco(text="不允许").click()
        except:
            pass

#登录后温馨提示
def gentle_reminder(is_agree=True):
    if is_agree:
        try:
            poco(text="同意").click()
        except:
            pass
    else:
        try:
            poco(text="不同意").click()
        except:
            pass

def sure_or_option(is_sure=True):
    if is_sure:
        try:
            poco(text="确定").click()
        except:
            pass
    else:
        try:
            poco(text="取消").click()
        except:
            pass        

def allow_or_option(is_allow=True):
    if is_allow:
        try:
            poco(text="允许").click()
        except:
            pass
    else:
        try:
            poco(text="不允许").click()
        except:
            pass  
def theme_style_set(theme_style=0):
    if theme_style:
        try:
            poco(text="确定").click()
        except:
            pass
    else:
        try:
            poco(f"{PACKAGE_NAME}:id/iv_img_scene").click()
            poco(text="确定").click()
        except:
            pass
#判断是否在一级页面，否则返回一级页面
def main_page():
    for i in range(10):
        if poco(text="首页").exists():
            break
        else:
            keyevent("BACK")#keyevent返回上一级
            sleep()
            
def login_page():
    for i in range(10):
        if poco(text="登录/注册").exists():
            break
        else:
            keyevent("BACK")#keyevent返回上一级
            sleep()
def poco_offsprings(parent,*subsets):
    try:
        element = poco(parent)
        for subset in subsets:
            element = element.offspring(subset)
        return element
    except:
        return None

def MyDeivice_page():
    for i in range(10):
        if poco(text="我的设备").exists() or poco(text="首页").exists():
            break
        else:
            keyevent("BACK")#keyevent返回上一级
            sleep()
def InMyDeivice_page():
    if poco(text="首页").exists():
        poco(text="所有设备").click()
        sleep()
    if poco(text="向左滑动即可删除设备。").exists():
        poco(text="确定").click()
    MyDeivice_page()
def InputBoxSetData(id_text="",data="",btn_id=""):
    if f"{PACKAGE_NAME}:id" in id_text:
        poco(id_text).click()
        data_len = len(poco(id_text).get_text())
    else:
        poco(text=id_text).click()
        data_len = len(poco(text=id_text).get_text())
    if data_len != 0:
        key_del(data_len)
    text(str(data))
    poco(btn_id).click()
    sleep()

def move_slider_to(bar_id,min_id,max_id,value_id,*data):
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
def parse_time_range(time_str):
    """解析时间字符串 'HHMM-HHMM' 格式"""
    start, end = time_str.split("-")
    start_hour = int(start[:2])
    start_min = int(start[-2:])
    end_hour = int(end[:2])
    end_min = int(end[-2:])
    return start_hour, start_min, end_hour, end_min
def single_time_picker(hour,minutes,offset=120):
    hour_pos = poco(f"{PACKAGE_NAME}:id/wv_hour").get_position() #获取时间控件的中心点坐标
    min_pos = poco(f"{PACKAGE_NAME}:id/wv_min").get_position()
    screen_width, screen_height = device().get_current_resolution() # 获取当前手机屏幕分辨率
    hour_x = hour_pos[0] * screen_width
    hour_y = hour_pos[1] * screen_height
    min_x = min_pos[0] * screen_width
    min_y = min_pos[1] * screen_height
    swipe((hour_x,hour_y),(hour_x,hour_y-offset*hour),duration=0.3)
    swipe((min_x,min_y),(min_x,min_y-offset*minutes),duration=0.3)
    
def double_time_picker(start_hour,start_min,end_hour,end_min,mark_time=None,offset=120):
    start_hour_pos = poco(f"{PACKAGE_NAME}:id/wv_start_hour").get_position() #获取时间控件的中心点坐标
    start_min_pos = poco(f"{PACKAGE_NAME}:id/wv_start_min").get_position()
    end_hour_pos = poco(f"{PACKAGE_NAME}:id/wv_end_hour").get_position() #获取时间控件的中心点坐标
    screen_width, screen_height = device().get_current_resolution() # 获取当前手机屏幕分辨率
    start_hour_x = start_hour_pos[0] * screen_width
    start_hour_y = start_hour_pos[1] * screen_height
    start_min_x = start_min_pos[0] * screen_width
    start_min_y = start_min_pos[1] * screen_height
    end_hour_x = end_hour_pos[0] * screen_width
    end_hour_y = end_hour_pos[1] * screen_height
    if mark_time != f"{start_hour}:{start_min}":
        swipe((start_hour_x,start_hour_y),(start_hour_x,start_hour_y-offset*start_hour),duration=0.3)
        swipe((start_min_x,start_min_y),(start_min_x,start_min_y-offset*start_min),duration=0.3)
    swipe((end_hour_x,end_hour_y),(end_hour_x,end_hour_y+offset*(23-end_hour)),duration=0.3)
    sleep(0.5)
    end_min_pos = poco(f"{PACKAGE_NAME}:id/wv_end_min").get_position()
    end_min_x = end_min_pos[0] * screen_width
    end_min_y = end_min_pos[1] * screen_height
    if end_hour != 23:
        swipe((end_min_x,end_min_y),(end_min_x,end_min_y-offset*end_min),duration=0.3)
    else:
        swipe((end_min_x,end_min_y),(end_min_x,end_min_y+offset*(59-end_min)),duration=0.3)
def charge_discharge_time_set(time_periods,offset=120):
    last_end_time = None
    for period in time_periods:
        time_list = list(period.values())[0]
        period_type = list(period.keys())[0]
        start_hour, start_min, end_hour, end_min = parse_time_range(time_list)
        if poco(text="00:00-23:59").exists():
            poco(text="00:00-23:59").click()
        if poco(text=f"{last_end_time}-23:59").exists():
            poco(text=f"{last_end_time}-23:59").click()
        double_time_picker(start_hour,start_min,end_hour,end_min,last_end_time,offset)
        if period_type == "充电":
            poco(f"{PACKAGE_NAME}:id/kvv_charging").click()
        else:
            poco(f"{PACKAGE_NAME}:id/cl_discharging").click()
        poco(text="确定").click()
        poco(text=time_list).wait_for_appearance(timeout=10)
        last_end_time = f"{end_hour:02d}:{end_min:02d}"
def _connect_more(name="",operation=""):
    if poco(text="首页").exists():
        device = find_device_by_name(f"{PACKAGE_NAME}:id/rv_device",name)
        device['element'].offspring(f"{PACKAGE_NAME}:id/iv_action").click()
    else:
        device = find_device_by_name(f"{PACKAGE_NAME}:id/rv_device_list",name)
        device['element'].offspring(f"{PACKAGE_NAME}:id/iv_action").click()
    if operation == "云端":
        poco(text=operation).click()
    elif operation == "蓝牙":
        poco(text=operation).click()
    elif operation == "更换网络":
        poco(text=operation).click()
    elif operation == "固件升级":
        poco(text=operation).click()
    
    if poco(text="主图风格设置").exists():
        theme_style_set()
    if poco(text="同意").exists():
        gentle_reminder()
        allow_or_option()    
    sleep(2)
    
def Device_HomePage(name=""):
    sleep()
    popups = ["检查更新", "电池维护提醒"]
    close_btn = f"{PACKAGE_NAME}:id/iv_close"
    for attempt in range(5):
        found = False
        for popup in popups:
            if poco(text=popup).exists():
                poco(close_btn).click()
                found = True
                sleep(0.5)
                break
        if not found:
            break
        sleep()
def DeviceConfig_page(name=""):
    Device_HomePage(name)
    poco(f"{PACKAGE_NAME}:id/tvRight").click()
    sleep()
    for i in range(10):
        if poco(text="设置").exists():
            break
        else:
            keyevent("BACK")#keyevent返回上一级
            sleep()
        
def add_device_page():
    for i in range(10):
        if poco(text="添加设备").exists():
            break
        else:
            keyevent("BACK")#keyevent返回上一级
            sleep()            
def button_back(num):
    for i in range(num):
        if poco(f"{PACKAGE_NAME}:id/imgLeft").exists():
            poco(f"{PACKAGE_NAME}:id/imgLeft").click()

def key_del(num):
    for i in range(num):
        keyevent("KEYCODE_DEL")
        
def is_refresh(refresh=False):
    if refresh:
        try:
            poco(text="确定").click()
        except:
            pass
    else:
        try:
                poco(text="取消").click()
        except:
            pass
        
def swipe_click_data(item_id,deviceSN=""):
    """
    滚动获取并定位列表数据
    :param item_id: 列表项中文本控件的 resourceId (如 'com.bluetti:id/name')
    :return: 所有数据的列表
    """
    data_set = set() # 使用集合去重
    
    # 定义一个最大滚动次数，防止死循环
    max_swipes = 20 
    
    for i in range(max_swipes):
#        
        visible_items = poco(item_id)
        
        if not visible_items.exists():
            print("当前页面没有找到列表项")
            break
        
        if poco(text=deviceSN).exists():
            element = poco(text=deviceSN)
            return element
        
        if i < max_swipes - 1:
            poco.swipe([0.5, 0.6], [0.5, 0.3], duration=1.0)
            sleep(1.5)
        
    return None

def get_all_devices(resourceId):
    device_list = poco(resourceId)
    if not device_list.exists():
        print("设备列表不存在")
        return []
    # 获取所有设备项（假设每个设备是一个ViewGroup）
    devices = device_list.child("android.view.ViewGroup")
    if devices:
        return devices

def find_device_by_name(resourceId,device_name=""):
    max_attempts = 20  # 最大尝试次数
    attempt = 0
    while attempt < max_attempts:
        if poco(textMatches=f".*{device_name}.*").exists():
            devices = get_all_devices(resourceId)
            for index, device in enumerate(devices):
                try:
                    name_element = device.offspring(type="android.widget.TextView")
                    if name_element.exists():
                        device_text = name_element.get_text()
                    if device_name in device_text:
                        print(f"找到设备 '{device_name}' 在索引 {index}，返回{device}")
                        return {'index':index,'name':device_name,'element':device}
                except Exception as e:
                    print(f"检查设备索引{index}中出错：{e}")
                    continue
            break
        else:
            poco("android.widget.ScrollView").focus([0.5, 0.9]).swipe([0,-0.2])
            sleep()
            attempt += 1
            continue          
def get_all_device_datas(resourceId):
    # 根据名称查找设备
    devices = get_all_devices(resourceId)
    data_lists = []
    for index, device in enumerate(devices):
        try:
            name_element = device.offspring(type="android.widget.TextView")
            device_text = name_element.get_text()
            data_lists.append({'index':index,'name':device_text,'element':device})
        except Exception as e:
            print(f"检查设备索引{index}中出错：{e}")
            continue
    return data_lists 

def login(email="ho@qq.com", password="123456"):
    login_page()
    poco(text="登录/注册").click()
    try:
        poco(text="请输入邮箱").click()
        poco(text="请输入邮箱").set_text(email)
        poco(text="请输入登录密码").click()
        if poco(text='不用了').exists():
            poco(text='不用了').click()
        sleep()
        text(password)
    except:
        email_text = poco_offsprings(f"{PACKAGE_NAME}:id/xedt_email",f"{PACKAGE_NAME}:id/edt_content").get_text()
        password_text = poco_offsprings(f"{PACKAGE_NAME}:id/xedt_password",f"{PACKAGE_NAME}:id/edt_content").get_text()
        if email_text != None:
            poco(text=email_text).click()
            key_del(len(email_text))
            text(email)
        if password_text != None:
            poco(text=password_text).click()
            key_del(len(password_text))
            text(password)
        else:
            poco(text="请输入登录密码").click()
            if poco(text="不用了").exists():
                poco(text="不用了").click()
            text(password)
    finally:
        poco(f"{PACKAGE_NAME}:id/check_user_agreement").click()
        poco(text="登录").click()
        sleep(2)
        if poco(textMatches=".*温馨提示.*").exists():
            poco(text="同意").click()
            target_ui2 = poco(textMatches=".*设备排序.*")
            target_ui2.wait_for_appearance(timeout=5)
            poco(text="好的").click()

def network_config(pwd=""):
    if poco(text="更换网络").exists():
        poco(text="更换网络").click()
#     elif poco(text="网络配置").exists():
#         poco(text="网络配置").click()
    if poco(text="仅在使用该应用时允许").exists():
        poco(text="仅在使用该应用时允许").click()
    poco(text="请输入Wi-Fi密码").click()
    text(pwd)
    if poco(text="提交").exists():
        poco(text="提交").click()
    elif poco(text="提交配置").exists():
        poco(text="提交配置").click()
    try:
        poco(text="已联网").wait_for_appearance(timeout=60)
        poco(text="已连接").wait_for_appearance(timeout=120)
        poco(text="确定").wait(timeout=30).click()
    except Exception as e:
        print(f"网络配置-等待超时或出现错误：{e}")
def multiple_network_config(wifi1_name="",wifi1_pwd="",wifi2_name="",wifi2_pwd="",wifi3_name="",wifi3_pwd=""):
    pass
def add_device(is_manual=True,model="",deviceSN="",name="",network_pwd="DLcs2023"):
    poco(f"{PACKAGE_NAME}:id/swipe_refresh").swipe([0.0307, -0.1617])
    sleep()
    poco(text="添加设备").click()
    sleep()
    if is_manual:
        poco(text="手动添加").click()
        InputBoxSetData("请输入设备类型+SN码",deviceSN,f"{PACKAGE_NAME}:id/btn_confirm")
        sleep(2)
        if poco(text="绑定失败").exists():
            fail_text = poco(f"{PACKAGE_NAME}:id/tv_message").get_text()
#             print(f'提示文字：{fail_text}')
            poco(text="确定").click()
            return
    else:
        element = swipe_click_data(f"{PACKAGE_NAME}:id/device_name",deviceSN)
        element.click()
        poco(text="确定").click()
        sleep(2)
        if poco(text="绑定失败").exists():
            poco(text="确定").click()
    if poco(text="网络配置").exists() and poco(text="没有联网").exists():
        network_config(network_pwd) # 默认配置DLCSASUS网络
    if poco(text="添加成功").exists():
        InputBoxSetData(model,name,f"{PACKAGE_NAME}:id/btn_action")
        sleep(2)
        
def del_device(name=""):
    InMyDeivice_page()
    device = find_device_by_name(f"{PACKAGE_NAME}:id/rv_device_list",name)
    device['element'].swipe([-0.5612, 0.0013])
    poco(f"{PACKAGE_NAME}:id/right_menu").click()
    poco(text="确定").click()

def Default_Connect_Method(method=1):
    swipe_up('默认连接方式')
    if method:
        poco(text="云端").click()
    else:
        poco(text="蓝牙").click()
           
def Bluetooth_connect_pwd(pwd=""):
    swipe_up('蓝牙连接密码')
    if poco(text='不用了').exists():
        poco(text='不用了').click()
    if pwd == "":
        if poco(text='新密码').exists():
            poco(f"{PACKAGE_NAME}:id/iv_close").click()
        if poco(text="不设密码").exists():
            poco(text="不设密码").click()
            poco(text="确定").click()
    else:
        if poco(text='重置密码').exists():
            poco(text='重置密码').click()
            if poco(text='不用了').exists():
                poco(text='不用了').click()
        if poco(text='新密码').exists():
            poco(text='新密码').click()
            if poco(text='不用了').exists():
                poco(text='不用了').click()
            text(pwd)
            sleep()
            poco(text='确认新密码').click()
            if poco(text='不用了').exists():
                poco(text='不用了').click()
            text(pwd)
            sleep()
            poco(text='确定').click()
def CarbonEmissionCoefficient_config(factor):
    swipe_up('碳排量系数')
    if factor == 0.959:
        poco(text="重置").click()
    else:
        InputBoxSetData(f"{PACKAGE_NAME}:id/edt_value",factor,f"{PACKAGE_NAME}:id/btn_set")

def VisitorControlAuthor_config(is_open = 1):
    swipe_up('访客控制授权')
    if is_open:
        poco_offsprings(f"{PACKAGE_NAME}:id/item_guest_mode",f"{PACKAGE_NAME}:id/ivEnd").click()
        poco(f"{PACKAGE_NAME}:id/btn_positive").click()
    else:
        poco_offsprings(f"{PACKAGE_NAME}:id/item_guest_mode",f"{PACKAGE_NAME}:id/ivEnd").click()    
#     sleep(2)
def WorkingMode_config(mode=1,soc_list=None,time_periods=None,offset=120):
    swipe_up('工作模式')
    slider_bar_id= f"{PACKAGE_NAME}:id/seek_bar_soc"
    soc_min_id= f"{PACKAGE_NAME}:id/tv_soc_min"
    soc_max_id= f"{PACKAGE_NAME}:id/tv_soc_max"
    soc_val_id= f"{PACKAGE_NAME}:id/tv_soc_value"
    if mode == 1:
        poco_offsprings(f"{PACKAGE_NAME}:id/cl_backup",f"{PACKAGE_NAME}:id/ivEnd").click()
        sleep(0.5)
    elif mode == 2:
        poco_offsprings(f"{PACKAGE_NAME}:id/cl_self",f"{PACKAGE_NAME}:id/ivEnd").click()
        sleep(0.5)
        poco_offsprings(f"{PACKAGE_NAME}:id/cl_self",f"{PACKAGE_NAME}:id/kvv_self_soc").click()
        move_slider_to(slider_bar_id,soc_min_id,soc_max_id,soc_val_id,soc_list)
        button_back(1)
    elif mode == 3:
        poco_offsprings(f"{PACKAGE_NAME}:id/cl_scheduled",f"{PACKAGE_NAME}:id/ivEnd").click()
        sleep(0.5)
        poco_offsprings(f"{PACKAGE_NAME}:id/cl_scheduled",f"{PACKAGE_NAME}:id/kvv_scheduled_soc").click()
        move_slider_to(slider_bar_id,soc_min_id,soc_max_id,soc_val_id,*soc_list)
        sleep()
        button_back(1)
        poco(text="时间设置").click()
        poco(f"{PACKAGE_NAME}:id/imgRight").click()
        poco(f"{PACKAGE_NAME}:id/btn_delete_all").click()
        poco(f"{PACKAGE_NAME}:id/btn_positive").click()
        sleep(0.5)
        poco(text="00:00-23:59").wait_for_appearance(timeout=30)
        charge_discharge_time_set(time_periods,offset)      
    else:
        poco_offsprings(f"{PACKAGE_NAME}:id/cl_custom",f"{PACKAGE_NAME}:id/ivEnd").click()
        sleep(0.5)
        poco_offsprings(f"{PACKAGE_NAME}:id/cl_custom",f"{PACKAGE_NAME}:id/kvv_custom_soc").click()
        move_slider_to(slider_bar_id,soc_min_id,soc_max_id,soc_val_id,*soc_list)
        sleep()
        button_back(1)
        if not poco(text="时间设置").exists():
            poco_offsprings(f"{PACKAGE_NAME}:id/item_custom_ctrl",f"{PACKAGE_NAME}:id/ivEnd").click()
        poco(text="时间设置").click()
        poco(f"{PACKAGE_NAME}:id/imgRight").click()
        poco(f"{PACKAGE_NAME}:id/btn_delete_all").click()
        poco(f"{PACKAGE_NAME}:id/btn_positive").click()
        sleep(0.5)
        poco(text="00:00-23:59").wait_for_appearance(timeout=30)
        charge_discharge_time_set(time_periods,offset)
        
def DisasterWarning_config(is_open = 1):
    swipe_up('灾害预警')
    if is_open:
        if poco(text="灾害预警已关闭").exists():
            poco(f"{PACKAGE_NAME}:id/sv_enable_status").click() 
#             sleep(0.5)
    else:
        if poco(text="灾害预警已开启").exists():
            poco(f"{PACKAGE_NAME}:id/sv_enable_status").click() 
#             sleep(0.5)
        
def ChargingMode_config(mode = 0, current = 3):
    swipe_up('充电模式')
    if mode == 0:
        poco(text="标准").click()
        sleep(0.5)
        poco(text="标准").exists()
    elif mode == 1:
        poco(text="静音").click()
        sleep(0.5)
        poco(text="静音").exists()
    elif mode == 2:
        poco(text="快充").click()
        sleep(0.5)
        poco(text="快充").exists()
    else:
        poco(text="自定义").click()
        poco(f"{PACKAGE_NAME}:id/tv_value").click()
        InputBoxSetData(f"{PACKAGE_NAME}:id/edt_value",current,f"{PACKAGE_NAME}:id/btn_set")
        button_back(1)
        poco(text="自定义").exists()
def StrongmanMode_config(is_open = 1):
    swipe_up('大力士模式')
    if is_open:
        poco_offsprings(f"{PACKAGE_NAME}:id/item_power_lifting",f"{PACKAGE_NAME}:id/ivEnd").click()
        button_back(1)
#         poco(f"{PACKAGE_NAME}:id/iv_power_lifting_mode").wait_for_appearance(timeout=10)
#         poco(f"{PACKAGE_NAME}:id/iv_power_lifting_mode").click()
    else:
        poco_offsprings(f"{PACKAGE_NAME}:id/item_power_lifting",f"{PACKAGE_NAME}:id/ivEnd").click()
        button_back(1)
#         sleep(3)
#         if not poco(f"{PACKAGE_NAME}:id/iv_power_lifting_mode").exists():
#             print("大力士模式关闭成功")
def ECOSet_config(is_ac_eco=1):
    swipe_up('ECO')
    sleep()
    select_l = ["1h","2h","3h","4h"]
    if is_ac_eco:
        if not poco(text="AC-ECO 关机时间").exists():
            poco_offsprings(f"{PACKAGE_NAME}:id/ll_ac_eco",f"{PACKAGE_NAME}:id/ivEnd").click()
        for i in range(len(select_l)):
            poco(text="AC-ECO 关机时间").click()
            poco(text=select_l[i]).click()
            sleep()
            poco(text="AC-ECO 功率设置").click()
            power = 10 * (i + 1)
            InputBoxSetData(f"{PACKAGE_NAME}:id/edt_value",power,f"{PACKAGE_NAME}:id/btn_set")
    else:
        if not poco(text="DC-ECO 关机时间").exists():
            poco_offsprings(f"{PACKAGE_NAME}:id/ll_dc_eco",f"{PACKAGE_NAME}:id/ivEnd").click()
        for i in range(len(select_l)):
            poco(text="DC-ECO 关机时间").click()
            poco(text=select_l[i]).click()
            sleep()
            poco(text="DC-ECO 功率设置").click()
            power = 5 * (i + 1)
            InputBoxSetData(f"{PACKAGE_NAME}:id/edt_value",power,f"{PACKAGE_NAME}:id/btn_set")
    sleep(2)
def ScreenSleepTime_config():
    swipe_up('屏幕休眠时间')
    select_l = ["30秒","1分钟","5分钟","常亮"]
    for i in range(len(select_l)):
        poco(text=select_l[i]).click()
        sleep()
        if i < len(select_l) - 1:
            poco(text="屏幕休眠时间").click()
    sleep()
def ChildLockSwitch(is_open="",level=""):
    swipe_up('童锁开关')
    if poco(text="立即体验").exists():
        poco(text="立即体验").click()
    if is_open == "启用":
        poco(text=is_open).click()
        sleep()
        if level == "等级一":
            poco_offsprings(f"{PACKAGE_NAME}:id/kvv_level1",f"{PACKAGE_NAME}:id/iv_icon_right").click()
        else:
            poco_offsprings(f"{PACKAGE_NAME}:id/kvv_level2",f"{PACKAGE_NAME}:id/iv_icon_right").click()
        sleep()
    else:
        poco(text=is_open).click()
        sleep()
def TimerSwitch(task_type,time_lists,offset=120):
    swipe_up('定时开关')
    if poco(text="好的").exists():
        poco(text="好的").click()
    if task_type == "DC":
        poco(text="DC").wait_for_appearance(timeout=2)
        poco(f"{PACKAGE_NAME}:id/rv_time_switch").child(f"{PACKAGE_NAME}:id/kvv_item")[0].offspring(f"{PACKAGE_NAME}:id/loading_switch_view").click()
        sleep()
        poco(f"{PACKAGE_NAME}:id/rv_time_switch").child(f"{PACKAGE_NAME}:id/kvv_item")[0].click()
    else:
        poco(text="AC").wait_for_appearance(timeout=2)
        poco(f"{PACKAGE_NAME}:id/rv_time_switch").child(f"{PACKAGE_NAME}:id/kvv_item")[1].offspring(f"{PACKAGE_NAME}:id/loading_switch_view").click()
        sleep()
        poco(f"{PACKAGE_NAME}:id/rv_time_switch").child(f"{PACKAGE_NAME}:id/kvv_item")[1].click()
    if not poco(text="没有数据").exists(): 
        poco(f"{PACKAGE_NAME}:id/imgRight").click()
        poco(f"{PACKAGE_NAME}:id/tv_check_all").click()
        poco(f"{PACKAGE_NAME}:id/btn_del").click()
        poco(f"{PACKAGE_NAME}:id/btn_positive").click()
        sleep(3)  
    for period in time_lists:
        poco(text="添加").click()
        poco(text=period.get('status')).click()
        week_list = period.get('week').split(',')
        time_list = period.get('time').split(':')
        poco(f"{PACKAGE_NAME}:id/kvv_select_week").click()
        poco(text="周一").click()
        for day in week_list:
            poco(text=day).click()
        sleep()
        poco(f"{PACKAGE_NAME}:id/btn_positive").click()
        single_time_picker(int(time_list[0]),int(time_list[1]),offset)
        poco(f"{PACKAGE_NAME}:id/btn_confirm").click()
        if poco(text="开启后将禁用ECO功能").exists():
            poco(text="确定").click()
        sleep()
def _wait_upgrade_success(success_text, timeout):
    try:
        poco(text=success_text).wait_for_appearance(timeout=timeout)
        poco(f"{PACKAGE_NAME}:id/btn_positive").click()
    except:
        raise
def FirmwareUpdate(update_type=""):
    swipe_up('固件升级')
    poco(text="IOT").wait_for_appearance(timeout=20)
    if update_type == "IOT":
        if poco(f"{PACKAGE_NAME}:id/btn_upgrade").exists():
            poco(f"{PACKAGE_NAME}:id/btn_upgrade").click()
            poco(text="确定").click()
            _wait_upgrade_success("IOT 升级成功",240)
    else:
        if poco(text="系统升级").exists():
            poco(text="系统升级").click()
        if update_type == "BOOT升级":
            poco(text=update_type,type="android.widget.Button").wait_for_appearance(timeout=20)
            poco(text=update_type,type="android.widget.Button").click()
            poco(text="确定").click()
            _wait_upgrade_success("升级成功", 600)
        else:
            upgrade_options = [("一键升级", "升级成功"),("系统升级", "升级成功")]
            for option_text, success_text in upgrade_options:
                if poco(text=option_text,type="android.widget.Button").exists():
                    poco(text=option_text,type="android.widget.Button").wait_for_appearance(timeout=20)
                    poco(text=option_text,type="android.widget.Button").click()
                    poco(text="确定").click()
                    _wait_upgrade_success(success_text, 600)          
def DCInputSource(source_type=""):
    swipe_up('高级设置')
    poco(f"{PACKAGE_NAME}:id/kvv_dc_input_source").click()
    if source_type == "PV":
        poco(f"{PACKAGE_NAME}:id/item_pv").click()
        sleep(0.5)
        poco_offsprings(f"{PACKAGE_NAME}:id/item_adv_mode",f"{PACKAGE_NAME}:id/ivEnd").click()
        sleep()
        poco(f"{PACKAGE_NAME}:id/edt_confirm_input").click()
        text("Y",enter=False)
        poco(f"{PACKAGE_NAME}:id/btn_positive").click()
        sleep()
    else:
        poco(f"{PACKAGE_NAME}:id/kvv_other").click()
        sleep(0.5)
    button_back(2)
def ACOutputFrequency(frequency=""):
    swipe_up('高级设置')
    poco(f"{PACKAGE_NAME}:id/kvv_output_frequency").click()
    poco(text=frequency).click()
    button_back(1)
def SystemSwitchMemory(is_open="",pwd=""):
    swipe_up('高级设置')
    poco(f"{PACKAGE_NAME}:id/kvv_power_auto_ctrl").click()
    poco(text=is_open).click()
    if is_open == "启用":
        poco(text="同意").click()
        if poco(text='不用了').exists():
            poco(text='不用了').click()
        poco(f"{PACKAGE_NAME}:id/edt_password").click()
        text(pwd,enter=False)
        poco(text="确定").click()
        sleep()
    button_back(1)
def MaxInputPowerGrid(current):
    swipe_up("高级设置")
    poco(f"{PACKAGE_NAME}:id/ll_settings_grid").click()
    slider_bar_id= f"{PACKAGE_NAME}:id/seek_bar"
    tv_min_id= f"{PACKAGE_NAME}:id/tv_min"
    tv_max_id= f"{PACKAGE_NAME}:id/tv_max"
    tv_val_id= f"{PACKAGE_NAME}:id/tv_value"
    if not poco(slider_bar_id).exists():
        poco_offsprings(f"{PACKAGE_NAME}:id/item_adv",f"{PACKAGE_NAME}:id/ivEnd").click()
        poco(text="同意").click()
        if poco(text='不用了').exists():
            poco(text='不用了').click()
        if poco(text="密码").exists():
            poco(f"{PACKAGE_NAME}:id/edt_password").click()
            text("88888888",enter=False)
            poco(f"{PACKAGE_NAME}:id/btn_login").click()
            sleep()
    move_slider_to(slider_bar_id,tv_min_id,tv_max_id,tv_val_id,current)
    poco(f"{PACKAGE_NAME}:id/btn_confirm").click()
    if poco(f"{PACKAGE_NAME}:id/tv_title").get_text() == "温馨提示":
        poco(f"{PACKAGE_NAME}:id/btn_positive").click()
    sleep()
def SleepModeSet(is_open="",soc=0):
    swipe_up("高级设置")
    poco(f"{PACKAGE_NAME}:id/kvv_sleep_mode").click()
    slider_bar_id= f"{PACKAGE_NAME}:id/seek_bar"
    tv_min_id= f"{PACKAGE_NAME}:id/tv_min"
    tv_max_id= f"{PACKAGE_NAME}:id/tv_max"
    tv_val_id= f"{PACKAGE_NAME}:id/tv_value"
    if is_open == "启用":
        poco(f"{PACKAGE_NAME}:id/tv_on").click()
        move_slider_to(slider_bar_id,tv_min_id,tv_max_id,tv_val_id,soc)
        sleep()
        button_back(3)
        poco(f"{PACKAGE_NAME}:id/iv_power").click()
        poco(f"{PACKAGE_NAME}:id/kvv_sleep_mode").click()
        poco(f"{PACKAGE_NAME}:id/btn_positive").click()
        sleep(12)
        title = poco(f"{PACKAGE_NAME}:id/tv_title").get_text()
        if title == "已休眠":
            poco(f"{PACKAGE_NAME}:id/iv_power").click()
            sleep(6)
    else:
        poco(f"{PACKAGE_NAME}:id/tv_off").click() 
def MaxChargingLimitSet(soc_num):
    swipe_up('高级设置')
    poco(f"{PACKAGE_NAME}:id/kvv_soc_high_limited").click()
    if poco(text="我知道了").exists():
        poco(text="我知道了").click()
    if soc_num == 85:
        poco(f"{PACKAGE_NAME}:id/view_point1").click()
    elif soc_num == 90:
        poco(f"{PACKAGE_NAME}:id/view_point2").click()
    elif soc_num == 95:
        poco(f"{PACKAGE_NAME}:id/view_point3").click()
    else:
        poco("net.poweroak.bluetticloud.debug:id/cl_sticking_point").click()
    sleep()
def RestoreFactorySet():
    swipe_up('高级设置')
    poco(f"{PACKAGE_NAME}:id/btn_factory_reset").click()
    poco(f"{PACKAGE_NAME}:id/btn_confirm").click()
def AdaptiveModeOfWeak(is_open=0,undervol_param=[80,3],highpress_param=[113,3],underfreq_param=[3.3,1],overfreq_param=[3.3,1]):
    swipe_up('高级设置')
    poco(f"{PACKAGE_NAME}:id/kvv_grid_self_adaption").click()
    if is_open:
        InputBoxSetData("电网欠压保护值",undervol_param[0],f"{PACKAGE_NAME}:id/btn_set")
        InputBoxSetData("电网欠压保护时间",undervol_param[1],f"{PACKAGE_NAME}:id/btn_set")
        InputBoxSetData("电网高压保护值",highpress_param[0],f"{PACKAGE_NAME}:id/btn_set")
        InputBoxSetData("电网高压保护时间",highpress_param[1],f"{PACKAGE_NAME}:id/btn_set")
        poco("android.widget.ScrollView").focus([0.5, 0.5]).swipe([0,-0.5])
        InputBoxSetData("电网欠频保护值",underfreq_param[0],f"{PACKAGE_NAME}:id/btn_set")
        InputBoxSetData("电网欠频保护时间",underfreq_param[1],f"{PACKAGE_NAME}:id/btn_set")
        InputBoxSetData("电网过频保护值",overfreq_param[0],f"{PACKAGE_NAME}:id/btn_set")
        InputBoxSetData("电网过频保护时间",overfreq_param[1],f"{PACKAGE_NAME}:id/btn_set")
        poco("android.widget.ScrollView").focus([0.5, 0.5]).swipe([0,0.5])
        poco(f"{PACKAGE_NAME}:id/tv_on").click()
        sleep()
    else:
        poco(f"{PACKAGE_NAME}:id/tv_off").click()
        sleep()
def AboutDevicePage(model="",deviceSN=""):
    swipe_up('关于设备')
    if poco(text="说明").exists():
        poco(text="确定").click()
    SN = poco_offsprings(f"{PACKAGE_NAME}:id/kvv_sn",f"{PACKAGE_NAME}:id/tv_value").get_text()
    model_text = poco(f"{PACKAGE_NAME}:id/tv_device_model").get_text()
    if deviceSN == SN and model == model_text:
        return True
def ModifyDeviceName(deviceName=""):
    poco(f"{PACKAGE_NAME}:id/iv_device_name_edit").click()
    poco(f"{PACKAGE_NAME}:id/edt_new_device_name").click()
    old_name = poco(f"{PACKAGE_NAME}:id/edt_new_device_name").get_text()
    key_del(len(old_name))
    text(deviceName)
    poco(f"{PACKAGE_NAME}:id/btn_set").click()
    sleep(2)
    new_name = poco(f"{PACKAGE_NAME}:id/tv_device_name").get_text()
    if new_name == deviceName:
        poco(f"{PACKAGE_NAME}:id/iv_device_name_edit").click()
        poco(f"{PACKAGE_NAME}:id/edt_new_device_name").click()
        key_del(len(new_name))
        text(old_name)
        poco(f"{PACKAGE_NAME}:id/btn_set").click()
        sleep(2)
        button_back(1)
        sleep()
#     if poco(f"{PACKAGE_NAME}:id/tvTitle").get_text() == new_name:
#         button_back(1)
        
def Bluetooth_device(deviceSN="",pwd=""):
    if not poco(text="蓝牙直连").exists():
        poco(f"{PACKAGE_NAME}:id/swipe_refresh").swipe([0.0307, -0.1617])
        sleep()
    poco(text="蓝牙直连").click()
    gentle_reminder()
    allow_or_option()
    if poco(text="说明").exists():
        poco(text="我知道了").click()
    element = swipe_click_data(f"{PACKAGE_NAME}:id/device_name",deviceSN)
    element.click()
    sleep(10)
    if poco(text="蓝牙连接密码").exists():
        poco(text="请输入密码").click()
        text(pwd)
        poco(text="确定").click()
    sleep()
    
# 提前登录即可 若要测试登录，把该值改为False
_global_logged_in = True
def ensure_login():
    global _global_logged_in
    if not _global_logged_in:
        operation_before_login()
        sleep()
        login("ho@qq.com","123456")
        sleep(2)
        gentle_reminder()
        is_refresh()
        _global_logged_in = True
    else:
        pass

deviceName = "AORA300"
deviceModel = "AORA300"
deviceSN = "AORA3002612110001164"
network_password = "DLcs2023"
bluetooth_con_pwd = "123456"
new_device_name = "AORA300-test20" 
time_offset = 120 # 这个值主要是用于工作模式/定时开关的时间选择上偏差，每台设备可能不一样
# 如果需要跳过某些用例的话再对应方法的上方加上 @unittest.skip("跳过")，也可ctrl+/注释掉用例。
# 若其中用例失败的话，可屏蔽其他用例 单独跑失败的用例。
# 访客授权控制需在测试之前都开启，否则会报错，设计缘故是因为可以都测试到打开和关闭，看后期使用情况也可做调整根据实际情况打开或关闭。
# 最好设备的电源较为充足以及设备数据默认的情况下测试,列表页的设备名称不能有相同的否则无法找到
class TestHomePage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
        
#     @unittest.skip("跳过")
    def test01_manually_add_del_device(self):
        self._testMethodDoc = "验证手动添加设备，并删除-默认配置DLCSASUS网络"
        add_device_page()
        sure_or_option()
        allow_or_option()
        add_device(True,deviceModel,deviceSN,deviceName,network_password)
        del_device(deviceName)
        
#     @unittest.skip("跳过")
    def test02_manually_addNotExist_device(self):
        self._testMethodDoc = "验证手动添加不存在的设备"
        add_device_page()
        sure_or_option()
        allow_or_option()
        add_device(True,"EL300","EL3002532344009705")
        
#     @unittest.skip("跳过")
    def test03_manually_addBound_device(self):
        self._testMethodDoc = "验证手动添加其他账号绑定的设备"
        add_device_page()
        sure_or_option()
        allow_or_option()
        add_device(True,"EL300","EL3002532000009700")
        
#     @unittest.skip("跳过")
    def test04_swipe_add_device(self):
        self._testMethodDoc = "验证拖动列表选定添加设备-默认配置DLCSASUS网络"
        add_device_page()
        sure_or_option()
        allow_or_option()
        add_device(False,deviceModel,deviceSN,deviceName,network_password)
    
    def test05_RestoreFactorySet(self):
        self._testMethodDoc = "恢复出厂初始化设置"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        RestoreFactorySet()
        button_back(3)
    def test06_BluetoothDirectConnect_not_pwd(self):
        self._testMethodDoc = "验证蓝牙直连功能-无密码"
        InMyDeivice_page()
        _connect_more(deviceName,"蓝牙")
        DeviceConfig_page(deviceName)
        Bluetooth_connect_pwd("")
        button_back(3)
        Bluetooth_device(deviceSN,'')
        button_back(2)   
    def test07_BluetoothDirectConnect_input_pwd(self):
        self._testMethodDoc = "验证蓝牙直连功能-有密码"
        InMyDeivice_page()
        _connect_more(deviceName,"蓝牙")
        DeviceConfig_page(deviceName)
        Bluetooth_connect_pwd(bluetooth_con_pwd)
        button_back(3)
        Bluetooth_device(deviceSN,bluetooth_con_pwd)
        button_back(2)
    
    def test08_DefaultConnectMethod_Bluetooth(self):
        self._testMethodDoc = "验证默认连接方式功能-蓝牙"
        InMyDeivice_page()
        _connect_more(deviceName,"蓝牙")
        DeviceConfig_page(deviceName)
        Default_Connect_Method(0)
        button_back(2)
        _connect_more(deviceName,"蓝牙")
        Device_HomePage()
        button_back(1)  
    
    def test09_DefaultConnectMethod_Cloud(self):
        self._testMethodDoc = "验证默认连接方式功能-云端"
        InMyDeivice_page()
        _connect_more(deviceName,"蓝牙")
        DeviceConfig_page(deviceName)
        Default_Connect_Method()
        button_back(2)
        _connect_more(deviceName,"云端")
        Device_HomePage()
        button_back(1)
    
    def test10_CarbonEmissionCoefficient_Set(self):
        self._testMethodDoc = "验证碳排量系数配置功能-设置"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        CarbonEmissionCoefficient_config(1.2)
        button_back(2) 
    
    def test11_CarbonEmissionCoefficient_Reset(self):
        self._testMethodDoc = "验证碳排量系数配置功能-重置"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        CarbonEmissionCoefficient_config(0.959)
        button_back(2)
    
    def test12_VisitorControlAuthorization_Close(self):
        self._testMethodDoc = "验证访客控制授权功能-关闭"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        VisitorControlAuthor_config(0)
#         button_back(3)
#         Bluetooth_device(deviceSN,bluetooth_con_pwd)
#         Device_HomePage()
#         poco(f"{PACKAGE_NAME}:id/tvRight").click()
#         if poco(text="温馨提示").exists():
#             poco(text="我知道了").click()
#         button_back(2)
    
    def test13_VisitorControlAuthorization(self):
        self._testMethodDoc = "验证访客控制授权功能-打开"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        VisitorControlAuthor_config()
#         button_back(3)
#         Bluetooth_device(deviceSN,bluetooth_con_pwd)
#         Device_HomePage()
#         poco(f"{PACKAGE_NAME}:id/tvRight").click()
#         if poco(text="设置").exists():
#             button_back(3)
    
    def test14_DisasterWarning_Open(self):
        self._testMethodDoc = "验证灾害预警功能-打开"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        DisasterWarning_config()
        button_back(3)
    
    def test15_DisasterWarning_Close(self):
        self._testMethodDoc = "验证灾害预警功能-关闭"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        DisasterWarning_config(0)
        button_back(3)
    
    def test16_ChargingMode_standard(self):
        self._testMethodDoc = "验证充电模式设置功能-标准-mode=0"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ChargingMode_config(0)
        button_back(2)
    
    def test17_ChargingMode_mute(self):
        self._testMethodDoc = "验证充电模式设置功能-静音-mode=1"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ChargingMode_config(1)
        button_back(2) 
    
    def test18_ChargingMode_fastcharging(self):
        self._testMethodDoc = "验证充电模式设置功能-快充-mode=2"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ChargingMode_config(2)
        button_back(2)
    
    def test19_ChargingMode_customize(self):
        self._testMethodDoc = "验证充电模式设置功能-自定义-mode=3"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ChargingMode_config(3,3)
        button_back(2)
    def test20_StrongmanMode_Open(self):
        self._testMethodDoc = "验证大力士模式功能-打开"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        StrongmanMode_config(1)
        button_back(1)
    def test21_StrongmanMode_Close(self):
        self._testMethodDoc = "验证大力士模式功能-关闭"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        StrongmanMode_config(0)
        button_back(1)
    def test22_ECOSetAC(self):
        self._testMethodDoc = "验证AC-ECO设置功能-设置关机时间1/2/3/4h-功率10-40W"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ECOSet_config(1)
        button_back(3)
    def test23_ECOSetDC(self):
        self._testMethodDoc = "验证DC-ECO设置功能-设置关机时间1/2/3/4h-功率5-20W"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ECOSet_config(0)
        button_back(3)  
    def test24_ScreenSleepTime(self):
        self._testMethodDoc = "验证屏幕休眠时间功能-30秒/1分钟/5分钟/常亮"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ScreenSleepTime_config()
        button_back(2)      
#     def test25_ChildLockSwitch_enable1(self):
#         self._testMethodDoc = "验证童锁开关-启用-等级一"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         ChildLockSwitch("启用","等级一")
#         button_back(3)
#     def test26_ChildLockSwitch_enable2(self):
#         self._testMethodDoc = "验证童锁开关-启用-等级二"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         ChildLockSwitch("启用","等级二")
#         button_back(3)
#     def test27_ChildLockSwitch_disenable(self):
#         self._testMethodDoc = "验证童锁开关-停用"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         ChildLockSwitch("停用")
#         button_back(3)
    def test28_WorkingMode_standard(self):
        self._testMethodDoc = "验证工作模式功能-标准UPS-备用电源"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        WorkingMode_config(1)
        button_back(3) 
    def test29_WorkingMode_PVPriority(self):
        self._testMethodDoc = "验证工作模式功能-PV优先UPS-自发自用"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        WorkingMode_config(2,64) # 64为soc值
        button_back(3)
    def test30_WorkingMode_TimeControlled(self):
        self._testMethodDoc = "验证工作模式功能-时间控制UPS-定时充放电"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        # [31,70]为soc范围值,时间设置范围值需合理否则报错
        WorkingMode_config(3,[31,70],[{"充电":"15:10-18:40"}],time_offset)
        button_back(3)
    def test31_WorkingMode_Customed(self):
        self._testMethodDoc = "验证工作模式功能-自定义UPS-自定义"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        # [30,65]为soc范围值,时间设置范围值需合理否则报错
        WorkingMode_config(4,[41,50],[{"放电":"12:10-23:02"}],time_offset)
        button_back(3)
#     def test32_SingleWiFiConfig(self):
#         self._testMethodDoc = "验证单个WiFi网络配置功能-设备不支持多WiFi-默认使用DLCSASUS"
#         InMyDeivice_page()
#         _connect_more(deviceName,"更换网络")
#         network_config(network_password)
#         sleep(5)
    def test33_TimerSwitch_DC(self):
        self._testMethodDoc = "验证定时开关-DC"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        TimerSwitch("DC",[{'status':'启用','week':'周一','time':'12:20'}],time_offset)
        button_back(4)  
    def test34_TimerSwitch_AC(self):
        self._testMethodDoc = "验证定时开关-AC"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        TimerSwitch("AC",[{'status':'停用','week':'周一','time':'15:45'}],time_offset)
        button_back(4)
    def test35_DCInputSource_PV(self):
        self._testMethodDoc = "验证高级设置-直流输入源-PV"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        DCInputSource("PV")
        button_back(3)
    def test36_DCInputSource_Other(self):
        self._testMethodDoc = "验证高级设置-直流输入源-其他"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        DCInputSource("Other")
        button_back(3)
    def test37_ACOutputFrequency_50Hz(self):
        self._testMethodDoc = "验证高级设置-交流电输出频率-50Hz"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ACOutputFrequency("50Hz")
        button_back(2)
    def test38_ACOutputFrequency_60Hz(self):
        self._testMethodDoc = "验证高级设置-交流电输出频率-60Hz"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ACOutputFrequency("60Hz")
        button_back(2)
    def test39_SystemSwitchMemory_enable(self):
        self._testMethodDoc = "验证高级设置-系统开关机记忆-启用"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        SystemSwitchMemory("启用","88888888")
        button_back(2)
    def test40_SystemSwitchMemory_disenable(self):
        self._testMethodDoc = "验证高级设置-系统开关机记忆-停用"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        SystemSwitchMemory("停用")
        button_back(2)
    def test41_MaxInputPowerGrid(self):
        self._testMethodDoc = "验证高级设置-电网最大输入电流"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        MaxInputPowerGrid(5)
        button_back(3)
#     def test42_SleepModeSet_enable(self):
#         self._testMethodDoc = "验证高级设置-休眠模式-启用"
#         InMyDeivice_page()
#         _connect_more(deviceName,"蓝牙")
#         DeviceConfig_page(deviceName)
#         SleepModeSet("启用",1)
#         sleep(5)
#     def test43_SleepModeSet_disenable(self):
#         self._testMethodDoc = "验证高级设置-休眠模式-停用"
#         InMyDeivice_page()
#         _connect_more(deviceName,"蓝牙")
#         DeviceConfig_page(deviceName)
#         SleepModeSet("停用")
#         button_back(3)
    def test44_MaxChargingLimitSet(self):
        self._testMethodDoc = "验证高级设置-充电上限设置"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        MaxChargingLimitSet(90)
        button_back(3)
#     def test45_FirmwareUpdate_Cloud_IOT(self):
#         self._testMethodDoc = "验证固件升级云端-IOT"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         FirmwareUpdate("IOT")
#     def test46_FirmwareUpdate_Bluetooth_IOT(self):
#         self._testMethodDoc = "验证固件升级蓝牙-IOT"
#         InMyDeivice_page()
#         _connect_more(deviceName,"蓝牙")
#         DeviceConfig_page(deviceName)
#         FirmwareUpdate("IOT")
#         sleep(60)
#     def test47_FirmwareUpdate_Cloud_System(self):
#         self._testMethodDoc = "验证固件升级云端-系统升级"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         FirmwareUpdate("系统升级")
#         sleep(3)
#     def test48_FirmwareUpdate_Bluetooth_System(self):
#         self._testMethodDoc = "验证固件升级蓝牙-系统升级"
#         InMyDeivice_page()
#         _connect_more(deviceName,"蓝牙")
#         DeviceConfig_page(deviceName)
#         FirmwareUpdate("系统升级")
#         sleep(3)
#     def test49_FirmwareUpdate_Cloud_BOOT(self):
#         self._testMethodDoc = "验证固件升级云端-BOOT升级"
#         InMyDeivice_page()
#         _connect_more(deviceName,"云端")
#         DeviceConfig_page(deviceName)
#         FirmwareUpdate("BOOT升级")
#         sleep(3)
#     def test50_FirmwareUpdate_Bluetooth_BOOT(self):
#         self._testMethodDoc = "验证固件升级蓝牙-BOOT升级"
#         InMyDeivice_page()
#         _connect_more(deviceName,"蓝牙")
#         DeviceConfig_page(deviceName)
#         FirmwareUpdate("BOOT升级")
#         sleep(3)
    def test51_AboutDevice(self):
        self._testMethodDoc = "验证关于设备页"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        AboutDevicePage(deviceName,deviceSN)
        button_back(3) 
    def test52_ModifyDeviceName(self):
        self._testMethodDoc = "验证修改设备名称"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        ModifyDeviceName(new_device_name) 
    def test53_AdaptiveModeOfWeak_Stop(self):
        self._testMethodDoc = "验证弱电网自适应模式-停用默认"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        AdaptiveModeOfWeak()
        button_back(3)
    def test54_AdaptiveModeOfWeak_Open(self):
        self._testMethodDoc = "验证弱电网自适应模式-启用"
        InMyDeivice_page()
        _connect_more(deviceName,"云端")
        DeviceConfig_page(deviceName)
        # 第1个参数：启用，第2个参数：欠压参数，第3个参数：高压参数，第4个参数：欠频参数，第5个参数：过频参数
        AdaptiveModeOfWeak(1,[85,5],[110,5],[3.4,3],[3.5,2])
#         button_back(3)

def load_suite():
    loaderer = unittest.TestLoader()
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestHomePage)
    suite = unittest.TestSuite([suite1])
    return suite

suite = load_suite()
runner = unittestreport.TestRunner(suite,
                                   title='APP自动化测试报告',           # 报告标题
                                   tester='邵翠玲',               # 测试人员名称 👈 在这里修改
                                   desc='Android自动化测试生成的报告v1.0',       # 报告描述
                                   templates=1 )

try:
    runner.run()
finally:
    h1 = LogToHtml(script_root=r"D:\Projects\AirtestProject\APPAutoTest\AppTest2026\android.air",
                   log_root=r"D:\Projects\AirtestProject\APPAutoTest\AppTest2026\android.air\log",
                   export_dir=r"D:\Projects\AirtestProject\APPAutoTest\AppTest2026\test_report\android",
                   logfile=r"D:\Projects\AirtestProject\APPAutoTest\AppTest2026\android.air\log\log.txt",
                   lang='zh',
                   plugins=["poco.utils.airtest.report"])
    h1.report()

