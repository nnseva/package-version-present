import io
import unittest
from unittest import mock

import package_version_present


class Test(unittest.TestCase):
    def test_help(self):
        """Test default help output"""
        stdout = io.StringIO()
        with mock.patch('sys.stdout', stdout):
            package_version_present.main(['package_version_present_test'])
        output = stdout.getvalue()
        self.assertIn('package_version_present_test', output)

        with self.assertRaises(SystemExit):  # The help action calls sys.exit()
            stdout = io.StringIO()
            with mock.patch('sys.stdout', stdout):
                package_version_present.main(['package_version_present_test', '--help'])
            output = stdout.getvalue()
            self.assertIn('package_version_present_test', output)

    def test_default(self):
        """Test the default call without any additional params"""
        with mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'')
            )
        )) as cp:
            ret = package_version_present.main(['package_version_present_test', 'a', 'b'])
        cp.assert_called_with('https://pypi.org/simple/a/')

        with mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Links for a</title>
  </head>
  <body>
    <h1>Links for a</h1>
    <a href="https://files.pythonhosted.org/packages/a4/XX/a-0.0.1a1.tar.gz" >a-0.0.1a1.tar.gz</a><br />
  </body>
</html>
<!--SERIAL 21585523-->
                ''')
            )
        )) as cp:
            ret = package_version_present.main(['package_version_present_test', 'a', '0.0.1a2'])
        cp.assert_called_with('https://pypi.org/simple/a/')
        self.assertEqual(ret, 1)

        with mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Links for a</title>
  </head>
  <body>
    <h1>Links for a</h1>
    <a href="https://files.pythonhosted.org/packages/a4/XX/a-0.0.1a1.tar.gz" >a-0.0.1a1.tar.gz</a><br />
  </body>
</html>
<!--SERIAL 21585523-->
                ''')
            )
        )) as cp:
            ret = package_version_present.main(['package_version_present_test', 'a', '0.0.1a1'])
        cp.assert_called_with('https://pypi.org/simple/a/')
        self.assertEqual(ret, 0)

    def test_html_not_xml(self):
        """Test the default call with the content returned by the API as HTML, not XML"""
        with mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Links for a</title>
  </head>
  <body>
    <h1>Links for a</h1>
    <a href="https://files.pythonhosted.org/packages/a4/XX/a-0.0.1a1.tar.gz" >a-0.0.1a1.tar.gz</a><br>
  </body>
</html>
<!--SERIAL 21585523-->
                ''')
            )
        )) as cp:
            ret = package_version_present.main(['package_version_present_test', 'a', '0.0.1a2'])
        cp.assert_called_with('https://pypi.org/simple/a/')
        self.assertEqual(ret, 1)

        with mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Links for a</title>
  </head>
  <body>
    <h1>Links for a</h1>
    <a href="https://files.pythonhosted.org/packages/a4/XX/a-0.0.1a1.tar.gz" >a-0.0.1a1.tar.gz</a><br>
  </body>
</html>
<!--SERIAL 21585523-->
                ''')
            )
        )) as cp:
            ret = package_version_present.main(['package_version_present_test', 'a', '0.0.1a1'])
        cp.assert_called_with('https://pypi.org/simple/a/')
        self.assertEqual(ret, 0)

    def test_request_params(self):
        """Test the call with params for the request"""
        with mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'')
            )
        )) as cp:
            package_version_present.main(['package_version_present_test', 'a', 'b', '-R', 'https://qq.ww'])
        cp.assert_called_with('https://qq.ww/simple/a/')

        with mock.patch('urllib.request.build_opener', mock.MagicMock()) as od:
            package_version_present.main([
                'package_version_present_test', 'a', 'b', '-R', 'https://qq.ww', '-U', 'test-user', '-P', 'test-pass'
            ])
        auth = od.call_args[0][0]
        self.assertEqual(auth.passwd.find_user_password(None, 'https://qq.ww'), ('test-user', 'test-pass'))

    def test_return_params(self):
        """Test the call with params for the return values"""
        with mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Links for a</title>
  </head>
  <body>
    <h1>Links for a</h1>
    <a href="https://files.pythonhosted.org/packages/a4/XX/a-0.0.1a1.tar.gz" >a-0.0.1a1.tar.gz</a><br />
  </body>
