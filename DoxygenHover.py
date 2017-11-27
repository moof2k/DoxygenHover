import sublime
import sublime_plugin
import re
import os

class DoxygenHover(sublime_plugin.EventListener):

  def on_hover(self, view, point, hover_zone):
    if hover_zone == sublime.HOVER_TEXT:

      # Lookup word under hover point.
      word = view.substr(view.word(point))

      # Find all references to symbol in open files and index.
      symbols_index = view.window().lookup_symbol_in_index(word)
      symbols_files = view.window().lookup_symbol_in_open_files(word)
      symbols = set(symbols_files) | set(symbols_index)

      popup = ''

      for s in symbols:
        description = self.read_description_clang(s[0], s[2])

        if description:
          popup += '<i><a href="' + s[0] + ':' + str(s[2][0]) + '">'
          popup +=  s[1] + ':' + str(s[2][0]) + '</a></i><br>'
          popup += description.replace('\n', '<br>')
          popup += '<br><br>'

      def on_navigate(href):
        view.window().open_file(href, sublime.ENCODED_POSITION)

      if popup != '':
        view.show_popup(popup, sublime.HIDE_ON_MOUSE_MOVE_AWAY, point, \
          900, 600, on_navigate)

  def read_description_primitive(self, filename, loc):
    regex_string = '[:;\{\}]'

    with open(filename) as f:
      content = f.read().splitlines()

      line = loc[0] - 1
      description = '  ' + content[line].strip()

      # Grab everything before the definition.
      l = line - 1
      while not re.search(regex_string, content[l]) and content[l].strip() != '':
        description = '  ' + content[l].strip() + "\n" + description
        l = l - 1

      description = description.replace('&', '&amp;')
      description = description.replace('<', '&lt;')
      return description

    return Null

  def read_description_clang(self, filename, loc):
    print_comment = os.path.dirname(os.path.realpath(__file__)) + "/print_comment.py"
    print_comment = print_comment + " " + filename + " " + str(loc[0]) + " " + str(loc[1]) 
    comment = os.popen(print_comment).read()


    regex_string = '[:;\{\}]'

    with open(filename) as f:
      content = f.read().splitlines()

      line = loc[0] - 1
      description = '  ' + content[line].strip()

      description = comment + description

      description = description.replace('&', '&amp;')
      description = description.replace('<', '&lt;')
      return description

    return Null




