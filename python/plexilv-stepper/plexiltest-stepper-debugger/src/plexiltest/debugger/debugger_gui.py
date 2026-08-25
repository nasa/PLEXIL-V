import argparse
import tkinter as tk
import tkinter.font as tkfont
from tkinter import scrolledtext, messagebox, filedialog
from pprint import PrettyPrinter
from contextlib import contextmanager

from ..shared import extract_elements_from_script
from ..shared import is_initial_state_element
from ..shared import convert_script_element_to_xml
from ..shared import ExecutiveParsingError
from ..shared import ExecutiveError
from ..shared import MultipleInitialStateError
from ..shared import PLEXILTest
from ..shared import ScriptParsingError

# ==========================================
# Auxiliary functions and classes
# ==========================================

def pprint_state(state):
    pp = PrettyPrinter(indent=4, width=80, compact=False)
    nodes_str = '\n'.join(f"  {k}: {pp.pformat(v)}"
                          for k, v in state['nodes'].items())
    vars_str = '\n'.join(f"  {k}: {pp.pformat(v)}"
                         for k, v in state['variables'].items())
    return 'Nodes:\n' + nodes_str + '\n\nVariables:\n' + vars_str


# ==========================================
# MODEL
# ==========================================
class DebuggerModel:
    def __init__(self, plan_file, script_file, library_names=[], library_paths=[]):
        self.plexiltest = PLEXILTest(plan_file, library_names, library_paths)

        self.input_initial_state, self.input_script_items = \
            extract_elements_from_script(script_file)
        self.executable_items = []
        if self.input_initial_state:
            self.executable_items.append(self.input_initial_state)
        self.executable_items.extend(self.input_script_items)

        self.input_script_index = 0
        self.initial_state_done = False
        self.output_initial_state = ''
        self.output_script_items = []

    def get_current_executable_item(self):
        if self.input_script_index < len(self.executable_items):
            return self.executable_items[self.input_script_index]
        return None

    def construct_output_script(self):
        output = ''
        if len(self.output_initial_state) > 0:
            output += self.output_initial_state + '\n\n'
        output += 'script {\n'
        for item in self.output_script_items:
            output += '  ' + item + '\n'
        output += '}\n'
        return output

    def step_initial_state_if_needed(self):
        if not self.initial_state_done:
            self.plexiltest.step('<InitialState/>')

    def step_plexil(self, xml_element):
        self.plexiltest.step(xml_element)

    def add_to_output_script(self, item):
        if is_initial_state_element(item):
            self.output_initial_state = item
        else:
            self.output_script_items.append(item)
        self.initial_state_done = True

    def get_formatted_state(self):
        return self.plexiltest.pprint_str()

    def needs_step(self):
        return self.plexiltest.needs_step()


