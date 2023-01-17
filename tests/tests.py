import unittest
import pandas as pd
from unittest.mock import patch
from file_Selector import FileSelector

class TestFileSelector(unittest.TestCase):
    @patch('tkinter.filedialog.askopenfilename')
    def test_browse(self, mock_askopenfilename):
        # Arrange
        mock_askopenfilename.return_value = 'mock_file.csv'
        file_selector = FileSelector()

        # Act
        file_selector.browse()

        # Assert
        mock_askopenfilename.assert_called_once()
        self.assertEqual(file_selector.filename, 'mock_file.csv')
        self.assertEqual(file_selector.analyze_button['state'], 'normal')

    @patch('tkinter.filedialog.askopenfilename')
    def test_browse_invalid_file_type(self, mock_askopenfilename):
        # Arrange
        mock_askopenfilename.return_value = 'mock_file.txt'
        file_selector = FileSelector()

        # Act
        file_selector.browse()

        # Assert
        mock_askopenfilename.assert_called_once()
        self.assertEqual(file_selector.filename, 'mock_file.txt')
        self.assertEqual(file_selector.analyze_button['state'], 'disable')
        self.assertEqual(file_selector.result_label['text'], 'Por favor, selecione um arquivo CSV.')

    def test_analyze(self):
        # Arrange
        file_selector = FileSelector()
        file_selector.filename = 'mock_file.csv'
        file_selector.df = pd.DataFrame({'name': ['Pikachu', 'Charmander'], 'weight_kg': [6.0, 8.5]})
        file_selector.weight_kg_entry.insert(0, '6')

        # Act
        file_selector.analyze()

        # Assert
        self.assertEqual(file_selector.result_label['text'], 'Pikachu')

    def test_analyze_no_match(self):
        # Arrange
        file_selector = FileSelector()
        file_selector.filename = 'mock_file.csv'
        file_selector.df = pd.DataFrame({'name': ['Pikachu', 'Charmander'], 'weight_kg': [6.0, 8.5]})
        file_selector.weight_kg_entry.insert(0, '7')

        # Act
        file_selector.analyze()

        # Assert
        self.assertEqual(file_selector.result_label['text'], 'Nenhum Pokémon encontrado')

if __name__ == '__main__':
    unittest.main()
