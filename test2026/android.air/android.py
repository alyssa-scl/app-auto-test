# -*- encoding=utf8 -*-
__author__ = "刘青林"

from airtest.core.api import *
auto_setup(__file__,logdir=True)
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
import logging
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)
from airtest.report.report import LogToHtml
import unittest
import unittestreport


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
#判断是否在一级页面，否则返回一级页面
def main_page():
    for i in range(10):
        if poco(text="首页").exists():
            break
        else:
            keyevent("BACK")#keyevent返回上一级
            sleep()
#登录页
def login_page():
    for i in range(10):
        if poco(text="登录/注册").exists():
            break
        else:
            keyevent("BACK")#keyevent返回上一级
            sleep()
#登录
def login(email="us1@qq.com", password="123456"):
    login_page()
    poco(text="登录/注册").click()
    try:
        poco(text="请输入邮箱").click()
        text(email)
        poco(text="请输入登录密码").click()
        text(password)
    except:
        poco(text="us1@qq.com").click()
        key_del(10)
        text(email)
        poco(text="••••••").click()
        key_del(6)
        text(password)
    finally:
        poco("net.poweroak.bluetticloud.debug:id/check_user_agreement").click()
        poco(text="登录").click()
#退出登录
def logout():
    main_page()
    poco(text="我的").click()
    poco(text="我的账户").click()
    poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
    poco(text="确定").click()
#按钮返回上一级
def button_back(num):
    for i in range(num):
        poco("net.poweroak.bluetticloud.debug:id/imgLeft").click()
#整页从上至下滑动，展示上方内容
def swipe_up(num):
    for i in range(num):
        swipe((600, 600), (600, 2000))
#整夜从下至上滑动，展示下方内容
def swipe_down(num):
    for i in range(num):
        swipe((600, 2000), (600, 600))
#提交数据（下一步、确定）
def submit(num):
    for i in range(num):
        poco("net.poweroak.bluetticloud.debug:id/btn_submit").click()
#点击搜索框输入文案
def search(txt):
    poco("net.poweroak.bluetticloud.debug:id/edt_search").click()
    text(txt)
#键盘删除
def key_del(num):
    for i in range(num):
        keyevent("KEYCODE_DEL")
#检测到新版本是否刷新页面
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

class TestLogin(unittest.TestCase):
    def test01_login(self):
        login()
        sleep(2)
        gentle_reminder()
        is_refresh()
    def test02_logout(self):
        logout()
    def test03_nomail_no_password(self):
        login(email="", password="")
    def test04_error_format(self):
        login(email="123456", password="123456")
    def test05_error_password(self):
        login(email="us1@qq.com", password="1234567")
    def test06_error_email(self):
        login(email="us12345@qq.com", password="1234567")
    def test07_quick_login(self):
        login_page()
        poco(text="登录/注册").click()
        poco(text="快捷登录").click()
        poco(text="登录").click()
        poco(text="请输入验证码").click()
        text("123456")
        poco(text="登录").click()
        poco(text="同意").click()
        poco(text="登录").click()
    def test08_sigin_in(self):
        login_page()
        poco(text="登录/注册").click()
        poco(text="注册").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
    def test09_forgot_password(self):
        login_page()
        poco(text="登录/注册").click()
        poco(text="忘记密码").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
    def test10_check_user_agreement(self):
        login_page()
        poco(text="登录/注册").click()
        touch(Template(r"tpl1770362926499.png", record_pos=(-0.058, 0.936), resolution=(1080, 2400)))
        sleep(3)
        button_back(1)

        touch(Template(r"tpl1770362941172.png", record_pos=(0.256, 0.933), resolution=(1080, 2400)))
        sleep(3)
        button_back(1)
        poco("net.poweroak.bluetticloud.debug:id/login_sub_protocol").click()
        sleep(3)
        button_back(1)
    def test11_login_without_agreement(self):
        login_page()
        poco(text="登录/注册").click()
        poco(text="us1@qq.com").click()
        key_del(10)
        text("us1@qq.com")
        poco(text="••••••").click()
        key_del(6)
        text("123456")
        poco(text="登录").click()
        poco(text="同意").click()
        poco(text="登录").click()
        sleep(2)
        gentle_reminder()
        is_refresh()

