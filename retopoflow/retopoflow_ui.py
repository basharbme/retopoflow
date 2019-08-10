'''
Copyright (C) 2019 CG Cookie
http://cgcookie.com
hello@cgcookie.com

Created by Jonathan Denning, Jonathan Williamson, and Patrick Moore

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os

import bpy
import bmesh

from ..addon_common.common.globals import Globals
from ..addon_common.common import ui
from ..addon_common.common.ui_styling import load_defaultstylings

class RetopoFlow_UI:
    def setup_ui(self):
        self.manipulator_hide()
        self.panels_hide()
        self.overlays_hide()
        self.region_darken()
        self.header_text_set('RetopoFlow')
        self.target.hide_viewport = True

        # load ui.css
        path = os.path.join(os.path.dirname(__file__), '..', 'config', 'ui.css')
        try:
            Globals.ui_draw.load_stylesheet(path)
        except AssertionError as e:
            # TODO: show proper dialog to user here!!
            print('could not load stylesheet "%s"' % path)
            print(e)

        def setup_main_ui():
            self.ui_main = ui.framed_dialog(label='RetopoFlow 2.1.0α', id="maindialog", parent=self.document.body)

            # tools
            ui_tools = ui.div(id="tools", parent=self.ui_main)
            count = 0
            def add_tool(lbl, img):
                nonlocal count
                count += 1
                radio = ui.input_radio(value=lbl.lower(), name="tool", classes="tool", checked=(count==1), parent=ui_tools)
                ui.img(src=img, parent=radio, style="width:20px; height:20px; border:0px; padding:0px; margin:0px")
                ui.label(innerText=lbl, parent=radio, style="padding:2px 0px; margin:0px; margin-left: 4px")
            add_tool("Contours",   "contours_32.png")
            add_tool("PolyStrips", "polystrips_32.png")
            add_tool("PolyPen", "polypen_32.png")
            add_tool("Strokes", "strokes_32.png")
            add_tool("Patches", "patches_32.png")
            add_tool("Loops", "loops_32.png")
            add_tool("Relax", "relax_32.png")
            add_tool("Tweak", "tweak_32.png")

            ui.button(label='Welcome!', parent=self.ui_main)
            ui.button(label='All Help', parent=self.ui_main)
            ui.button(label='General Help', parent=self.ui_main)
            ui.button(label='Tool Help', parent=self.ui_main)
            ui.button(label='Report Issue', parent=self.ui_main)
            ui.button(label='Exit', parent=self.ui_main)


        def setup_options():
            self.ui_options = ui.framed_dialog(label='Options', id='optionsdialog', right=0, parent=self.document.body)

            ui_general = ui.collapsible(label='General', id='generaloptions', parent=self.ui_options)
            ui.button(label='Maximize Area', parent=ui_general)

            ui_target_cleaning = ui.collapsible(label='Target Cleaning', id='targetcleaning', parent=ui_general)
            ui_target_snapverts = ui.collapsible(label='Snap Verts', id='snapverts', parent=ui_target_cleaning)
            ui.button(label="All", parent=ui_target_snapverts)
            ui.button(label="Selected", parent=ui_target_snapverts)
            ui_target_removedbls = ui.collapsible(label='Remove Doubles', id='removedoubles', parent=ui_target_cleaning)
            ui.input_text(value='Distance = 0.001', parent=ui_target_removedbls)
            ui.button(label="All", parent=ui_target_removedbls)
            ui.button(label="Selected", parent=ui_target_removedbls)

            ui_target_rendering = ui.collapsible(label="Target Rendering", parent=ui_general)
            ui.input_text(value='Above = 100', parent=ui_target_rendering)
            ui.input_text(value='Below = 10', parent=ui_target_rendering)
            ui.input_text(value='Backface = 20', parent=ui_target_rendering)
            ui.input_checkbox(label='Cull Backfaces', parent=ui_target_rendering)

            ui_symmetry = ui.collapsible(label='Symmetry', id='symmetryoptions', parent=self.ui_options)

        '''
            # c = 0
            # def mouseclick(e):
            #     nonlocal c
            #     c += 1
            #     e.target.innerText = "You've clicked me %d times.\nNew lines act like spaces here, but there is text wrapping!" % c
            # def mousedblclick(e):
            #     e.target.innerText = "NO!!!!  You've double clicked me!!!!"
            #     e.target.add_pseudoclass('disabled')
            # def mousedown(e):
            #     e.target.innerText = "mouse is down!"
            # def mouseup(e):
            #     e.target.innerText = "mouse is up!"
            # def reload_stylings(e):
            #     load_defaultstylings()
            #     self.document.body.dirty_styling()
            # def width_increase(e):
            #     self.ui_main.width = self.ui_main.width_pixels + 50
            # def width_decrease(e):
            #     self.ui_main.width = self.ui_main.width_pixels - 50
            # self.ui_main.append_child(ui.img(src='contours_32.png'))
            # # self.ui_main.append_child(ui.img(src='polystrips_32.png', style='width:26px; height:26px'))
            # # self.ui_main.append_child(ui.button(label="Click on me, but do NOT double click!", on_mouseclick=mouseclick, on_mousedblclick=mousedblclick, on_mousedown=mousedown, on_mouseup=mouseup))
            # # self.ui_main.append_child(ui.button(label="FOO", style="display:block", children=[ui.button(label="BAR", style="display:block")]))
            # # self.ui_main.append_child(ui.button(id="alpha0", label="ABCDEFGHIJKLMNOPQRSTUVWXYZ 0"))
            # # self.ui_main.append_child(ui.button(id="alpha1", label="ABCDEFGHIJKLMNOPQRSTUVWXYZ 1"))
            # # self.ui_main.append_child(ui.button(id="alpha2", label="ABCDEFGHIJKLMNOPQRSTUVWXYZ 2"))
            # # self.ui_main.append_child(ui.button(id="alpha3", label="ABCDEFGHIJKLMNOPQRSTUVWXYZ 3"))
            # self.ui_main.append_child(ui.br())
            # self.ui_main.append_child(ui.button(label="Reload Styles Now", on_mouseclick=reload_stylings))
            # self.ui_main.append_child(ui.input_checkbox(label="test"))
            # self.ui_main.append_child(ui.br())
            # self.ui_main.append_child(ui.span(innerText="Options:"))
            # self.ui_main.append_child(ui.input_radio(label="A", value="A", name="option"))
            # self.ui_main.append_child(ui.input_radio(label="B", value="B", name="option"))
            # self.ui_main.append_child(ui.input_radio(label="C", value="C", name="option"))
            # # self.ui_main.append_child(ui.p(innerText="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."))
            # # self.ui_main.append_child(ui.textarea(innerText="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."))

            # self.ui_tools = ui.framed_dialog(id='toolsframe', label='Tools', parent=self.document.body)
            # #self.ui_tools = self.ui_main
            # state_p = self.ui_tools.append_child(ui.p())
            # state_p.append_child(ui.span(innerText='State:'))
            # self.state = state_p.append_child(ui.span(innerText='???'))
            # self.ui_tools.append_child(ui.p(innerText="Foo Bar Baz"))
            # ui_input = self.ui_tools.append_child(ui.input_text(id="inputtext"))
            # ui_input.value = 'Lorem   ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
            # div_width = self.ui_tools.append_child(ui.div())
            # div_width.append_child(ui.span(innerText='width:'))
            # div_width.append_child(ui.button(label='+', on_mouseclick=width_increase))
            # div_width.append_child(ui.button(label='-', on_mouseclick=width_decrease))
            # div_width.append_child(ui.button(label='=')).add_pseudoclass('disabled')
            # self.ui_tools.right = 0
            # self.ui_tools.top = 0
            # print(self.document.body.structure())
        '''

        setup_main_ui()
        setup_options()