</html>
<!--SERIAL 21585523-->
                ''')
            )
        )):
            ret = package_version_present.main(['package_version_present_test', 'a', '0.0.1a1', '-E'])
        self.assertEqual(ret, 0)

        with mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Links for a</title>
  </head>
  <body>
    <h1>Links for a</h1>
    <a href="https://files.pythonhosted.org/packages/a4/XX/a-0.0.1a1.tar.gz" >a-0.0.1a1.tar.gz</a><br />
  </body>
</html>
<!--SERIAL 21585523-->
                ''')
            )
        )):
            ret = package_version_present.main(['package_version_present_test', 'a', '0.0.1a2', '-E'])
        self.assertEqual(ret, 0)

        with mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Links for a</title>
  </head>
  <body>
    <h1>Links for a</h1>
    <a href="https://files.pythonhosted.org/packages/a4/XX/a-0.0.1a1.tar.gz" >a-0.0.1a1.tar.gz</a><br />
  </body>
</html>
<!--SERIAL 21585523-->
                ''')
            )
        )):
            ret = package_version_present.main(['package_version_present_test', 'a', '0.0.1a1', '-X'])
        self.assertEqual(ret, 1)

        with mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Links for a</title>
  </head>
  <body>
    <h1>Links for a</h1>
    <a href="https://files.pythonhosted.org/packages/a4/XX/a-0.0.1a1.tar.gz" >a-0.0.1a1.tar.gz</a><br />
  </body>
</html>
<!--SERIAL 21585523-->
                ''')
            )
        )):
            ret = package_version_present.main(['package_version_present_test', 'a', '0.0.1a2', '-X'])
        self.assertEqual(ret, 0)

        stdout = io.StringIO()
        with mock.patch('sys.stdout', stdout), mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Links for a</title>
  </head>
  <body>
    <h1>Links for a</h1>
    <a href="https://files.pythonhosted.org/packages/a4/XX/a-0.0.1a1.tar.gz" >a-0.0.1a1.tar.gz</a><br />
  </body>
</html>
<!--SERIAL 21585523-->
                ''')
            )
        )):
            ret = package_version_present.main(['package_version_present_test', 'a', '0.0.1a1', '-T'])
        self.assertEqual(ret, 0)
        self.assertEqual(stdout.getvalue().strip(), 'TRUE')

        stdout = io.StringIO()
        with mock.patch('sys.stdout', stdout), mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Links for a</title>
  </head>
  <body>
    <h1>Links for a</h1>
    <a href="https://files.pythonhosted.org/packages/a4/XX/a-0.0.1a1.tar.gz" >a-0.0.1a1.tar.gz</a><br />
  </body>
</html>
<!--SERIAL 21585523-->
                ''')
            )
        )):
            ret = package_version_present.main(['package_version_present_test', 'a', '0.0.1a2', '-T'])
        self.assertEqual(ret, 1)
        self.assertEqual(stdout.getvalue().strip(), 'FALSE')

    def test_presize_versions(self):
        """Test presize versions with different parts"""
        with mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Links for a</title>
  </head>
  <body>
    <h1>Links for a</h1>
    <a href="https://files.pythonhosted.org/packages/a4/XX/a-0.0.1a1.tar.gz" >a-0.0.1a1.tar.gz</a><br />
  </body>
</html>
<!--SERIAL 21585523-->
                ''')
            )
        )) as cp:
            ret = package_version_present.main(['package_version_present_test', 'a', '0.0.1a'])
        cp.assert_called_with('https://pypi.org/simple/a/')
        self.assertEqual(ret, 1)

        with mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Links for a</title>
  </head>
  <body>
    <h1>Links for a</h1>
    <a href="https://files.pythonhosted.org/packages/a4/XX/a-0.0.1a1.tar.gz" >a-0.0.1a1.tar.gz</a><br />
  </body>
</html>
<!--SERIAL 21585523-->
                ''')
            )
        )) as cp:
            ret = package_version_present.main(['package_version_present_test', 'a', '0.0.1a11'])
        cp.assert_called_with('https://pypi.org/simple/a/')
        self.assertEqual(ret, 1)

        with mock.patch('urllib.request.OpenerDirector.open', mock.MagicMock(
            return_value=mock.MagicMock(
                read=mock.MagicMock(return_value=b'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Links for a</title>
  </head>
  <body>
    <h1>Links for a</h1>
    <a href="https://files.pythonhosted.org/packages/a4/XX/a-0.0.1a1.tar.gz" >a-0.0.1a1.tar.gz</a><br />
  </body>
</html>
<!--SERIAL 21585523-->
                ''')
            )
        )) as cp:
            ret = package_version_present.main(['package_version_present_test', 'a', '.0.1a1'])
        cp.assert_called_with('https://pypi.org/simple/a/')
        self.assertEqual(ret, 1)
