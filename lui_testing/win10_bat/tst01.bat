set ini_dir=%cd%
set full_sting=python %ini_dir%\src\all_local.py windows_exe=true
echo %full_sting% > run_me.bat
echo: use run_me.bat to launch Dui2
