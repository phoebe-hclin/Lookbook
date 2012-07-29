#!/usr/bin/python

import os, sys, shutil, getopt

# Project dependent stuff
DJANGO_APP_NAME = 'lookbook'

# System dependent stuff
URL_ROOT = 'http://ec2-107-22-22-8.compute-1.amazonaws.com'

# Django project dependent stuff
SOURCE_ROOT = os.getcwd()
STATIC_ROOT = '/'.join([SOURCE_ROOT,'static'])
MEDIA_ROOT = '/'.join([SOURCE_ROOT, 'media'])
DJANGO_APACHE_ROOT = '/'.join([SOURCE_ROOT, DJANGO_APP_NAME, 'apache'])
DJANGO_WSGI_FILENAME = 'django.wsgi'
DJANGO_WSGI_FILE = '/'.join([DJANGO_APACHE_ROOT, DJANGO_WSGI_FILENAME])
DJANGO_SETTINGS_LOCATION = '/'.join([SOURCE_ROOT, DJANGO_APP_NAME, DJANGO_APP_NAME])
DJANGO_SETTINGS_FILENAME = 'settings.py'
DJANGO_SETTINGS_FILE = '/'.join([DJANGO_SETTINGS_LOCATION, DJANGO_SETTINGS_FILENAME])


# TODO: MySQL settings
########################################
# Deploy Django settings.py
########################################
def deploy_django_settings():
	tmpfile = DJANGO_SETTINGS_LOCATION + '/__' + DJANGO_SETTINGS_FILENAME

	try:
		fin = open(DJANGO_SETTINGS_FILE, 'r')
	except IOError:
		print 'Cannot open file %s ' % DJANGO_SETTINGS_FILE
		sys.exit(2)
		
	try:
		fout = open(tmpfile, 'w')
	except IOError:
		print 'Cannot open file %s ' % tmpfile
		sys.exit(2)

	lines = fin.readlines()
	for line in lines:
		line = line.rstrip()
		settings_project_root = 'PROJECT_ROOT = '
		if line.find(settings_project_root) != -1:
			line = line[:len(settings_project_root)] + '\'' + SOURCE_ROOT + '/' + '\''
			
		settings_url_root = 'URL_ROOT = '
		if line.find(settings_url_root) != -1:
			line = line[:len(settings_url_root)] + '\'' + URL_ROOT + '/' + '\''

		fout.write(line+'\n')

	fin.close()
	fout.close()

	try:
		shutil.copyfile(tmpfile, DJANGO_SETTINGS_FILE)
	except IOError:
		print 'Cannot copy file %s ' % DJANGO_SETTINGS_FILE
		sys.exit(2)
	os.remove(tmpfile)

	print 'Deployed %s' % DJANGO_SETTINGS_FILE 


########################################
# Deploy django.wsgi
########################################
def deploy_django_wsgi():
	tmp_wsgi_file = SOURCE_ROOT + '/__' + DJANGO_WSGI_FILENAME
	dst_wsgi_file = DJANGO_WSGI_FILE
	django_setting_module = DJANGO_APP_NAME + '.' + 'settings'

	try:
		fout = open(tmp_wsgi_file, 'w')
	except IOError:
		print 'Cannot open file %s ' % tmp_wsgi_file
		sys.exit(2)

	fout.write('import os, sys\n')
	fout.write('\n')
	fout.write('path = \'%s\'\n' % (SOURCE_ROOT+'/'+DJANGO_APP_NAME))
	fout.write('if path not in sys.path:\n')
	fout.write('    sys.path.append(path)\n')
	fout.write('\n')
	fout.write('os.environ[\'DJANGO_SETTINGS_MODULE\'] = \'%s\'\n' % django_setting_module)
	fout.write('\n')
	fout.write('import django.core.handlers.wsgi\n')
	fout.write('application = django.core.handlers.wsgi.WSGIHandler()')

	fout.close()

	try:
		shutil.copyfile(tmp_wsgi_file, dst_wsgi_file)
	except IOError:
		print 'Cannot copy file %s ' % dst_wsgi_file
		sys.exit(2)
	os.remove(tmp_wsgi_file)

	print 'Deployed %s' % DJANGO_WSGI_FILE 


