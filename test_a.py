import os

def test_env():
	assert '1234' == os.getenv('SEEKRIT')
