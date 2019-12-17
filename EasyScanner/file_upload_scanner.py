from crawler import Crawler



class FileUploadScanner:
	def __init__(self,url,login_form):
		self.url = url
		self.login_form = login_form
		self.file_included_forms = []

	

	def run(self):
		crawler = Crawler(self.url,self.login_form,quiet=True)
		crawler.run()
		self.internal_hrefs , self.get_forms, self.post_forms, self.session = crawler.return_results()
		self.get_file_included_forms()
		self.print_file_included_forms()

	def get_file_included_forms(self):
		for _form in self.post_forms:
			url, form = _form
			inputs = form.find_all('input')
			for input in inputs:
				input_type = input.get('type')
				enctype = input.get('enctype')
				if input_type == 'file' or enctype == 'multipart/form-data':
					self.file_included_forms.append(_form)

	def print_file_included_forms(self):
		for form in self.file_included_forms:
			print(form)




login_form = dict()
login_form['user_name_field'] = 'username'
login_form['user_value_field'] = 'admin'
login_form['password_name_field'] = 'password'
login_form['password_value_field'] = 'password'
login_form['url'] = 'http://192.168.1.101/login.php'
login_form['action'] = 'http://192.168.1.101/login.php'

scanner = FileUploadScanner("http://192.168.1.101",login_form)
scanner.run()


