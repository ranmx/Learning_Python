from modulefinder import ModuleFinder
import os

path_init = 'scheduler/tasks/'
script_init = 'downloader.py'


class ImportSpider(object):
    def __init__(self, path, script):
        self.path = path
        self.full_path = [path+script]
        print '=' * 100
        print 'Loaded modules of %s:' % self.full_path[0]
        self.full_path_discard = []
        self.all_path = [x[0].strip('/')+'/' for x in os.walk(path)]
        self.result = []
        self.spider()

    def spider(self):
        print '-' * 40
        while len(self.full_path) != 0:
            full_path = self.full_path.pop()
            self.full_path_discard.append(full_path)
            finder = ModuleFinder()
            finder.run_script(full_path)

            for name, mod in finder.modules.iteritems():
                full_path = str(mod.__file__).replace('.', '/')
                if full_path not in self.full_path_discard:
                    if full_path.startswith('/home/alfred/pipline/code/'):
                        self.result.append(name.replace('.', '/'))
                        if not full_path.startswith('/home/alfred/pipline/code/U'):
                            self.full_path.append(full_path)
                        else:
                            self.full_path_discard.append(full_path)

            names = finder.any_missing()
            for name in names:
                for folder in self.all_path:
                    try:
                        full_path = folder + name + '.py'
                        if os.path.isfile(full_path):
                            if full_path not in self.full_path_discard:
                                self.full_path.append(full_path)
                                self.result.append(full_path)
                    except:
                        pass

        for item in sorted(set(self.result)):
            print item
        print '='*100


ImportSpider(path_init, script_init)