class TestMe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        main_page()
        poco(text="我的").click()
    def tearDown(self):
        main_page()
    def test01_my_account01(self):
        #个人中心
        poco("net.poweroak.bluetticloud.debug:id/iv_user_avatar").click()
        poco("net.poweroak.bluetticloud.debug:id/item_nickname").click()
        poco("net.poweroak.bluetticloud.debug:id/et_content").click()
        key_del(3)
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco("net.poweroak.bluetticloud.debug:id/iv_close").click()
        poco("net.poweroak.bluetticloud.debug:id/layout_start").click()
        poco(text="安全邮箱").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco("net.poweroak.bluetticloud.debug:id/imgLeft").click()
        poco(text="更改密码").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco("net.poweroak.bluetticloud.debug:id/imgLeft").click()
        poco(text="更改国家/地区").click()
        poco(text="取消").click()
        poco(text="更改国家/地区").click()
        poco(text="确定").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_content").click()
        poco(text="阿尔巴尼亚").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco("net.poweroak.bluetticloud.debug:id/imgLeft").click()
        poco(text="Google").click()
        poco("net.poweroak.bluetticloud.debug:id/imgLeft").click()
        poco(text="Twitter").click()
        poco("net.poweroak.bluetticloud.debug:id/imgLeft").click()
        poco(text="注销账户").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_protocol").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
    def test01_my_account02(self):
        poco(text="我的账户").click()
    def test02_push(self):
        poco("net.poweroak.bluetticloud.debug:id/iv_push_message").click()
        poco("net.poweroak.bluetticloud.debug:id/imgRight").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_notify_manager").click()
        button_back(1)
        poco("net.poweroak.bluetticloud.debug:id/iv_switch").click()
        poco("net.poweroak.bluetticloud.debug:id/iv_switch").click()
        poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("net.poweroak.bluetticloud.debug:id/rv_other_setting").child("net.poweroak.bluetticloud.debug:id/rl_subject_notify_container")[0].child("net.poweroak.bluetticloud.debug:id/iv_switch_subject").click()
        poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("net.poweroak.bluetticloud.debug:id/rv_other_setting").child("net.poweroak.bluetticloud.debug:id/rl_subject_notify_container")[0].child("net.poweroak.bluetticloud.debug:id/iv_switch_subject").click()
    def test03_address(self):
        #地址管理
        poco(text="地址管理").click()
        poco(text="新增地址").click()
        swipe_down(2)
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco("net.poweroak.bluetticloud.debug:id/set_default").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        swipe_up(2)
        poco(text="请输入你的名字").click()
        text("姓氏姓氏")
        poco(text="请输入你的姓氏").click()
        text("姓名姓名")
        poco(text="请输入你的中间名").click()
        text("中间名中间名")
        poco(text="请输入你的公司名称").click()
        text("公司名称公司名称公司名称")
        poco("net.poweroak.bluetticloud.debug:id/tv_content").click()
        swipe_down(3)
        poco("net.poweroak.bluetticloud.debug:id/edt_search").click()
        text("美国")
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        swipe_down(1)
        poco(text="请选择所在省/州").click()
        poco("net.poweroak.bluetticloud.debug:id/btnSubmit").click()
        poco(text="请输入所在城市").click()
        text("所在城市所在城市所在城市所在城市所在城市")
        poco(text="请输入详细地址").click()
        text("详细地址所在城市所在城市所在城市所在城市所在城市所在城市")
        swipe_down(1)
        poco(text="请输入邮政编码").click()
        text("87655678")
        poco(text="请输入手机号码").click()
        text("4259923545")
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        #poco(text="姓氏姓氏 中间名中间名 姓名姓名").click()
        swipe((800, 600), (300, 600))
        poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android:id/content").offspring("net.poweroak.bluetticloud.debug:id/refreshLayout").offspring("net.poweroak.bluetticloud.debug:id/rv_address").offspring("net.poweroak.bluetticloud.debug:id/right_menu")[0].child("android.widget.ImageView").click()
        poco(text="取消").click()
        swipe((800, 600), (300, 600))
        poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android:id/content").offspring("net.poweroak.bluetticloud.debug:id/refreshLayout").offspring("net.poweroak.bluetticloud.debug:id/rv_address").offspring("net.poweroak.bluetticloud.debug:id/right_menu")[0].child("android.widget.ImageView").click()
        poco(text="确定").click()
    def test04_bluetti_star(self):
        #bluetti star
        poco(text="BLUETTI STAR").click()
        sleep(6)
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        swipe_down(2)
        for i in range(2):
            poco("net.poweroak.bluetticloud.debug:id/btn_submit").click()
        swipe_down(4)
        for i in range(2):
            poco("net.poweroak.bluetticloud.debug:id/btn_submit").click()
        button_back(3)
        swipe_up(2)
        poco(text="合作企业名称").click()
        for i in range(6):
            keyevent("KEYCODE_DEL")
        swipe_down(2)
        poco("net.poweroak.bluetticloud.debug:id/btn_submit").click()
        sleep()
        button_back(1)
        poco(text="确定").click()
    def test05_installer_contact_us(self):
        #installer&联系我们
        poco(text="INSTALLER").click()
        sleep(2)
        poco("android.widget.LinearLayout").offspring("net.poweroak.bluetticloud.debug:id/webContainer").child("android.webkit.WebView").child("android.webkit.WebView").child("android.view.View").child("android.view.View")[1].click()
        poco("android.widget.LinearLayout").offspring("android:id/content").offspring("net.poweroak.bluetticloud.debug:id/item_online_service").child("net.poweroak.bluetticloud.debug:id/root_view").click()
        button_back(1)
        poco("android.widget.LinearLayout").offspring("android:id/content").offspring("net.poweroak.bluetticloud.debug:id/item_phone_service").child("net.poweroak.bluetticloud.debug:id/root_view").click()
        poco("android.widget.LinearLayout").offspring("android:id/content").offspring("net.poweroak.bluetticloud.debug:id/swipeRefreshLayout").offspring("net.poweroak.bluetticloud.debug:id/rv_content").child("android.view.ViewGroup")[0].child("net.poweroak.bluetticloud.debug:id/rv_item").offspring("android.widget.ImageView").click()
        poco("net.poweroak.bluetticloud.debug:id/iv_close").click()
        button_back(1)
        poco("android.widget.LinearLayout").offspring("android:id/content").offspring("net.poweroak.bluetticloud.debug:id/item_email_service").child("net.poweroak.bluetticloud.debug:id/root_view").click()
        poco("android.widget.LinearLayout").offspring("android:id/content").offspring("net.poweroak.bluetticloud.debug:id/swipeRefreshLayout").offspring("net.poweroak.bluetticloud.debug:id/rv_content").child("android.view.ViewGroup")[0].child("net.poweroak.bluetticloud.debug:id/rv_item").offspring("android.widget.ImageView").click()
        poco("net.poweroak.bluetticloud.debug:id/iv_close").click()
    def test06_rate(self):
        #app评分
        poco(text="App评分").click()
        home()
        start_app("net.poweroak.bluetticloud.debug")
    def test07_clear_cache(self):
        #清理缓存
        poco(text="清理缓存").click()
        poco(text="取消").click()
        poco(text="清理缓存").click()
        poco(text="确定").click()
        poco(text="清理缓存").click()
        poco(text="取消").click()
    def test08_agreement_policy(self):
        #用户协议&隐私政策
        swipe_down(1)
        poco(text="用户协议").click()
        button_back(1)
        poco(text="隐私政策").click()
    def test09_setting(self):
        #通用设置
        poco(text="通用设置").click()
        poco(text="多语言").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco(text="字体大小").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco(text="主题模式").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco(text="主图风格").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco(text="America/New_York").click()
        poco(text="America/New_York").click()
        poco(text="温度单位").click()
        poco(text="℃").click()
        poco(text="货币单位").click()
        poco("net.poweroak.bluetticloud.debug:id/iv_search").click()
        poco("net.poweroak.bluetticloud.debug:id/edt_search").click()
        text("美国")
        poco("net.poweroak.bluetticloud.debug:id/tv_country_name").click()
        poco(text="电价设置").click()
        poco("net.poweroak.bluetticloud.debug:id/layout_start").click()
        poco(text="固定电价").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        button_back(1)
        poco(text="峰谷电价").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        button_back(3)
        poco(text="碳排量系数").click()
        poco("net.poweroak.bluetticloud.debug:id/iv_tips_icon").click()
        poco("net.poweroak.bluetticloud.debug:id/iv_close").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco(text="首页天气组件").click()
        poco(text="首页天气组件").click()
        swipe((500, 2000), (600, 600))
        poco(text="数据统计服务").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco(text="取消").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
        poco(text="确定").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_name").click()
    def test10_about_bluetti(self):
        #关于我们
        poco(text="关于我们").click()
    def test11_subscribe(self):
        #订阅品牌
        poco(text="订阅品牌").click()
        sleep(5)
        poco(text="取消订阅").click()
        sleep(5)
        poco(text="确认订阅").click()
        sleep(2)


