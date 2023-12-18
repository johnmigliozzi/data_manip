from setuptools import find_packages, setup  
  
setup(  
	name='data_manip',  
	packages=find_packages(include=['data_manip']),
	version='0.1.0',  
	description='Personal Data Manipulation functions',  
	author='Me',  
	install_requires=[],  
	setup_requires=['pytest-runner'],  
	tests_require=['pytest==4.4.1'],  
	test_suite='tests',  
)