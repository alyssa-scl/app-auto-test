from airtest.cli.runner import AirtestCase, run_script
from airtest.cli.parser import runner_parser
from airtest.core.api import *
import os
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

class CustomAirtestCase(AirtestCase):
    def __init__(self):
        self.package_name = "net.poweroak.bluetticloud.debug"
        super(CustomAirtestCase, self).__init__()

    def setUp(self):
        print("custom setup launcher")
        super(CustomAirtestCase, self).setUp()
#         try:
#             # 检查设备连接状态
#             self._start_app()         
#         except Exception as e:
#             print(f"Setup failed: {str(e)}")
#             self._clearup_app()
#             raise
        

    def tearDown(self):
        print("custom tearDown launcher")
#         self._clearup_app()
        super(CustomAirtestCase, self).tearDown()
    
    def _start_app(self):
        try:
            installed_packages = shell("pm list packages")
            if self.package_name not in installed_packages:
                raise Exception(f"{self.package_name}应用未安装launcher")
            print(f"{self.package_name}应用正在启用launcher。。。。")
            start_app(self.package_name)
            sleep()
        except Exception as e:
            self._clearup_app()
            raise e 
            
    
    def _clearup_app(self):
        try:
            clear_app(self.package_name)
            stop_app(self.package_name)
        except:
            pass
        
if __name__ == '__main__':
	ap = runner_parser()
	args = ap.parse_args()
	run_script(args, CustomAirtestCase)