class TestService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        main_page()
        poco(text="服务").click()
    def tearDown(self):
        main_page()
    def test01_contact_us(self):
        #联系我们入口
        poco("android.widget.LinearLayout").offspring("android.widget.FrameLayout").offspring("net.poweroak.bluetticloud.debug:id/scroll_view").offspring("android.widget.ImageView").click()
    def test02_user_manuals(self):
        #产品手册
        poco(text="产品手册").click()
        poco("net.poweroak.bluetticloud.debug:id/imgRight").click()
        poco("net.poweroak.bluetticloud.debug:id/edt_search").click()
        text("AC300")
        poco("net.poweroak.bluetticloud.debug:id/edt_search").click()
        for i in range(5):
            keyevent("KEYCODE_DEL")
        text("AC")
        poco("net.poweroak.bluetticloud.debug:id/arrow").click()
        poco(text="CN    中国").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_country").click()
        swipe_down(1)
        poco(text="US    美国").click()
        poco(text="EP600").click()
        poco(text="18345a6007110d5a636fb34b579(1)").click()
        home()
        start_app("net.poweroak.bluetticloud.debug")
        poco(text="Home Energy System Design Estimate").click()
        poco("net.poweroak.bluetticloud.debug:id/tvRight").click()
        poco("com.android.chrome:id/negative_button").click()
        home()
        start_app("net.poweroak.bluetticloud.debug")
        button_back(3)
        poco("net.poweroak.bluetticloud.debug:id/tv_content").click()
        poco(text="中国").click()
        poco("android.widget.LinearLayout").offspring("android:id/content").offspring("android.widget.ScrollView").offspring("net.poweroak.bluetticloud.debug:id/rv_data").child("android.view.ViewGroup")[1].child("net.poweroak.bluetticloud.debug:id/iv_fold").click()
        poco("android.widget.LinearLayout").offspring("android:id/content").offspring("android.widget.ScrollView").offspring("net.poweroak.bluetticloud.debug:id/rv_data").child("android.view.ViewGroup")[2].child("net.poweroak.bluetticloud.debug:id/iv_fold").click()
        poco("android.widget.LinearLayout").offspring("android:id/content").offspring("android.widget.ScrollView").offspring("net.poweroak.bluetticloud.debug:id/rv_data").child("android.view.ViewGroup")[0].child("net.poweroak.bluetticloud.debug:id/iv_fold").click()
    def test03_guidelins(self):
        #用户指引
        poco(text="用户指引").click()
        poco("net.poweroak.bluetticloud.debug:id/imgRight").click()
        poco("net.poweroak.bluetticloud.debug:id/et_search").click()

        text("AC300")
        sleep(1)
        poco("net.poweroak.bluetticloud.debug:id/et_search").click()
        for i in range(5):
            keyevent("KEYCODE_DEL")
        text("AC")
        sleep(1)
        poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android:id/content").child("android.view.ViewGroup").offspring("net.poweroak.bluetticloud.debug:id/rv_search_video").child("android.widget.LinearLayout")[0].offspring("net.poweroak.bluetticloud.debug:id/siv_video_cover")[0].click()
        for i in range(3):
            touch(Template(r"tpl1768897610029.png", record_pos=(-0.414, -0.937), resolution=(1080, 2400)))
        poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("net.poweroak.bluetticloud.debug:id/rv_serial_model").child("net.poweroak.bluetticloud.debug:id/root_view")[0].click()
        poco("net.poweroak.bluetticloud.debug:id/iv_expand").click()
    def test04_FAQ_trouble_shooting_feedback(self):
        #常见问题&故障排查&问题反馈
        poco(text="常见问题").click()
        touch(Template(r"tpl1770369442706.png", record_pos=(-0.281, -0.462), resolution=(1080, 2400)))
        poco(text="详情").click()
        button_back(2)
        poco("net.poweroak.bluetticloud.debug:id/imgRight").click()
        poco("net.poweroak.bluetticloud.debug:id/tv_country").click()
        poco(text="JP  日本").click()
        poco("net.poweroak.bluetticloud.debug:id/edt_search").click()
        text("30")
        sleep(1)
        poco("net.poweroak.bluetticloud.debug:id/edt_search").click()
        text("0")
        sleep(1)
        poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android:id/content").offspring("net.poweroak.bluetticloud.debug:id/rv_model").child("androidx.appcompat.widget.LinearLayoutCompat")[0].child("net.poweroak.bluetticloud.debug:id/iv_product").click()
        poco(text="文章1修改修改").click()
        poco("hfhfghfghfghfghfh").click()
        poco("Can the Apex 300 output both 120V and 240V at the same time?").click()
        poco(text="AC500").click()
        poco(text="大萨达").click()
        poco(text="已解决").click()
        poco(text="已解决").click()
        poco(text="未解决").click()
        poco(text="问题反馈").click()
        poco(text="自助报障").click()
        poco("net.poweroak.bluetticloud.debug:id/btn_submit").click()
        button_back(1)
        poco(text="物流").click()
        poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android:id/content").child("android.view.ViewGroup").child("net.poweroak.bluetticloud.debug:id/fragment_container").child("net.poweroak.bluetticloud.debug:id/fragment_container").offspring("net.poweroak.bluetticloud.debug:id/rv_feedback").offspring("net.poweroak.bluetticloud.debug:id/rv_checkbox").child("android.view.ViewGroup")[3].click()
        poco(text="客服问题").click()
        poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android:id/content").child("android.view.ViewGroup").child("net.poweroak.bluetticloud.debug:id/fragment_container").child("net.poweroak.bluetticloud.debug:id/fragment_container").offspring("net.poweroak.bluetticloud.debug:id/rv_feedback").offspring("net.poweroak.bluetticloud.debug:id/rv_checkbox")[0].child("android.view.ViewGroup")[3].click()
        poco("net.poweroak.bluetticloud.debug:id/imgLeft").click()
        poco(text="BLUETTI APP").click()
        poco("net.poweroak.bluetticloud.debug:id/btn_submit").click()
        button_back(2)
        poco(text="未解决").click()
        poco(text="已解决").click()
        sleep(1)
        poco(text="未解决").click()
        poco(text="联系我们").click()
        button_back(4)
        poco("net.poweroak.bluetticloud.debug:id/layout_start").click()
        poco(text="中国").click()
        poco("android.widget.LinearLayout").offspring("android:id/content").offspring("android.widget.ScrollView").offspring("net.poweroak.bluetticloud.debug:id/rv_data").offspring("net.poweroak.bluetticloud.debug:id/rv_device_model").child("androidx.appcompat.widget.LinearLayoutCompat")[0].child("net.poweroak.bluetticloud.debug:id/iv_product").click()
        poco(text="文章2引用美国、日本文章1").click()
        poco(text="AC200+B300").click()
        button_back(2)
        poco(text="故障排查").click()
        poco(text="BC500C").click()
        poco(text="25").click()
        poco(text="BC500C").click()
        poco(text="B300K Battery").click()
        poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android:id/content").offspring("net.poweroak.bluetticloud.debug:id/ll_category").child("net.poweroak.bluetticloud.debug:id/iv_more").click()
        poco("net.poweroak.bluetticloud.debug:id/iv_close").click()
    def test05_LAAF(self):
        #LAAF
        poco(text="LAAF").click()
        poco("net.poweroak.bluetticloud.debug:id/imgRight").click()
    def test06_warranty(self):
        #保修政策
        poco(text="保修政策").click()
    def test07_refund(self):
        #退款政策
        poco(text="退款政策").click()

