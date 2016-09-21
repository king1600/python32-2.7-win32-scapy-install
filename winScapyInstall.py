import os, shutil
import site, sys
import errno

# setup paths
pythonPath  = site.getsitepackages()[0]
currentPath = os.getcwd()
pipPath     = os.path.join(pythonPath,"Scripts","pip.exe")
IncludePath = os.path.join(pythonPath, "include")
LibPath     = os.path.join(pythonPath, "libs")
incPath     = os.path.join(currentPath, "Include")
libPath     = os.path.join(currentPath, "Libs")
pkgPath     = os.path.join(currentPath, "packages")
mainPath    = os.path.join(currentPath, "mainfiles")

try:
	print "[*] Installing main files.."
	for f in os.listdir(mainPath):
		filepath = os.path.join(mainPath, f)
		os.system(filepath)
	print "[*] Main Installations done!\n\n"

	print "[*] Copying files to Python directory..."
	# copy files
	def copyAll(src_dir, dst_dir):
		for f in os.listdir(src_dir):
			filepath = os.path.join(src_dir, f)
			if os.path.isfile(filepath):
				dst_file = os.path.join(dst_dir, f)
				print "Copying to", dst_file
				if os.path.exists(dst_file):
					os.remove(dst_file)
				shutil.copyfile(filepath, dst_file)
			elif os.path.isdir(filepath):
				new_dir = os.path.join(dst_dir, f)
				if not os.path.exists(new_dir):
					os.makedirs(new_dir)
				copyAll(filepath, new_dir)
			else:
				pass

	# check windows version
	def is64bit():
		return "programfiles(x86)".upper() in os.environ

	# copy include files
	copyAll(incPath, IncludePath)
	copyAll(libPath, LibPath)
	if is64bit():
		print "[*] Copying 64 bit files.."
		copyAll(os.path.join(libPath, "x64"), LibPath)

	# install PyReadLine
	print "[*] Installing scapy dependencies."
	os.system(pipPath + " install --upgrade pip")
	os.system(pipPath + " install pyreadline")
	os.system(pipPath + " install numpy")
	os.system(pipPath + " install pycrypto")

	# installing packages
	print "[*] Installing packages..."
	for f in os.listdir(pkgPath):
		filepath = os.path.join(pkgPath, f)
		os.system(filepath)
	print "[*] Done!\n"

	# finally, install scapy
	print "[*] Installing Scapy..."
	os.system(pipPath + " install scapy")

	raw_input("\n\n[*~*] Scapy has been installed!")

except Exception as exc:
	raw_input("[x] Error!: " + str(exc))
