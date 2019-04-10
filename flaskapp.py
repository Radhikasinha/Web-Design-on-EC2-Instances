def upload():
    return render_template('uploads.html')

@app.route('/upload', methods=['GET', 'POST'])

def upload_file():
    message="File Uploaded Successfully"

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            message1="Please select a file"
        file1=request.form.get(file)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fileuploading=True
            flash('You were successfully logged in')
            mylist = os.listdir(UPLOAD_FOLDER)

    return render_template('uploadedsucc.html', message=message,
                                    mylist=mylist, filename=filename)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/uploads/delete/<filename>', methods=['GET','POST'])
def deletefile(filename):
    message1="File Deleted Successfully"

    for f in os.listdir(BACKUP_FOLDER):
        if f == filename:
            os.remove(os.path.join(app.config['BACKUP_FOLDER'], f))
    shutil.move((os.path.join(app.config['UPLOAD_FOLDER'], filename)),app.config['BACKUP_FOLDER'])
    mylist = os.listdir(UPLOAD_FOLDER)
    return render_template('deletedsucc.html', message1=message1, mylist=mylist)
@app.route('/uploads/delete/retrieve', methods=['GET','POST'])
def retrieve_file():
    mylist1 = os.listdir(BACKUP_FOLDER)

    mylist = os.listdir(UPLOAD_FOLDER)

    files = []


    for f1 in mylist1:
        for f in mylist:
              if f1 == f:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))

        files.append(f1)

        shutil.move((os.path.join(app.config['BACKUP_FOLDER'], f1)),app.config['UPLOAD_FOLDER'] )

    return render_template('retrieve.html', mylist1=mylist1, files=files)

@app.route('/uploads/display', methods=['GET', 'POST'])
def display_file():
    for f1 in os.listdir(UPLOAD_FOLDER):
        now = time.time()
        cutoff = now - (5*60)
        stat = os.stat(os.path.join(app.config['UPLOAD_FOLDER'], f1))
        if stat.st_ctime < cutoff:
          for f in os.listdir(BACKUP_FOLDER):
             if f == f1:
                os.remove(os.path.join(app.config['BACKUP_FOLDER'], f))
          shutil.move((os.path.join(app.config['UPLOAD_FOLDER'], f1)),app.config['BACKUP_FOLDER'])
    mylist= os.listdir(UPLOAD_FOLDER)
    return render_template('display.html', mylist=mylist)


@app.route('/uploads/propertie<filename>', methods=['GET', 'POST'])
def property(filename):
    filename=filename
    Filecreationtime="File Creation Time"
    FileSize="File Size"
    LastModification = "Last Modification"
    Paper = "Paper Size"
    PageSize = []
    size1=os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    createdtime= time.ctime(os.path.getctime(os.path.join(app.config['UPLOAD_FOLDER'],filename)))
    lastmod= time.ctime(os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'],filename)))
    mylist=os.listdir(UPLOAD_FOLDER)
    if filename.endswith(".pdf"):
        input1 = PdfFileReader(open((os.path.join(app.config['UPLOAD_FOLDER'],filename)), 'rb'))
        PageSize=input1.getPage(0).mediaBox
    else:
        im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        PageSize = im.size
        AverageMeanOfRGB = np.array(im).mean(axis=(0,1))
    return render_template('properties.html', mylist=mylist,Paper=Paper, size1=size1,createdtime=createdtime,lastmod=lastmod,Filecreationtime=Filecreationtime,FileSize=FileSize, LastModification = LastModification, PageSize = PageSize, AverageMeanOfRGB=AverageMeanOfRGB,filename=filename)


    if __name__ == '__main__':
        app.run(debug=True)
