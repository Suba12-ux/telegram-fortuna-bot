from app import main
from app.data import FORTUNES_Giga

def test_fortunes():
	first_name = 'Субхон'
	data = FORTUNES_Giga(first_name)
	print(data)
	assert data