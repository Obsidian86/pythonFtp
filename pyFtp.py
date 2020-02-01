import ftplib
import os
# www.url.com   ftpPassword  ftpUsername
from creds import mUrl, mPass, mUname

create = True

ftpCon = ftplib.FTP(mUrl, mUname, mPass)
# remote www folder
ftpCon.cwd('public_html')
# folder to upload to (project name) www/folder || 'folder name' or None
projectName = 'testupload'
# build folder
fromDirectory = os.path.join('..', '..', 'projects', 'image-gal', 'build')
# allowed file types
allowedFiles = ['.html', '.js', '.css', '.json', '.jpg', '.gif', '.txt']
# directory names to upload
allowedDirs = ['scripts', 'static', 'js', 'media', 'css']

# main function to upload files
def uploadFiles(path):
    files = os.listdir(path)
    os.chdir(path)
    for f in files:
        # test if is a file and if it is allowed
        fileTest = False
        for fType in allowedFiles:
            if fType in f:
                fileTest = True
        # test if directory and if it is allowed
        directoryTest = False
        for dName in allowedDirs:
            if dName == f:
                directoryTest = True
        if fileTest:
            print('Uploading file: ' + f + ' to ' + '-> ' + ftpCon.pwd() )
            fh = open(f, 'rb')
            ftpCon.storbinary('STOR %s' % f, fh)
            fh.close()
        elif directoryTest:
            if f not in ftpCon.nlst():
                print('Created directory: ' + f)
                ftpCon.mkd(f)
            ftpCon.cwd(f)
            uploadFiles(os.path.join('.', f))
    ftpCon.cwd('..')
    os.chdir('..')


# create folders + upload files
if create:
    print('Begin upload to ' + mUrl)
    # root (www) if false or sub folder (www/subfolder)
    if projectName:
        # create project folder if it doesn't exist
        if projectName not in ftpCon.nlst():
            print('Created directory: ' + projectName)
            ftpCon.mkd(projectName)
        ftpCon.cwd(projectName) 
    # initialize 
    uploadFiles(fromDirectory)
else:
    print('Create mode disabled')

# End session
ftpCon.quit()