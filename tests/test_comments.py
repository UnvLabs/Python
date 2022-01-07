from unv import compile


def test_inline_comment():
    assert (
        compile(
            """
import print from 'standard'

#This is a comment
print("Hello, World!")
"""
        )
        == """
from standard import print


print("Hello, World!")
"""
    )
    assert (
        compile(
            """
import print from 'standard'

print("Hello, World!") #This is a comment
"""
        )
        == """
from standard import print

print("Hello, World!") 
"""
    )
    assert (
        compile(
            """
import print from 'standard'


print("Cheers, Mate!")
"""
        )
        == """
from standard import print


print("Cheers, Mate!")
"""
    )


def test_block_comment():
    assert (
        compile(
            """
import print from 'standard'

#This is a comment
#written in
#more than just one line
print("Hello, World!")
"""
        )
        == """
from standard import print




print("Hello, World!")
"""
    )
    assert (
        compile(
            """
import print from 'standard'

###
This is a comment
written in
more than just one line
###
print("Hello, World!")
"""
        )
        == """
from standard import print


print("Hello, World!")
"""
    )
