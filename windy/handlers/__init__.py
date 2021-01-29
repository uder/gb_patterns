def root(self,environ,start_response):
	start_response(self.http_200, self.response_headers)
	
	return [b'Index Page']
	
def about(self,environ,start_response):
	start_response(self.http_200, self.response_headers)
	return [b'About Page']
	
def not_found(self,environ,start_response):
	start_response(self.http_404, self.response_headers)
	return [b'NOT EXISTENT PAGE '+environ['PATH_INFO'].encode('utf-8')]