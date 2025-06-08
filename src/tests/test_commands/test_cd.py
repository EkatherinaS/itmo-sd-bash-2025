import pytest
import os
from unittest.mock import patch, MagicMock
from commands.cd import Cd

class TestCd:
    @pytest.fixture
    def cd_cmd(self):
        def _cd(args=None, flags=None, options=None, stdin=None):
            if args is None:
                args = []
            if flags is None:
                flags = []
            if options is None:
                options = {}
            return Cd(args, flags, options, stdin).run()
        return _cd

    @patch('os.chdir')
    @patch('os.path.abspath')
    def test_cd_success(self, mock_abspath, mock_chdir, cd_cmd):
        test_dir = "/test/directory"
        mock_abspath.return_value = test_dir
        
        result = cd_cmd(["valid_dir"])
        
        mock_chdir.assert_called_once_with("valid_dir")
        mock_abspath.assert_called_once_with(os.curdir)
        assert result == f"{test_dir}\n"

    @patch('os.chdir')
    def test_cd_file_not_found(self, mock_chdir, cd_cmd):
        mock_chdir.side_effect = FileNotFoundError(2, "No such directory")
        to_dir = "nonexistent_dir"
        
        result = cd_cmd([to_dir])
        
        mock_chdir.assert_called_once_with(to_dir)
        assert result == f"cd: {to_dir}: No such directory\n"

    @patch('os.chdir')
    def test_cd_not_a_directory(self, mock_chdir, cd_cmd):
        mock_chdir.side_effect = NotADirectoryError(20, "Not a directory")
        to_dir = "not_a_dir"
        
        result = cd_cmd([to_dir])
        
        mock_chdir.assert_called_once_with(to_dir)
        assert result == f"cd: {to_dir}: Not a directory\n"

    @patch('os.chdir')
    def test_cd_permission_denied(self, mock_chdir, cd_cmd):
        mock_chdir.side_effect = PermissionError(13, "Permission denied")
        to_dir = "/restricted"
        
        result = cd_cmd([to_dir])
        
        mock_chdir.assert_called_once_with(to_dir)
        assert result == f"cd: {to_dir}: Permission denied\n"

    @patch('os.chdir')
    @patch('os.path.expanduser')
    @patch('os.path.abspath')
    def test_cd_no_args(self, mock_abspath, mock_expanduser, mock_chdir, cd_cmd):
        mock_expanduser.return_value = "/home/user"
        mock_abspath.return_value = "/home/user"
        
        result = cd_cmd([])
        
        mock_expanduser.assert_called_once_with("~")
        mock_chdir.assert_called_once_with("/home/user")
        mock_abspath.assert_called_once_with(os.curdir)
        assert result == "/home/user\n"

    def test_cd_too_many_args(self, cd_cmd):
        result = cd_cmd(["dir1", "dir2"])
        assert result == "cd: There are too many arguments\n"

    @patch('os.chdir')
    @patch('os.path.abspath')
    def test_cd_relative_path(self, mock_abspath, mock_chdir, cd_cmd):
        test_dir = "/current/dir/subdir"
        mock_abspath.return_value = test_dir
        
        result = cd_cmd(["subdir"])
        
        mock_chdir.assert_called_once_with("subdir")
        mock_abspath.assert_called_once_with(os.curdir)
        assert result == f"{test_dir}\n"

    @patch('os.chdir')
    @patch('os.path.abspath')
    def test_cd_special_chars_in_path(self, mock_abspath, mock_chdir, cd_cmd):
        test_dir = "/path/with spaces and $pec!al chars"
        mock_abspath.return_value = test_dir
        
        result = cd_cmd(["path with spaces and $pec!al chars"])
        
        mock_chdir.assert_called_once_with("path with spaces and $pec!al chars")
        mock_abspath.assert_called_once_with(os.curdir)
        assert result == f"{test_dir}\n"

    @patch('os.chdir')
    @patch('os.path.abspath')
    def test_cd_empty_string(self, mock_abspath, mock_chdir, cd_cmd):
        test_dir = "/home/user"
        mock_abspath.return_value = test_dir
        
        result = cd_cmd([""])
        
        mock_chdir.assert_called_once_with("")
        mock_abspath.assert_called_once_with(os.curdir)
        assert result == f"{test_dir}\n"