import os
print("Plik testowy")

os.environ['haslo'] = 'tajneprzezpoufne'

zmienna = os.environ.get('haslo')

print(zmienna)
#test
