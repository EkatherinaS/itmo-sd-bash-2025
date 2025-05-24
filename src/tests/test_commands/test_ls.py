import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from commands.ls import Ls

class TestLs:
    @pytest.fixture
    def ls_cmd(self):
        def _ls():
            return Ls([], [], {}, None).run()
        return _ls

    @patch('os.listdir')
    @patch('os.path.join')
    @patch('os.path.abspath')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    @patch('os.stat')
    def test_ls_output_format(self, mock_stat, mock_isfile, mock_isdir, 
                            mock_abspath, mock_join, mock_listdir, ls_cmd):
        test_dir = "/test/directory"
        mock_abspath.return_value = test_dir
        mock_listdir.return_value = ['file1', 'dir1']
        
        mock_isdir.side_effect = lambda x: x.endswith('dir1')
        mock_isfile.side_effect = lambda x: x.endswith('file1')
        
        mock_stat_result = MagicMock()
        mock_stat_result.st_mtime = datetime(2023, 1, 1).timestamp()
        mock_stat_result.st_size = 1024
        mock_stat.return_value = mock_stat_result
        
        mock_join.side_effect = lambda a, b: f"{a}/{b}"
        
        result = ls_cmd()
        
        assert f"Каталог: {test_dir}" in result
        assert "| Mode   |    LastWriteTime |     Length | Name\n" in result
        assert "| d---   | 01.01.2023 00:00 |            | dir1\n" in result
        assert "| -a---  | 01.01.2023 00:00 |       1024 | file1\n" in result
        assert result.endswith('\n')

    def test_ls_always_ends_with_newline(self, ls_cmd):
        output = ls_cmd()
        assert output.endswith("\n")

    @patch('os.listdir')
    @patch('os.path.abspath')
    @patch('os.path.join')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    @patch('os.stat')
    def test_ls_skips_hidden_files(self, mock_stat, mock_isfile, mock_isdir, 
                                mock_join, mock_abspath, mock_listdir, ls_cmd):
        test_dir = "/test/directory"
        mock_abspath.return_value = test_dir
        mock_listdir.return_value = ['.hidden', 'visible']
        
        mock_join.side_effect = lambda a, b: f"{a}/{b}"
        
        mock_isdir.return_value = False
        mock_isfile.return_value = True
        
        mock_stat_result = MagicMock()
        mock_stat_result.st_mtime = 1672531200  # 01.01.2023
        mock_stat_result.st_size = 1024
        mock_stat.return_value = mock_stat_result
        
        result = ls_cmd()
        
        assert '.hidden' not in result
        assert 'visible' in result
        assert '1024' in result  # Проверяем что размер файла отображается
