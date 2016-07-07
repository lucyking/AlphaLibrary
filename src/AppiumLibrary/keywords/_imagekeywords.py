# -*- coding: utf-8 -*-
import os
from time import sleep, time
import aircv as ac
from AppiumLibrary.keywords.keywordgroup import KeywordGroup
from robot.libraries.BuiltIn import BuiltIn


class _ImageKeywords(KeywordGroup):
    """  **Wrapper Keywords for RobotFramework to click mobile screen, based on opencv & aircv.**
    """

    def __init__(self):
        print "Here is from Image"
        self._screen = ""
        self._timeout = 10
        self.img_path = ""
        self.output_dir = ""
        """ only can achieve BuiltIn().get_variables() at **running time**
        """
        # sys_variables = BuiltIn().get_variables()
        # self.output_dir = os.path.abspath(sys_variables['${OUTPUTDIR}'])

    def _capture_background(self, filename="screen.png"):
        """
        filename  the background screen
        """
        self._screen = os.path.join(self.output_dir, filename)
        self.capture_page_screenshot_without_html_log(os.path.join(self.output_dir, self._screen))

    def _prepare(self):
        """ update background  screen
        """
        if not self.output_dir:
            sys_variables = BuiltIn().get_variables()
            self.output_dir = os.path.abspath(sys_variables['${OUTPUTDIR}'])

        if os.path.isfile(self._screen):
            os.remove(self._screen)
        self._capture_background()

        start_time = time()
        while time() - start_time < self._timeout:
            if os.path.isfile(self._screen):
                return
            sleep(0.2)
            continue
        self._info("[>>>]:Capture Background failed")

    def mobile_image_set_timeout(self, time_num):
        """
        :parameter
            time_num:  wait in N secs to capture background screen
        :example
            Mobile Image Set Timeout    10
        """
        self._timeout = time_num

    def mobile_image_set_path(self, path='None'):
        """
        :param path: set the target image path
        :return: None
        """
        self.img_path = path

    def mobile_image_listdir(self):
        """show the target image directory's content
        """
        self._info("*" * 6)
        if self.img_path:
            self._info(self.img_path)
            self._info('-' * 6)
            content = os.listdir(self.img_path)
            if content.__len__() > 0:
                for item in content:
                    self._info(item)
            else:
                self._info("[>>>]:None Image")
        else:
            self._info("[>>>]:Image Path is NONE")
        self._info("*" * 6)

    def _image_click(self, target, times=1):
        """
        :param target: the target image that should be clicked
        :param times: click times
        :return: None
        """
        self._prepare()
        if self.img_path:
            target = os.path.join(self.img_path, target)
        else:
            self._info("[>>>] img path not set")
        im_source = ac.imread(self._screen.decode('utf-8').encode('gbk'))
        im_search = ac.imread(target.decode('utf-8').encode('gbk'))
        re = ac.find_template(im_source, im_search, 0.8, True)
        self._info(re)
        while (times > 0):
            times = times - 1
            self.click_a_point(re['result'][0], re['result'][1])
        os.remove(self._screen)
        return re

    def mobile_image_click(self, target):
        """click target image area 1 time
        """
        return self._image_click(target, 1)

    def mobile_image_double_click(self, target):
        """click target image area 2 times
        """
        return self._image_click(target, 2)

    def mobile_screen_should_contain(self, target):
        """assert current  screen should contain target image
        """
        self._prepare()
        im_source = ac.imread(self._screen)
        im_search = ac.imread(target)
        re = ac.find_template(im_source, im_search, 0.8, True)
        if re:
            return True
        else:
            return False

    def mobile_screen_should_not_contain(self, target):
        """assert current  screen should  NOT contain target image
        """
        if self.mobile_screen_should_contain(target):
            return False
        else:
            return True

