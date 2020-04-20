from public.xlrd_handle import xlrd_handle

#excel写
a = (['a','b','c',4],[5,6,7,8],[9,10,11,12])
xh = xlrd_handle()
xh.set_sheet_name('create')
xh.set_file_path(r'C:\Users\Administrator\Desktop\abc.xls')
xh.write_to_sheet(a,[1,3,5],range(5,9))