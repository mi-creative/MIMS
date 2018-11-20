from cx_Freeze import setup,Executable
import sys

includefiles = ['darkstyle.qss', 'ui', 'html', 'icons']
includes = []
excludes = []
packages = ['numpy']

build_exe_options = {'includes':includes,'excludes':excludes,'packages':packages,'include_files':includefiles}

company_name = 'IANG'
product_name = 'Mass Interaction Model Scripter (MIMS)'

base = None
if sys.platform == "win32":
    base = "Win32GUI"

bdist_msi_options = {
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name)
    }

exe = Executable(script='MIMS_main.py',
                 base=base,
                 shortcutName="MIMS",
                shortcutDir="DesktopFolder",
                 # icon='MyGui.ico',
                )

setup(
    name = 'MIMS',
    version = '0.1',
    description = 'A Mass Interaction Model Scripter for Sound Synthesis',
    author = 'James Leonard',
    author_email = 'james.leonard@gipsa-lab.fr',
    options = {'build_exe': build_exe_options, 'bdist_msi' : bdist_msi_options},
    executables = [exe]
)
