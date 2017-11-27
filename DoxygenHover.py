import sublime
import sublime_plugin
import re

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
        description = self.read_description(s[0], s[2])

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

  def read_description(self, filename, loc):

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