########################################
# Deploy /etc/apache2/httpd.conf
########################################
def deploy_httpconf():
	CSS_REGEXP = '^/([^/]*\\.css)'
	JS_REGEXP = '^/([^/]*\\.js)'

	HTTPDCONF_FILENAME = 'httpd.conf'
	tmp_httpdconf_file = SOURCE_ROOT + '/__' + HTTPDCONF_FILENAME
	dst_httpdconf_file = '/etc/apache2/httpd.conf' 

	try:
		fout = open(tmp_httpdconf_file, 'w')
	except IOError:
		print 'Cannot open file %s ' % tmp_httpdconf_file
		sys.exit(2)

	fout.write(' '.join(['AliasMatch', CSS_REGEXP, STATIC_ROOT+'/css/$1']) + '\n')
	fout.write(' '.join(['AliasMatch', JS_REGEXP, STATIC_ROOT+'/js/$1']) + '\n')
	fout.write('\n')

	fout.write(' '.join(['Alias', '/media', MEDIA_ROOT]) + '\n')
	fout.write(' '.join(['Alias', '/static', STATIC_ROOT]) + '\n')
	fout.write('\n')

	fout.write('<Directory '+MEDIA_ROOT+'>\n')
	fout.write('Order deny,allow\n')
	fout.write('Allow from all\n')
	fout.write('</Directory>\n')
	fout.write('\n')

	fout.write('<Directory '+STATIC_ROOT+'>\n')
	fout.write('Order deny,allow\n')
	fout.write('Allow from all\n')
	fout.write('</Directory>\n')
	fout.write('\n')

	fout.write(' '.join(['WSGIScriptAlias', '/', DJANGO_APACHE_ROOT+'/django.wsgi']) + '\n')
	fout.write('\n')

	fout.write('<Directory '+DJANGO_APACHE_ROOT+'>\n')
	fout.write('<Files django.wsgi>\n')
	fout.write('Order deny,allow\n')
	fout.write('Allow from all\n')
	fout.write('</Files>\n')
	fout.write('</Directory>\n')

	fout.close()

	try:
		shutil.copyfile(tmp_httpdconf_file, dst_httpdconf_file)
	except IOError:
		print 'Cannot copy file %s ' % dst_httpdconf_file
		sys.exit(2)
	os.remove(tmp_httpdconf_file)

	print 'Deployed /etc/apache2/httpd.conf'


def deploy_debug():
	print 'Deploying in DEBUG mode.'
	deploy_django_settings()
	

# TODO: chmod lookbook/, media/, media/looks/, sqlite3.db
def deploy_production():
	print 'Deploying in PRODUCTION mode.'
	deploy_django_settings()
	deploy_django_wsgi()
	deploy_httpconf()


def usage():
	print ''
	print 'usage: python deploy.py [option] [args]'
	print '  -h, --help        Display this help'
	print '  -d, --debug=MODE  MODE=true will deploy in DEBUG mode. MODE=false will deploy in PRODUCTION mode. Note that root permission is required to deploy in PRODUCTION mode'
	print ''
	print 'Example usages:'
	print 'python deploy.py --debug=true'
	print 'python deploy.py --debug=false'


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hd:', ['help', 'debug='])
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)

	debug = True
	for o, a in opts:
		if o in ('-h', '--help'):
			usage()
			sys.exit()
		elif o in ('-d', '--debug'):
			if a == 'false':
				debug = False
			elif a == 'true':
				debug = True
			else:
				print 'Invalid values for option %s' % o
				usage()
				sys.exit(2)

	if debug == True:
		deploy_debug()
	else:
		deploy_production()
	

if __name__ == '__main__':
	main()
