pyinstaller -i=pyqtbrowser.ico --noconfirm ^
	--add-data=img;img ^
	--noconsole ^
	--windowed ^
	--name="pyQtBrowser" ^
	main.py 