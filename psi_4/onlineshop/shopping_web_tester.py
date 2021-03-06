# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import unittest, time, os
from onlineshop.settings import MEDIA_DIR, BASE_DIR
try:
   from loremipsum import get_paragraphs
except:
   def get_paragraphs():
       return "Y, viéndole don Quijote de aquella manera, con muestras de " \
              "tanta tristeza, le dijo: Sábete, Sancho, que no es un hombre " \
              "más que otro si no hace más que otro. Todas estas borrascas " \
              "que nos suceden son señales de que presto ha de serenar el " \
              "tiempo y han de sucedernos bien las cosas; porque no es posible " \
              "que el mal ni el bien sean durables, y de aquí se sigue que, " \
              "habiendo durado mucho el mal, el bien está ya cerca. Así que, " \
              "no debes congojarte por las desgracias que a mí me suceden, " \
              "pues a ti no te cabe parte dellas."
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onLineShop.settings')
#import django
#django.setup()

#from shop.models import Product

class onLineShopTester(unittest.TestCase):
    POPULATE      = True # set to True if you  want to populate the database
    ADDPRODUCT    = True # set to True if you  want to add
                         # products to the shoppingcart
    REMOVEPRODUCT = True # set to True if you  want to remove
                         # products from the shoppingcart
    CHECKOUT      = True # press checkout botton
    PLACEORDER    = True # place order. The END ;-)
    username    = "alumnodb"
    passwd      = "alumnodb"
    #base_url    = "https://rocky-inlet-76734.herokuapp.com/"
    #base_url    = "https://pure-bayou-13155.herokuapp.com/"
    base_url     = "http://127.0.0.1:8000/"
    #base_url = "https://pacific-ocean-78885.herokuapp.com/"
    admin_url    = base_url + "admin/"
    shoppingcart_url = base_url + "shoppingcart/list/"
    create_order_url      = base_url + "placeorder/create_order/"
    confirm_order_url = base_url + "placeorder/confirm_order/"
    addCategoryPath = "shop/category/add/"
    addProductPath  = "shop/product/add/"
    catList     = ["Eau de Cologne", "Eau de Parfum","Eau de Toilette"]
    
    #los jpg esperados deben llamarse como los names
    productDict = {
                catList[0]: ["onett",
                    "twoson", "threed", "fourside", "winters", "summers"],
                catList[1]: ["phantom-blood",
                    "battle-tendency", "stardust-crusaders", 
                    "diamond-is-unbreakable","vento-aureo", "stone-ocean"],
                 catList[2]: ["symetra",
                 "ana", "mercy", "zarya", "mei", "phara"],
                }
    
    chromeDriver = os.path.join(BASE_DIR, "chromedriver")
    imagesPath = os.path.join(os.path.join(MEDIA_DIR,"images"),"products")
    purchaseCost = "136.40"

    def setUp(self):
#        self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome(self.chromeDriver)
############################################
##DO NOT CHANGE ANYTHING BELLOW THIS POINT
###########################################
    def find_element_by_id(self,_id,value,waitFor=1):
        self.driver.find_element_by_id(_id).clear()
        self.driver.find_element_by_id(_id).send_keys(value)
        time.sleep(waitFor)

    def find_element_by_xpath(self,_xpath,waitFor=1):
        self.driver.find_element_by_xpath(_xpath).click()
        time.sleep(waitFor)

    def find_element_by_name(self,_name,waitFor=1):
        self.driver.find_element_by_name(_name).click()
        time.sleep(waitFor)

    def find_element_by_link_text(self, _link, waitFor=1):
        self.driver.find_element_by_link_text(_link).click()
        time.sleep(waitFor)

    def get_url(self, url, waitFor=1):
        self.driver.get(url)

        time.sleep(waitFor)

    def login(self,userName, passwd):
        self.get_url(self.admin_url)
        self.find_element_by_id("id_username",userName)
        self.find_element_by_id("id_password",passwd)
        self.find_element_by_xpath('//*[@id="login-form"]/div[3]/input')

    def addCat(self,catName, waitFor=1):
        self.get_url(self.admin_url + self.addCategoryPath)
        self.find_element_by_id("id_catName",catName, waitFor)
        self.find_element_by_name("_save", waitFor)

    def addProduct(self, cat, prodName, ext="jpg", price="1.1", stock="1", waitFor=1):
        self.get_url(self.admin_url + self.addProductPath)

        select = Select(self.driver.find_element_by_id('id_category'))
        select.select_by_visible_text(cat)

        self.find_element_by_id("id_prodName",prodName, waitFor)
        imagePath =  os.path.join(self.imagesPath,cat.lower(),prodName+"."+ext)
        #self.driver.find_element_by_id("id_image").send_keys(imagePath)######
        self.find_element_by_id("id_image",imagePath)
        self.find_element_by_id("id_description",get_paragraphs(1)[0], waitFor)
        self.find_element_by_id("id_price",price, waitFor)
        self.find_element_by_id("id_stock",stock, waitFor)
        self.find_element_by_name("_save", waitFor)

    def selectProduct(self, id, prodSlug, units=1, waitFor=1):
        self.get_url(os.path.join(self.base_url,str(id),prodSlug))
        try:
            self.selectProductInteger(units, waitFor)
        except:
            self.selectProductList(units, waitFor)

    def selectProductInteger(self, units=1, waitFor=1):
        """ units as an IntegerField"""
        self.find_element_by_id("id_units", units, waitFor)
        self.find_element_by_xpath('//*[@id="content"]/div/form/input[4]')

    def selectProductList(self, units=1, waitFor=1):
        """units as a list"""
        select = Select(self.driver.find_element_by_id('id_units'))
        select.select_by_visible_text(str(units))
        self.find_element_by_xpath('//*[@id="content"]/div/form/input[3]')
        self.assertEqual(self.driver.current_url, self.shoppingcart_url)

    def removeProduct(self, id, prodSlug, waitFor=1):
        self.get_url(self.shoppingcart_url)
        time.sleep(waitFor)
        self.find_element_by_link_text("Remove")
        #self.find_element_by_xpath('//tr[2]/td[4]')
