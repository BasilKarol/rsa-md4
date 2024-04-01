import pytest  # importowanie biblioteki pytest, która umożliwia pisanie testów jednostkowych w Pythonie
from hypothesis import given, strategies as st  # importowanie biblioteki do generowania danych testowych, która integruje się z pytestem
from md4_oop import MD4  # importowanie klasy MD4 z innego modułu

# Definicja testu jednostkowego dla metody from_string()
def test_md4_from_string():
    input_string = "Ala ma kota"  # tworzenie zmiennej input_string i przypisanie jej wartości "Ala ma kota", czyli wejściowego ciągu znaków, dla którego zostanie obliczony skrót MD4
    expected_hash = "e1fefa8fb989926d1322695a4ae34503"  # tworzenie zmiennej expected_hash i przypisanie jej oczekiwanego skrótu MD4 dla input_string
    md4_hash = MD4.from_string(input_string)  # obliczenie skrótu MD4 dla input_string za pomocą metody from_string()
    assert str(md4_hash) == expected_hash  # porównanie obliczonego skrótu z oczekiwanym skrótem

# Definicja testu jednostkowego dla metody from_file()
def test_md4_from_file(tmp_path):
    input_file = tmp_path / "test.txt"  # tworzenie tymczasowego pliku o nazwie "test.txt" i zapisanie w nim tekstu "Ala ma kota"
    input_string = "Ala ma kota"
    input_file.write_text(input_string)
    expected_hash = "e1fefa8fb989926d1322695a4ae34503"
    md4_hash = MD4.from_file(str(input_file))  # obliczenie skrótu MD4 dla zawartości pliku za pomocą metody from_file()
    assert str(md4_hash) == expected_hash  # porównanie obliczonego skrótu z oczekiwanym skrótem

# Definicja testu jednostkowego dla metody bit_blocks()
@given(st.binary())# pochodzi z biblioteki Hypothesis i jest używana do generowania danych testowych dla testu ; w teście porównywane są wyniki metody bit_blocks() z oczekiwaną listą bloków danych wejściowych. Test ten ma na celu sprawdzenie, czy metoda bit_blocks() poprawnie podzieli dane wejściowe na bloki o odpowiedniej długości
def test_md4_bit_blocks(input_text):
    md4_hash = MD4(input_text)  # utworzenie obiektu klasy MD4 z danymi wejściowymi
    assert md4_hash.block_list == md4_hash.bit_blocks()  # porównanie listy bloków danych wejściowych z listą bloków uzyskaną za pomocą metody bit_blocks()


# Wywołanie testów jednostkowych
if __name__ == "__main__":
    pytest.main()