suite = unittest.TestSuite()
loaderer = unittest.TestLoader()

suite0 = unittest.TestLoader().loadTestsFromTestCase(TestLogin)
suite1 = unittest.TestLoader().loadTestsFromTestCase(TestMe)
suite2 = unittest.TestLoader().loadTestsFromTestCase(TestService)
suite = unittest.TestSuite([suite0, suite1, suite2])

#test = [TestService('test01_contact_us')]
#suite.addTests(test)

runner = unittestreport.TestRunner(suite,
                                   tester='刘青林',
                                   filename="android_unittestreport.html",
                                   report_dir=r"D:\Projects\AirtestProject\APPAutoTest\test2026\test_report\android",
                                   title="Android测试报告",
                                   desc="Android非设备类测试",
                                   templates=1
                                   )
try:
    runner.run()
finally:
    h1 = LogToHtml(script_root=r"D:\Projects\AirtestProject\APPAutoTest\test2026\android.air",
                   log_root=r"D:\Projects\AirtestProject\APPAutoTest\test2026\android.air\log",
                   export_dir=r"D:\Projects\AirtestProject\APPAutoTest\test2026\test_report\android",
                   logfile=r"D:\Projects\AirtestProject\APPAutoTest\test2026\android.air\log\log.txt",
                   lang='zh',
                   plugins=["poco.utils.airtest.report"])
    h1.report()




