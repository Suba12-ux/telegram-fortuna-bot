from app import main
from app.data import FORTUNES_Ollama

def test_fortunes():
	first_name = 'Субхон'
	data = FORTUNES_Ollama(first_name)
	print(data)
	assert data