#                                   //*[@id="content"]/table/tbody/tr[1]/td[4]

    def fillOrderCreateForm(self, firstName, familyName,
                                  email, address, zip, city, waitFor=1):
        if self.driver.current_url == self.shoppingcart_url:
            self.find_element_by_link_text("Checkout")
        else:
            self.get_url(self.create_order_url)
        self.find_element_by_id("id_firstName", firstName)
        self.find_element_by_id("id_familyName", familyName)
        self.find_element_by_id("id_email", email)
        self.find_element_by_id("id_address", address)
        self.find_element_by_id("id_zip", zip)
        self.find_element_by_id("id_city", city)
        #text = self.purchaseCost
        #self.assertTrue(text in self.driver.page_source)

        time.sleep(waitFor)

    def placeOrder(self, waitFor=1):
        self.find_element_by_xpath(
            "//input[@type='submit' and @value='Place order']")
        time.sleep(waitFor)
        self.assertEqual(self.driver.current_url, self.confirm_order_url)

    def seeHome(self, waitFor=1):
        self.get_url(self.base_url, waitFor=1)

    def quit(self, waitFor=1):
        time.sleep(waitFor)
        self.driver.quit()

    def test_shop(self):
        #connect to Home
        self.seeHome(2)

        if self.POPULATE:
            #login in
            self.login(self.username, self.passwd)

            #addCategories
            for catName in self.catList:
                self.addCat(catName,1)

            #addProducts
            counter =1
            for catName in self.catList:
                for prodName in self.productDict[catName]:
                    self.addProduct(catName,prodName,
                                    price = str(counter * 1.1),
                                    stock = str(counter), waitFor = 0)
                    counter += 1

            #connect to Home
            self.seeHome(1)

        id1 = 1; id2 = 8; id3 = 15; id4=16
        prodSlug1 = self.productDict[self.catList[0]][0]
        prodSlug2 = self.productDict[self.catList[1]][1]
        prodSlug3 = self.productDict[self.catList[2]][2]
        prodSlug4 = self.productDict[self.catList[2]][3]
        if self.ADDPRODUCT:  #select several products
            self.selectProduct(id1, prodSlug1, units=2, waitFor=1)
            self.selectProduct(id2, prodSlug2, units=3, waitFor=1)
            self.selectProduct(id3, prodSlug3, units=4, waitFor=1)
            self.selectProduct(id4, prodSlug4, units=4, waitFor=1)

        if self.REMOVEPRODUCT:
            self.removeProduct(id2, prodSlug2, waitFor=1)
            self.removeProduct(id3, prodSlug3, waitFor=1)

        if self.CHECKOUT:
            self.fillOrderCreateForm('Julius', 'Caesar',
                                     'julius@rome.it',
                                     'Imperial Place, Pallatinus Hill',
                                     '12345', 'Rome')

            if self.PLACEORDER:
                self.placeOrder()
        #close browser
        self.quit(20)

if __name__ == "__main__":
    unittest.main()

"""

"""