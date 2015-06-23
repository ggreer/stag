# coding: utf-8

# import os
import subprocess

import sublime
import sublime_plugin


class StagPromptSearchCommand(sublime_plugin.WindowCommand):
    def run(self, q='', p=None):
        self.window.show_input_panel('Query:', q, self.on_input, None, None)

    def on_input(self, q):
        self.window.run_command('stag_search', {
            'q': q,
        })


class StagSearchCommand(sublime_plugin.WindowCommand):
    def is_visible(self):
        return False

    def is_enabled(self):
        return True

    def get_output_panel(self):
        if hasattr(self, 'output_panel'):
            return self.output_panel
        v = self.window.create_output_panel('Ag')
        v.set_scratch(True)
        v.set_name('STAg')
        self.output_panel = v
        return self.output_panel

    def run(self, q='', p=None):
        v = self.get_output_panel()

        p = p or self.window.folders()
        if not p:
            print('WTF? No paths to search')
            v.run_command('stag_set_view', {'data': 'WTF? No paths to search.'})
            return

        # TODO: make this a setting
        ag = '/usr/local/bin/ag'
        command = [ag, '-C', '--group', q]
        print('Ag command: %s' % ' '.join(command))
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=p)
        stdout, stderr = p.communicate()
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
        print('stdout: %s' % stdout)
        print('stderr: %s' % stderr)
        v.run_command('stag_set_view', {
            'stdout': stdout,
            'stderr': stderr,
        })
        self.window.run_command('show_panel', {'panel': 'output.Ag'})


# The new ST3 plugin API sucks
class StagSetView(sublime_plugin.TextCommand):
    def run(self, edit, stdout, stderr, *args, **kwargs):
        size = self.view.size()
        self.view.set_read_only(False)
        self.view.insert(edit, size, stdout)
        self.view.set_read_only(True)
        self.view.set_scratch(True)
        self.view.set_name('STAg')
        self.view.show(size)

    def is_visible(self):
        return False

    def is_enabled(self):
        return True

    def description(self):
        return


class StagClick(sublime_plugin.TextCommand):
    def run(self, *args, **kwargs):
        v = self.view
        if v is None or v.name() != 'STAg':
            return
        sel = v.sel()
        # TODO: parse path and open it


class StagOpenSettingsCommand(sublime_plugin.WindowCommand):
    def run(self):
        window = sublime.active_window()
        if window:
            window.open_file()
