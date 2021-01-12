@echo off
"C:\ProgramData\Anaconda3\pythonw.exe" "F:\Desktop\excuter\download_csv.py"

"C:\ProgramData\Anaconda3\pythonw.exe" "F:\Desktop\excuter\pay_count.py"

echo %DATE %TIME END >> F:\Desktop\excuter\request.log

exit  
