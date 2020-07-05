from selenium import webdriver
import os.path

class Scraper:
    FDriver = ''
    FDBLink = ''
    FDownloadPath = ''
    
    def __init__(self, ADatabasename, ADownloadpath):
        if ADatabasename.upper() == 'CT':
            self.FDBLink = 'https://heise.extdb.e-fellows.net/zeitschriften/ct/artikel-archiv'
        elif ADatabasename.upper() == 'IX':
            self.FDBLink = 'https://heise.extdb.e-fellows.net/zeitschriften/ix/artikel-archiv'
        else:
            raise ValueError('Invalid database name: ' + ADatabasename)
        
        if ADownloadpath == '':
            self.FDownloadPath = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'Magazine'
        else:
            self.FDownloadPath = ADownloadpath

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

x = Scraper('ct', '')
