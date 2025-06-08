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
        
        mock_isdir.side_effect = lambda x: x == test_dir
        mock_isfile.side_effect = lambda x: not mock_isdir(x)
        
        mock_stat_result = MagicMock()
        mock_stat_result.st_mtime = datetime(2023, 1, 1).timestamp()
        mock_stat_result.st_size = 1024
        mock_stat.return_value = mock_stat_result
        
        result = ls_cmd()
        
        assert '.hidden' not in result
        assert 'visible' in result
        assert '1024' in result

    @patch('os.listdir')
    @patch('os.path.abspath')
    def test_ls_nonexistent_directory(self, mock_abspath, mock_listdir, ls_cmd):
        test_dir = "/nonexistent/directory"
        mock_abspath.return_value = test_dir
        mock_listdir.side_effect = FileNotFoundError
        
        result = ls_cmd()
        assert f"ls: {test_dir}: No such file or directory" in result

    @patch('os.path.abspath')
    @patch('os.path.isdir')
    def test_ls_with_file_argument(self, mock_isdir, mock_abspath):
        test_file = "/test/file.txt"
        mock_abspath.return_value = test_file
        mock_isdir.return_value = False

        mock_stat_result = MagicMock()
        mock_stat_result.st_mtime = datetime(2023, 1, 1).timestamp()
        mock_stat_result.st_size = 2048
        
        with patch('os.stat', return_value=mock_stat_result):
            ls = Ls([test_file], [], {}, None)
            result = ls.run()
        
        assert "| -a---  | 01.01.2023 00:00 |       2048 | file.txt" in result

    @patch('os.listdir')
    @patch('os.path.abspath')
    @patch('os.path.isdir')
    def test_ls_empty_directory(self, mock_isdir, mock_abspath, mock_listdir):
        test_dir = "/empty/directory"
        mock_abspath.return_value = test_dir
        mock_isdir.return_value = True
        mock_listdir.return_value = []
        
        ls = Ls([test_dir], [], {}, None)
        result = ls.run()
        expected_output = (
            "\nКаталог: /empty/directory\n\n"
            "| Mode   |    LastWriteTime |     Length | Name\n"
            "|--------|------------------|------------|----------\n"
            "\n"
        )
        assert result == expected_output

    @patch('os.listdir')
    @patch('os.path.abspath')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    @patch('os.stat')
    def test_ls_multiple_directories(self, mock_stat, mock_isfile, mock_isdir,
                                   mock_abspath, mock_listdir):
        dir1 = "/test/dir1"
        dir2 = "/test/dir2"
        mock_abspath.side_effect = lambda x: x
        mock_isdir.side_effect = lambda x: x in [dir1, dir2]
        mock_listdir.side_effect = [
            ['file1'],
            ['file2']
        ]
        
        mock_isfile.return_value = False
        mock_stat_result = MagicMock()
        mock_stat_result.st_mtime = datetime(2023, 1, 1).timestamp()
        mock_stat_result.st_size = 1024
        mock_stat.return_value = mock_stat_result
        
        ls = Ls([dir1, dir2], [], {}, None)
        result = ls.run()
        
        assert f"Каталог: {dir1}" in result
        assert f"Каталог: {dir2}" in result
        assert "file1" in result
        assert "file2" in result

    @patch('os.listdir')
    @patch('os.path.abspath')
    @patch('os.path.join')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    @patch('os.stat')
    def test_ls_special_characters_in_names(self, mock_stat, mock_isfile, mock_isdir,
                                          mock_join, mock_abspath, mock_listdir, ls_cmd):
        test_dir = "/test/directory"
        mock_abspath.return_value = test_dir
        mock_listdir.return_value = ['file with spaces', 'file$with$special$chars']
        
        mock_isdir.return_value = False
        mock_isfile.return_value = True
        mock_join.side_effect = lambda a, b: f"{a}/{b}"
        
        mock_stat_result = MagicMock()
        mock_stat_result.st_mtime = datetime(2023, 1, 1).timestamp()
        mock_stat_result.st_size = 1024
        mock_stat.return_value = mock_stat_result
        
        result = ls_cmd()
        
        assert "file with spaces" in result
        assert "file$with$special$chars" in result
