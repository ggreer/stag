import os
import subprocess
import sys
import threading

import sublime
import sublime_plugin

PY2 = sys.version_info < (3, 0)


class StagPromptSearchCommand(sublime_plugin.WindowCommand):
    def run(self, q=''):
        self.window.show_input_panel('Query:', q, self.on_input, None, None)

    def on_input(self, q):
        self.window.run_command('stag_search', {'q': q})


class StagSearchCommand(sublime_plugin.WindowCommand):
    def is_visible(self):
        return False

    def is_enabled(self):
        return True

    def run(self, q=''):
        ag = '/usr/local/bin/ag'
        p = self.window.folders()
        command = [ag, q]
        command += p
        print('Ag command: %s' % ' '.join(command))
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print('stdout: %s' % stdout)
        print('stderr: %s' % stderr)
        if PY2:
            v = self.window.get_output_panel('Ag')
        else:
            v = self.window.create_output_panel('Ag')
        v.run_command('stag_set_view', {'data': stdout})


# The new ST3 plugin API sucks
class StagSetView(sublime_plugin.TextCommand):
    def run(self, edit, data, *args, **kwargs):
        size = self.view.size()
        self.view.set_read_only(False)
        self.view.insert(edit, size, data)
        self.view.set_read_only(True)
        # TODO: this scrolling is lame and centers text :/
        self.view.show(size)

    def is_visible(self):
        return False

    def is_enabled(self):
        return True

    def description(self):
        return


class StagOpenSettingsCommand(sublime_plugin.WindowCommand):
    def run(self):
        window = sublime.active_window()
        if window:
            window.open_file()
