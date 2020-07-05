from selenium import webdriver
import os.path
import time

class Scraper:
    FDriver = ''
    FDBLink = ''
    FDownloadPath = ''
    
    def __init__(self, ADatabasename, ADownloadpath):
        LRootURL = 'https://heise.extdb.e-fellows.net/zeitschriften'        
        if ADatabasename.upper() == 'CT':
            self.FDBLink = LRootURL + '/ct/artikel-archiv?dir=desc&mode=list&order=publishing_date&p='
        elif ADatabasename.upper() == 'IX':
            self.FDBLink = LRootURL + '/ix/?dir=desc&mode=list&order=publishing_date&p='
        else:
            raise ValueError('Invalid database name: ' + ADatabasename)
        
        if ADownloadpath == '':
            self.FDownloadPath = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'Magazine'
        else:
            self.FDownloadPath = ADownloadpath

        self.createWebdriver()

    def createWebdriver(self):
        # Profile settings
        ffProfile = webdriver.FirefoxProfile()
        ffProfile.set_preference("browser.download.folderList", 2)
        ffProfile.set_preference("browser.download.manager.showWhenStarting", False)
        ffProfile.set_preference("browser.download.dir", self.FDownloadPath)
        ffProfile.set_preference("browser.helperApps.neverAsk.saveToDisk", ("application/pdf"))
        ffProfile.set_preference("browser.helperApps.neverAsk.openFile", ("application/pdf"))
        ffProfile.set_preference("pdfjs.disabled", True)
        
        self.FDriver = webdriver.Firefox(ffProfile)
    
    def eFellowsLogin(self, AEmail, APassword):
        self.FDriver.get('https://www.e-fellows.net/')
        self.FDriver.find_element_by_class_name("btn-login").click()
        LInputEmail = self.FDriver.find_element_by_name("Login")
        LInputPassword = self.FDriver.find_element_by_name("Password")
        LInputEmail.send_keys(AEmail)
        LInputPassword.send_keys(APassword)
        LInputEmail.submit()

        time.sleep(7) # Todo: Wait until submit is finished
        
        LErrorResponses = []
        try:
            # No login-response element when login was successful -> exception is raised
            LResponseParent = self.FDriver.find_element_by_class_name('login-response')
            LErrorResponses = LResponseParent.find_elements_by_tag_name('p')
        except:
            pass
        # Check for login error codes
        for LResponse in LErrorResponses:
            if LResponse.text != '':
                raise Exception('Login error: ' + LResponse.text)
    
    def startScraper(self):
        LPageNum = 3000
        LValidPage = True

        while(LValidPage):
            self.FDriver.get(self.FDBLink + str(LPageNum))
            time.sleep(3) # Todo: dynamic waiting

            try:
                LDownloadButtons = self.FDriver.find_elements_by_xpath('//*[@title="Herunterladen"]')
                if len(LDownloadButtons) > 0:
                    for LBtn in LDownloadButtons:
                        LBtn.click()
                else:
                    LValidPage = False
            except Exception as e:
                print(e)

            LPageNum += 1

    def stopScraper(self):
        self.FDriver.quit()

class CredentialReader:
    FEmail = ''
    FPassword = ''

    def __init__(self):
        import json

        jsoncreds = {}
        if not os.path.isfile('credentials.json'):
            jsoncreds['email'] = ''
            jsoncreds['password'] = ''
            try:
                with open('credentials.json', 'w') as f:
                    json.dump(jsoncreds, f, indent = 2)
                    f.close
            finally:
                raise ValueError('File credentials.json doesn\'t exist! Please enter your credentials.')
        else:
            with open('credentials.json', 'r') as f:
                jsoncreds = json.load(f)
                f.close()            
            if (jsoncreds['email'] == '') or (jsoncreds['password'] == ''):
                raise ValueError('No credentials in credentials.json provided!')
            else:
                self.FEmail = jsoncreds['email']
                self.FPassword = jsoncreds['password'] 

FCreds = CredentialReader()

x = Scraper('ct', '')
x.eFellowsLogin(FCreds.FEmail, FCreds.FPassword)
x.startScraper()
x.stopScraper()
