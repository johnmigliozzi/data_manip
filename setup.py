from setuptools import find_packages, setup  
  
setup(  
	name='data_manip',  
	packages=find_packages(include=['data_manip','datetime','dataset','dateutil']),
	version='0.2.1',  
	description='Personal Data Manipulation functions',  
	author='John Migliozzi',  
	install_requires=[],  
	setup_requires=['pytest-runner'],  
	tests_require=['pytest==4.4.1'],  
	test_suite='tests',  
)