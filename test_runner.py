import unittest
from unittest.mock import patch, MagicMock
import sys
import io
from runner import load_yaml, list_classes_and_objects, execute_command, main

class TestRunner(unittest.TestCase):

    def test_load_yaml(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data="commands:\n  - test command")):
            result = load_yaml('dummy.yaml')
            self.assertEqual(result, {'commands': ['test command']})

    @patch('importlib.import_module')
    def test_list_classes_and_objects(self, mock_import):
        mock_module = MagicMock()
        mock_class = type('MockClass', (), {})
        mock_function = lambda x: x
        mock_variable = 'test_variable'

        mock_module.MockClass = mock_class
        mock_module.mock_function = mock_function
        mock_module.mock_variable = mock_variable

        mock_import.return_value = mock_module

        result = list_classes_and_objects()
        
        self.assertIn('Account', result)
        self.assertIn('Message', result)
        self.assertIn('MockClass', result['Account']['classes'])
        self.assertIn('mock_function', result['Account']['objects'])
        self.assertIn('mock_variable', result['Account']['variables'])

    @patch('builtins.print')
    def test_execute_command(self, mock_print):
        mock_classes_and_objects = {
            'TestModule': {
                'classes': {
                    'TestClass': type('TestClass', (), {'test_method': lambda self, **kwargs: 'test_result'})
                }
            }
        }

        execute_command('TestModule TestClass test_method arg1=value1', mock_classes_and_objects)

        mock_print.assert_called_with("Result of TestModule.TestClass.test_method: test_result")

    @patch('sys.argv', ['runner.py', 'test_commands.yaml'])
    @patch('runner.load_yaml')
    @patch('runner.list_classes_and_objects')
    @patch('runner.execute_command')
    def test_main(self, mock_execute, mock_list, mock_load, ):
        mock_load.return_value = {'commands': ['command1', 'command2']}
        mock_list.return_value = {'TestModule': {'classes': {}, 'objects': {}, 'variables': {}}}

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            main()

        self.assertIn("Available modules, classes, objects, and variables:", fake_out.getvalue())
        self.assertIn("Executing commands:", fake_out.getvalue())
        self.assertEqual(mock_execute.call_count, 2)

if __name__ == '__main__':
    unittest.main()