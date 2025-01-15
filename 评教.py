from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

#为了学习，我在下面即使用了XPath也使用了Selector。

# 配置 ChromeDriver 路径并启动浏览器
options = Options()#设置浏览器启动选项。

# 手动配置chromedriver路径
# chromedriver_path = r"C:\Users\restrain\.wdm\drivers\chromedriver\win64\131.0.6778.264\chromedriver-win32\chromedriver.exe"#指定ChromeDriver路径。
# service = Service(chromedriver_path) #加载ChromeDriver服务。

#如果不知道自己电脑的chromedriver的路径在哪，也可以用下面代码自动下载。
service = Service(ChromeDriverManager().install())  # 自动下载与当前 Chrome 版本匹配的驱动

#当然如果你想用edge也可以，类比上面的代码即可。
# service = Service(EdgeChromiumDriverManager().install())  # 自动下载与 Edge 版本匹配的驱动

driver = webdriver.Chrome(service=service, options=options)# 启动浏览器。
driver.implicitly_wait(20)#隐式等待，找不到元素时会等待20秒。

try:
    # 打开登录页面
    driver.get("https://cas.upc.edu.cn/cas/login")

    # 检查是否有 iframe，需要切换到 iframe
    if len(driver.find_elements(By.TAG_NAME, "iframe")) > 0:
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        print("已切换到 iframe")

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="请输入用户名"]')))#等待用户名输入框出现。
    username_input = driver.find_element(By.XPATH, '//input[@placeholder="请输入用户名"]')#获取用户名输入框
    username_input.send_keys("你的用户名")  # 替换为你的用户名

    password_input = driver.find_element(By.XPATH, '//input[@placeholder="请输入密码"]')#获取密码输入框
    password_input.send_keys("你的密码")  # 替换为你的密码

    # 找到登录按钮并点击
    login_button = driver.find_element(By.XPATH, '//button[contains(@class, "van-button")]')#获取登录按钮
    login_button.click()

    # 等待页面跳转并检查登录是否成功
    WebDriverWait(driver, 20).until(EC.url_contains("i.upc.edu.cn"))#等待页面 URL 包含 "i.upc.edu.cn"，确保登录成功。
    print("登录成功！当前页面URL:", driver.current_url)

    # 如果当前页面URL包含"/portal/portal"，则执行后续操作
    if "/portal/portal" in driver.current_url:
        print("当前页面包含'/portal/portal'，继续执行后续操作")

        driver.switch_to.default_content()#从iframe中出来，切换回主页面上下文，以便操作主页面内容。
        print("已切换回主页面")

        # 定位到 container 并逐步点击子元素
        container = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body//*[@id="container"]'))
        )
        print("找到 container 元素")

        # 定位到第一部分
        div1 = container.find_element(By.XPATH, './div[1]')
        print("找到 container > div[1]")

        # 定位到 appMenuWidget-content 并点击子元素
        app_menu = div1.find_element(By.XPATH, '//*[@id="appMenuWidget-content"]')
        print("找到 appMenuWidget-content")

        # 定位并点击“教学应用”
        teaching_app = app_menu.find_element(By.XPATH, './div/div[5]')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(teaching_app))
        teaching_app.click()
        print("成功点击教学应用")

        # 等待并点击“教务系统”链接
        jwxt_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//li[@code="jwxt"]//a'))#检查元素是否可见并可点击。
        )
        jwxt_link.click()
        print("成功点击教务系统链接")

        try:
           # 等待新窗口打开
            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
            # 切换到最后一个窗口
            driver.switch_to.window(driver.window_handles[-1])
            print("成功切换到新窗口，新页面URL:", driver.current_url)
        except Exception as e:
            print(f"发生错误: {e}")
            print("当前窗口句柄列表:", driver.window_handles)
            driver.save_screenshot("switch_window_error.png")

        # 在新页面上执行操作
        print("新页面标题:", driver.title)
        
        # 等待并点击“教学评价”主菜单
        teaching_evaluation = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.new-main > div.main > div.sidebar > div.scrollbar > div > ul > li:nth-child(5) > div"))
        )
        teaching_evaluation.click()
        print("成功点击‘教学评价’主菜单")

        # 等待并点击“教学评价”子菜单
        sub_menu = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.new-main > div.main > div.sidebar > div.scrollbar > div > ul > li:nth-child(5) > ul > li > div"))
        )
        sub_menu.click()
        print("成功点击‘教学评价’子菜单")

        # 等待并点击“学生评价”选项
        student_evaluation = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.new-main > div.main > div.sidebar > div.scrollbar > div > ul > li:nth-child(5) > ul > li > ul > li > div"))
        )
        student_evaluation.click()
        print("成功点击‘学生评价’")
        
        # 切换到 iframe
        evaluation_iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//iframe[@id="FrameNEW_XSD_JXPJ_JXPJ_XSPJ"]'))
        )
        driver.switch_to.frame(evaluation_iframe)
        print("已切换到‘学生评价’iframe")

        # 等待表格加载
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Form1"]/table'))
        )
        print("表格已加载")

        # 获取表格的所有行
        rows = driver.find_elements(By.XPATH, '//*[@id="Form1"]/table/tbody/tr')

        # 如果有数据，遍历每一行
        if len(rows) > 1:
            print(f"找到 {len(rows) - 1} 行数据（除表头）")

            for index in range(1, len(rows)):
                try:
                    # 获取重新获取表格防止stale element reference
                    rows = driver.find_elements(By.XPATH, '//*[@id="Form1"]/table/tbody/tr')
                    row = rows[index]
                    
                    # 定位操作列中的链接
                    operation_td = row.find_element(By.XPATH, './td[8]')
                    link = operation_td.find_element(By.XPATH, './a')

                    # 打印找到的链接并点击
                    print(f"第 {index} 行找到链接：{link.get_attribute('href')}")
                    link.click()
                    print("成功点击进入评价")
                    
                    # 等待表格加载
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="dataList"]'))
                    )
                    print("课程表格已加载")

                    # 获取表格的所有行
                    dataList = driver.find_elements(By.XPATH, '//*[@id="dataList"]/tbody/tr')
                        
                    if len(dataList) > 1:
                        print(f"找到 {len(dataList) - 1} 行课程数据（除表头）")

                        for class_index in range(1, len(dataList)):
                            try:
                                # 重新获取表格的所有行，防止stale element reference错误
                                dataList = WebDriverWait(driver, 30).until(
                                    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="dataList"]/tbody/tr'))
                                )

                                #driver.find_elements(By.XPATH, '//*[@id="dataList"]/tbody/tr')
                                # 获取当前行
                                class_row = dataList[class_index]
                                # 定位操作列中的链接
                                class_operation_td = class_row.find_element(By.XPATH, './td[8]')
                                class_link = class_operation_td.find_element(By.XPATH, './a')

                                # 打印找到的链接并点击
                                print(f"第 {class_index} 行找到课程链接：{class_link.get_attribute('href')}")
                                class_link.click()
                                print("成功点击进入课程评价")
                                
                                # 等待评价表加载
                                WebDriverWait(driver, 30).until(
                                    EC.presence_of_element_located((By.XPATH, '//*[@id="table1"]'))
                                )
                                print("评价表已加载")
                                
                                # 获取评价表的所有行
                                evaluation_rows = driver.find_elements(By.XPATH, '//*[@id="table1"]/tbody/tr')

                                for norm_index in range(1, len(evaluation_rows)):
                                    try:
                                        # 获取评价表的所有行
                                        evaluation_rows = driver.find_elements(By.XPATH, '//*[@id="table1"]/tbody/tr')
                                        # 获取当前行
                                        norm_row = evaluation_rows[norm_index]
                                        # 定位操作列中的链接
                                        norm_operation_td = norm_row.find_element(By.XPATH, './td[2]')
                                        if norm_index == 1:# 第一行选择 B
                                            b_option = norm_operation_td.find_element(By.XPATH, './label[2]/input')                                      
                                            driver.execute_script("arguments[0].click();", b_option)  # 使用 JavaScript 点击.   如果使用b_option.click()的话会出现异常：Message: element not interactable
                                            #print(f"第 {norm_index} 行选择了 B")
                                        if 2 <= norm_index <= 8:# 第二到第八行选择 A 
                                            a_option = norm_operation_td.find_element(By.XPATH, './label[1]/input')
                                            driver.execute_script("arguments[0].click();", a_option)  # 使用 JavaScript 点击
                                            #print(f"第 {norm_index} 行选择了 A")
                                        if norm_index == 9:# 第九行输入总体评价
                                            pjbfb_input = WebDriverWait(driver, 10).until(
                                                EC.visibility_of_element_located((By.XPATH, '//*[@id="pjbfb"]'))
                                            )
                                            pjbfb_input.clear()
                                            pjbfb_input.send_keys("100")
                                            print("第九行已输入总体评价：100")
                                        if norm_index == 10:# 第十行输入教师建议
                                            print("第十行开始输入建议")
                                            textarea = WebDriverWait(driver, 10).until(
                                                EC.element_to_be_clickable((By.XPATH, '//*[@id="jynr"]'))
                                            )
                                            print("找到输入框了")
                                            # 清空原有内容
                                            textarea.clear()
                                            print("已清空textarea")

                                            textarea.send_keys("希望老师再接再励，老师再见！！！！！！")
                                            # txt = "希望老师再接再励，老师再见！！！！！！"
                                            # js = """var txt = arguments[1];
                                            # var textarea = arguments[0];
                                            # var nativeTextAreaValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                                            # nativeTextAreaValueSetter.call(textarea, txt);
                                            # const event = new Event("input", {bubbles: true});
                                            # textarea.dispatchEvent(event);"""
                                            # driver.execute_script(js, textarea,txt)

                                            print("已输入教师建议：希望老师再接再励，老师再见！！！！！！")                                       
                                    except Exception as e:
                                        print(f"第 {norm_index} 指标行操作失败，跳过。错误: {e}")
                                
                                # 点击保存按钮
                                norm_save = driver.find_element(By.XPATH, '//*[@id="bc"]')
                                norm_save.click()
                                
                                alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
                                alert_text = alert.text
                                print(f"Alert 对话框内容: {alert_text}")
                                
                                alert.accept()
                                
                                WebDriverWait(driver, 30).until(
                                    EC.presence_of_element_located((By.XPATH, '//*[@id="dataList"]/tbody/tr[1]/th[2]'))
                                )
                                print("评价完成，返回课程表格")
                                    
                            except Exception as e:
                                print(f"第 {class_index} 课程行操作失败，跳过。错误: {e}")

                        # 返回上一级
                        driver.find_element(By.XPATH,'//*[@id="btnShenshen"]').click()
                        
                except Exception as e:
                    print(f"第 {index - 1} 行操作失败，跳过。错误: {e}")
        
        else:
            print("表格没有数据，跳过操作")
except Exception as e:
    print(f"发生错误: {e}")
    driver.save_screenshot("error_screenshot.png")  # 保存截图以供调试

finally:
    # 关闭浏览器
    driver.quit()



