import os

def test_env():
	assert 'A' == os.getenv('A')
