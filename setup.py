import setuptools

with open('README.md', 'rt') as readme:
	long_description = readme.read()

with open('requirements.txt', 'rt') as f:
	requires = f.readlines()
	for i, r in enumerate(requires):
		requires[i] = r.strip('\r\n')

setuptools.setup(
	name='knigavuhe',
	version='0.1.0',
	author='Chechkenev Andrey (@DarkCat09)',
	author_email='aacd0709@mail.ru',
	description='Unofficial knigavuhe.org API',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/DarkCat09/knigavuhe',
	project_urls={
		'Bug Tracker': 'https://github.com/DarkCat09/knigavuhe/issues',
	},
	classifiers=[
		'Development Status :: 4 - Beta',
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: Apache Software License',
		'Operating System :: OS Independent'
	],
	install_requires=requires,
	packages=['knigavuhe'],
	python_requires=">=3.6",
)
