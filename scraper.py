class Scraper:
    db_link = ''
    
    def __init__(self, databasename):
        if databasename.upper() == 'CT':
            self.db_link = 'https://heise.extdb.e-fellows.net/zeitschriften/ct/artikel-archiv'
        elif databasename.upper() == 'IX':
            self.db_link = 'https://heise.extdb.e-fellows.net/zeitschriften/ix/artikel-archiv'
        else:
            raise ValueError('Invalid database name: ' + databasename)

    def printLink(self):
        print('Link: ' + self.db_link)

class CredentialReader:
    email = ''
    password = ''

    def __init__(self):
        import json
        import os.path

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
                self.email = jsoncreds['email']
                self.password = jsoncreds['password'] 

x = Scraper('ct')

y = CredentialReader()
print('Email: ' + y.email)
print('Password: ' + y.password)