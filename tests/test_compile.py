from unv import compile

def test_inline_comment():
    assert (
        compile(
            """
# This is an inline comment
"""
        )
        == "\n\n"
    )
