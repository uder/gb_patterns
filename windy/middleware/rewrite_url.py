def _check_trailing_slash(path):
	if path[-1:]=="/":
		retval=True
	else:
		retval=False
	return retval

def rewrite_url(self,request,environ):
	path=environ['PATH_INFO']
	if not _check_trailing_slash(path):
		path=path+"/"
		
	environ['PATH_INFO']=path
	
	return request