# ==========================================
# VIEW
# ==========================================
class DebuggerView:
    def __init__(self, root):
        self.root = root
        self.root.title("PLEXIL Debugger")

        # Make a zoomable font
        self.current_font_size = 12
        self.zoomable_font = tkfont.Font(family="TkDefaultFont",
                                         size=self.current_font_size)
        self.root.bind("<Control-plus>",
                       lambda event: self.increase_zoomable_font_size())
        self.root.bind("<Control-minus>",
                       lambda event: self.decrease_zoomable_font_size())

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1, minsize=300)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=4)
        self.root.rowconfigure(1, weight=0)
        self.root.rowconfigure(2, weight=1)

        # Panel : Executive State (Row 0, Col 0 of 2)
        frame1 = tk.LabelFrame(self.root, text="Executive State")
        frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.exec_state_display = scrolledtext.ScrolledText(
            frame1,
            wrap=tk.WORD,
            state='disabled',
            font=self.zoomable_font
        )
        self.exec_state_display.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5, pady=5
        )

        # Panel: Input Script (Row 0, Col 1 of 2)
        frame2 = tk.LabelFrame(self.root, text="Input Script")
        frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.input_script_display = scrolledtext.ScrolledText(
            frame2,
            wrap=tk.WORD,
            state='disabled',
            font=self.zoomable_font
        )
        self.input_script_display.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5, pady=5
        )
        self.input_script_display.tag_config(
            "highlight",
            background="yellow",
            foreground="black"
        )
        self.input_script_display.tag_raise("sel")

        input_script_controls = tk.Frame(frame2)
        input_script_controls.pack(fill=tk.X, pady=5)
        self.btn_execute = tk.Button(input_script_controls, text="Execute")
        self.btn_execute.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.btn_go_down = tk.Button(input_script_controls, text="Go Down")
        self.btn_go_down.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.btn_go_up = tk.Button(input_script_controls, text="Go Up")
        self.btn_go_up.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Panel: Output Script (Row 0, Col 2 of 2)
        frame3 = tk.LabelFrame(self.root, text="Output Script")
        frame3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.output_script_display = scrolledtext.ScrolledText(
            frame3,
            wrap=tk.WORD,
            state='disabled',
            font=self.zoomable_font
        )
        self.output_script_display.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5, pady=5
        )
        self.btn_save = tk.Button(frame3, text="Save Script")
        self.btn_save.pack(
            side=tk.BOTTOM,
            fill=tk.X,
            padx=5, pady=(0, 5)
        )

        # Indicator: PLEXIL Exec Macro Step Status (Row 1)
        self.exec_needs_step_frame = tk.Frame(self.root)
        self.exec_needs_step_frame.grid(
            row=1, column=0,
            columnspan=3,
            padx=10, pady=5,
            sticky="ew"
        )
        self.exec_needs_step_label = tk.Label(
            self.exec_needs_step_frame,
            text="Exec needs step?: Intializing ...",
            font=("Arial", 14, "bold")
        )
        self.exec_needs_step_label.pack()

        # Panel: User Input (Row 2)
        frame4 = tk.LabelFrame(self.root, text="Enter Plexilscript Element")
        frame4.grid(
            row=2, column=0,
            columnspan=3,
            padx=10, pady=10,
            sticky="nsew"
        )
        self.input_area = scrolledtext.ScrolledText(
            frame4,
            wrap=tk.WORD,
            height=5,
            font=self.zoomable_font
        )
        self.input_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.btn_submit = tk.Button(frame4, text="Submit")
        self.btn_submit.pack(pady=5)

        self.script_input_element_indices = []

    # --- Methods to Bind Buttons ---
    def bind_execute(self, callback): self.btn_execute.config(command=callback)
    def bind_go_down(self, callback): self.btn_go_down.config(command=callback)
    def bind_go_up(self, callback): self.btn_go_up.config(command=callback)
    def bind_save(self, callback): self.btn_save.config(command=callback)
    def bind_submit(self, callback): self.btn_submit.config(command=callback)

    # --- Methods to Update View ---
    def increase_zoomable_font_size(self):
        if self.current_font_size < 42:
            self.current_font_size += 2
            self.zoomable_font.config(size=self.current_font_size)

    def decrease_zoomable_font_size(self):
        if self.current_font_size > 8:
            self.current_font_size -= 2
            self.zoomable_font.config(size=self.current_font_size)

    def update_panel_text(self, widget, text):
        widget.config(state='normal')
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)
        widget.see(tk.END)
        widget.config(state='disabled')

    def set_exec_state(self, text):
        self.update_panel_text(self.exec_state_display, text)

    def set_output_script(self, text):
        self.update_panel_text(self.output_script_display, text)

    def set_needs_step_indicator(self, needs_step):
        val = "Yes" if needs_step else "No"
        self.exec_needs_step_label.config(text=f"Exec needs step?: {val}")

    def get_user_input(self):
        return self.input_area.get("1.0", "end-1c")

    def clear_user_input(self):
        self.input_area.delete("1.0", tk.END)

    def disable_input_script_controls(self):
        self.btn_execute.config(state='disabled')
        self.btn_submit.config(state='disabled')

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_info(self, title, message):
        messagebox.showinfo(title, message)

    def populate_input_script(self, initial_state, script_items):
        self.input_script_display.config(state='normal')
        self.input_script_display.delete("1.0", tk.END)
        self.script_input_element_indices = []

        if initial_state:
            start_idx = self.input_script_display.index("end-1c")
            self.input_script_display.insert(tk.END, initial_state + "\n\n")
            end_idx = self.input_script_display.index("end-1c")
            self.script_input_element_indices.append((start_idx, end_idx))

        if script_items:
            self.input_script_display.insert(tk.END, "script {\n")
            for item in script_items:
                start_idx = self.input_script_display.index("end-1c")
                indented_item = "  " + item.strip().replace("\n", "\n  ") + "\n"
                self.input_script_display.insert(tk.END, indented_item)
                self.script_input_element_indices.append(
                    (start_idx, self.input_script_display.index("end-1c"))
                )
            self.input_script_display.insert(tk.END, "}\n")

        self.input_script_display.config(state='disabled')

    def update_highlight(self, index):
        self.input_script_display.tag_remove("highlight", "1.0", tk.END)
        if index < len(self.script_input_element_indices):
            start, end = self.script_input_element_indices[index]
            self.input_script_display.tag_add("highlight", start, end)
            self.input_script_display.see(start)


