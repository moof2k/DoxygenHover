#!/usr/bin/python

import clang.cindex
from clang.cindex import Index, TranslationUnit, TokenKind
import sys

clang.cindex.Config.set_library_file('/usr/lib/llvm-3.8/lib/libclang.so.1')


def rangestr(x):
    return '%s:%d:%d - %s:%d:%d' % (x.start.file, x.start.line, x.start.column, x.end.file, x.end.line, x.end.column)

### Prints the comment immediately proceeding the identifier at line, col
def print_comment(filename, line, col):
    index = clang.cindex.Index.create()
    tu = index.parse(filename, args=['-x', 'c++'])

    comment = None
    for x in tu.cursor.get_tokens():
        #print x.kind
        #print x.spelling
        #print rangestr(x.extent)

        if x.kind == TokenKind.COMMENT:
            comment = x
        elif x.kind == TokenKind.PUNCTUATION and x.spelling == ';':
            comment = None
        elif x.kind == TokenKind.IDENTIFIER:
            if x.extent.start.line == line and x.extent.start.column == col:
                if comment != None:
                    print comment.spelling
                return


if __name__ == '__main__':

    if len(sys.argv) == 4:
        print_comment(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))