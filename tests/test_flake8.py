"""Unit tests for flake8 pytest plugin."""

import pathlib
import textwrap
from packaging import version

import pytest

from flake8 import __version__ as flake8_version

pytest_plugins = ("pytester",)


def run_pytest(testdir, *args):
    """
    Run pytest with flake8 enabled (and the enabler disabled).
    """
    return testdir.runpytest("-p", "no:enabler", "--flake8", *args)


class TestIgnores:
    """Test ignores."""

    @pytest.fixture
    def example(self, request):
        """Create a test file."""
        testdir = request.getfixturevalue("testdir")
        import sys

        print(testdir, file=sys.stderr)
        p = testdir.makepyfile("")
        p.write("class AClass:\n    pass\n       \n\n# too many spaces")
        return p

    def test_ignores(self, tmpdir):
        """Verify parsing of ignore statements."""
        from pytest_flake8 import Ignorer

        ignores = ["E203", "b/?.py E204 W205", "z.py ALL", "*.py E300"]
        ign = Ignorer(ignores)
        assert ign(tmpdir.join("a/b/x.py")) == "E203 E204 W205 E300".split()
        assert ign(tmpdir.join("a/y.py")) == "E203 E300".split()
        assert ign(tmpdir.join("a/z.py")) is None

    @pytest.mark.xfail(
        version.parse(flake8_version) >= version.parse("6.0.0"),
        reason="Requires Flake8 version earlier than 6.0.0.",
    )
    def test_default_flake8_ignores(self, testdir):
        testdir.makeini("""
            [pytest]
            markers = flake8

            [flake8]
            ignore = E203
                *.py E300
                tests/*.py ALL E203  # something
        """)
        testdir.tmpdir.ensure("xy.py")
        testdir.tmpdir.ensure("tests/hello.py")
        result = run_pytest(testdir, "-s")
        result.assert_outcomes(passed=2)
        result.stdout.fnmatch_lines([
            "*collected 2*",
            "*xy.py .*",
            "*2 passed*",
        ])

    def test_ignores_all(self, testdir):
        """Verify success when all errors are ignored."""
        testdir.makeini("""
            [pytest]
            markers = flake8
            flake8-ignore = E203
                *.py E300
                tests/*.py ALL E203 # something
        """)
        testdir.tmpdir.ensure("xy.py")
        testdir.tmpdir.ensure("tests/hello.py")
        result = run_pytest(testdir, "-s")
        result.assert_outcomes(passed=1)
        result.stdout.fnmatch_lines([
            "*collected 1*",
            "*xy.py .*",
            "*1 passed*",
        ])

    def test_w293w292(self, testdir, example):
        result = run_pytest(testdir)
        result.stdout.fnmatch_lines([
            # "*plugins*flake8*",
            "*W293*",
            "*W292*",
        ])
        result.assert_outcomes(failed=1)

    def test_mtime_caching(self, testdir, example):
        testdir.tmpdir.ensure("hello.py")
        result = run_pytest(testdir)
        result.stdout.fnmatch_lines([
            # "*plugins*flake8*",
            "*W293*",
            "*W292*",
        ])
        result.assert_outcomes(passed=1, failed=1)
        result = run_pytest(testdir)
        result.stdout.fnmatch_lines([
            "*W293*",
            "*W292*",
        ])
        result.assert_outcomes(skipped=1, failed=1)
        testdir.makeini("""
            [pytest]
            flake8-ignore = *.py W293 W292 W391
        """)
        result = run_pytest(testdir)
        result.assert_outcomes(passed=2)


def test_extensions(testdir):
    testdir.makeini("""
        [pytest]
        markers = flake8
        flake8-extensions = .py .pyx
    """)
    testdir.makefile(
        ".pyx",
        """
        @cfunc
        def f():
            pass
    """,
    )
    result = run_pytest(testdir)
    result.stdout.fnmatch_lines([
        "*collected 1*",
    ])
    result.assert_outcomes(failed=1)


def test_ok_verbose(testdir):
    p = testdir.makepyfile("""
        class AClass:
            pass
    """)
    p = p.write(p.read() + "\n")
    result = run_pytest(testdir, "--verbose")
    result.stdout.fnmatch_lines([
        "*test_ok_verbose*",
    ])
    result.assert_outcomes(passed=1)


def test_keyword_match(testdir):
    testdir.makepyfile("""
        def test_hello():
            a=[ 1,123]
            #
    """)
    result = run_pytest(testdir, "-mflake8")
    result.stdout.fnmatch_lines([
        "*E201*",
        "*1 failed*",
    ])
    result.assert_outcomes(failed=1)


def test_run_on_init_file(testdir):
    d = testdir.mkpydir("tests")
    result = run_pytest(testdir, d / "__init__.py")
    result.assert_outcomes(passed=1)


@pytest.mark.xfail("sys.platform == 'win32'")
def test_unicode_error(testdir):
    x = testdir.tmpdir.join("x.py")
    content = textwrap.dedent("""
    # coding=utf8

    accent_map = {
        u'\\xc0': 'a',  # À -> a  non-ascii comment crashes it
    }
    """).lstrip()
    x.write_text(content, encoding='utf-8')
    # result = run_pytest(testdir, x, "-s")
    # result.stdout.fnmatch_lines("*non-ascii comment*")


@pytest.mark.xfail(reason="flake8 is not properly registered as a marker")
def test_strict(testdir):
    testdir.makepyfile("")
    result = testdir.runpytest("-p", "no:enabler", "--strict", "-mflake8")
    result.assert_outcomes(passed=1)


def test_junit_classname(testdir):
    testdir.makepyfile("")
    result = run_pytest(testdir, "--junit-xml=TEST.xml")
    junit = testdir.tmpdir.join("TEST.xml")
    j_text = pathlib.Path(junit).read_text(encoding='utf-8')
    result.assert_outcomes(passed=1)
    assert 'classname=""' not in j_text
