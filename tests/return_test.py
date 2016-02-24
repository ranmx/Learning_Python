class ReturnMethod(object):
    def __init__(self):
        print "ReturnMethod is called"


def return_test():
    return_instance = ReturnMethod()
    return [return_instance]

print "functions are defined"
returned_value = return_test
print "returned_value is defined"
instance_list = []
print "instance_list is defined"
instance_list.extend(returned_value())

table_head_style = '<th style="background-color:rgb(51, 153, 102); height:1px">%s</th>'

table_head_line_temp = '<table border="double" style="width:1200px"><tbody><tr>'+\
    table_head_style % 'Index' +\
    table_head_style % 'Text Cast' +\
    table_head_style % 'Status' +\
    table_head_style % 'Execution' +\
    table_head_style % 'Comments' + '\n'

# tab = '&nbsp'*8
tc_dict = {}
tc_dict['href'] = 'HREF'
tc_dict['title'] = 'TITLE'

tc_temp_link  = '<a href=%(href)s>%(title)s</a></th>'

print tc_temp_link % tc_dict


def loop():
    for i in range(10):
        if i == 5:
            return True
        print "i =", i

loop()