# ==========================================
# CONTROLLER
# ==========================================
class DebuggerController:
    def __init__(
            self,
            root,
            plan_file, script_file,
            library_names, library_paths
        ):
        self.model = DebuggerModel(
            plan_file,
            script_file,
            library_names,
            library_paths
        )
        self.view = DebuggerView(root)

        # Bind View events to Controller methods
        self.view.bind_execute(self.execute_script_element)
        self.view.bind_go_down(self.go_down)
        self.view.bind_go_up(self.go_up)
        self.view.bind_submit(self.execute_user_input)
        self.view.bind_save(self.save_output_script)

        # Initial View Setup
        self.view.populate_input_script(self.model.input_initial_state,
                                        self.model.input_script_items)
        self.view.update_highlight(self.model.input_script_index)

    def refresh_displays(self):
        """Updates all displays relying on the current state of the model."""
        self.view.set_exec_state(self.model.get_formatted_state())
        self.view.set_output_script(self.model.construct_output_script())
        self.view.set_needs_step_indicator(self.model.needs_step())

    def _execute_element(self, element):
        if self.model.initial_state_done and is_initial_state_element(element):
            raise MultipleInitialStateError

        if not is_initial_state_element(element):
            self.model.step_initial_state_if_needed()
        xml_element = convert_script_element_to_xml(element)
        self.model.step_plexil(xml_element)
        self.model.add_to_output_script(element)

    @contextmanager
    def _handle_execution_errors(self):
        try:
            yield
        except MultipleInitialStateError:
            self.view.show_error("Input Error",
                                 "Initial state input rejected. "
                                 "Multiple initial states are not allowed.")
        except ScriptParsingError as e:
            self.view.show_error("PlexilScript Error",
                                 f"Ill-formatted input:\n{e}")
        except ExecutiveParsingError as e:
            self.view.show_error("Input Error",
                                 f"Rejected input:\n{e}")
        except ExecutiveError as e:
            self.view.show_error("PLEXIL Exec Error",
                                 f"Disabling scripting due to error:\n{e}")
            self.view.disable_input_script_controls()
        except Exception as e:
            self.view.show_error("Uncategorized Error",
                                 f"Disabling scripting due to error:\n{e}")
            self.view.disable_input_script_controls()

    def execute_script_element(self):
        current_element = self.model.get_current_executable_item()
        if not current_element:
            return
        with self._handle_execution_errors():
            self._execute_element(current_element)
            if self.model.input_script_index < len(self.model.executable_items) - 1:
                self.model.input_script_index += 1
            self.view.update_highlight(self.model.input_script_index)
            self.refresh_displays()

    def execute_user_input(self):
        user_pst_input = self.view.get_user_input()
        if not user_pst_input:
            return
        with self._handle_execution_errors():
            self._execute_element(user_pst_input)
            if self.model.input_script_index < len(self.model.executable_items) - 1:
                self.model.input_script_index += 1
            self.view.update_highlight(self.model.input_script_index)
            self.refresh_displays()

        self.view.clear_user_input()

    def go_down(self):
        if self.model.input_script_index < len(self.model.executable_items) - 1:
            self.model.input_script_index += 1
            self.view.update_highlight(self.model.input_script_index)

    def go_up(self):
        can_go_up = self.model.input_script_index > 1 \
            or (self.model.input_script_index > 0 and not self.model.initial_state_done)
        if can_go_up:
            self.model.input_script_index -= 1
            self.view.update_highlight(self.model.input_script_index)

    def save_output_script(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Script As",
            defaultextension=".txt",
            filetypes=[
                ("Plexilscript Files", "*.pst"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        if not file_path:
            return
        try:
            output_text = self.model.construct_output_script()
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(output_text)
            self.view.show_info(
                "Success",
                f"Output script successfully saved to:\n{file_path}"
            )
        except Exception as e:
            self.view.show_error("Error", f"Failed to save file:\n{e}")


# ==========================================
# MAIN
# ==========================================
def main():
    parser = argparse.ArgumentParser(description="PLEXIL Debugger GUI")
    parser.add_argument('-p','--plan', help="Path to the compiled plan file (.plx)", type=str, required=True)
    parser.add_argument('-s','--script', help="Path to the uncompiled script file (.pst)", type=str, required=True)
    parser.add_argument('--library_names', type=str, nargs='+', default=[])
    parser.add_argument('--library_paths', type=str, nargs='+', default=[])
    args = parser.parse_args()

    main_window = tk.Tk()
    main_window.geometry("1100x800")

    try:
        app = DebuggerController(
            main_window,
            args.plan,
            args.script,
            args.library_names,
            args.library_paths
        )
    except ScriptParsingError as e:
        print(f"\nScript error: {e}\n")
        return

    main_window.mainloop()

if __name__ == "__main__":
    main()