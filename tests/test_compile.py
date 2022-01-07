from unv import compile


def test_inline_comment():
    assert (
        compile(
            """
import print from 'standard'

print("Hello, World!")
"""
        )
        == """
from standard import print

print("Hello, World!")
"""
    )
