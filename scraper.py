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

x = Scraper('ct')
