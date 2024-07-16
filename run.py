import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)
app.secret_key = 'super secret key'

STUDENT_UPLOAD_FOLDER = os.path.abspath('uploads/students')
INSTRUCTOR_UPLOAD_FOLDER = os.path.abspath('uploads/instructors')

ALLOWED_EXTENSIONS = {'py', 'txt'}

app.config['STUDENT_UPLOAD_FOLDER'] = STUDENT_UPLOAD_FOLDER
app.config['INSTRUCTOR_UPLOAD_FOLDER'] = INSTRUCTOR_UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/student', methods=['GET', 'POST'])
def student_view():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['STUDENT_UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # print("file_path:", file_path)
            total_testcase=0
            test_lst=[]
            flash(f'File uploaded successfully. {file_path}')
            instructor_test = "uploads/instructors/test_cases.txt"
            instructor_code = 'uploads/instructors/'+ os.path.basename(file_path)
            if os.path.exists(instructor_code) and os.path.exists(instructor_test):
                with open(instructor_test, 'r') as input_f:
                    print("instructor_test: ",instructor_test)
                    with open('output_student.txt', 'w') as f:
                        for line in input_f:
                            args = line.rstrip().split(",")
                            print(args)
                            timeout = 60
                            test_lst.append(line)
                            try:
                                result = subprocess.run(["python", file_path, *args], capture_output=True,timeout=timeout,check=True).stdout
                                f.write(str(result, 'utf-8'))
                            except subprocess.TimeoutExpired:
                                flash(f'**warning**:Time out\n',"red")
                                break
                            except subprocess.CalledProcessError as e:
                                flash(f'**warning**:Compilation error in the submitted file\n',"red")
                                break
                with open(instructor_test, 'r') as input_f:
                    with open('output_teacher.txt', 'w') as f:
                        for line in input_f:
                            total_testcase+=1
                            args = line.rstrip().split(",")
                            print(args)
                            try:
                                result = subprocess.run(["python", instructor_code, *args], capture_output=True).stdout
                                f.write(str(result, 'utf-8'))
                            except subprocess.CalledProcessError as e:
                                print("Command failed with return code", e.returncode)      
                with open('output_student.txt', 'r') as f1, open('output_teacher.txt', 'r') as f2:
                    count = 0
                    tst_count=0
                    print(zip(f1,f2))
                    for line1, line2 in zip(f1, f2):
                        if (line1==line2):
                            tst_count+=1
                            count=count+1
                            flash(f'Testcases {tst_count} : {test_lst[int((tst_count-1)/2)]}')                          
                            flash(f'Actual output :( {line1} ) ----- Expected output : ( {line2} ) ---------- passed', "green")
                            print('count', count)
                        else:
                            print('not equal')
                            tst_count+=1
                            flash(f'Testcases {tst_count} : {test_lst[int((tst_count-1)/2)]}')
                            flash(f'Actual output : ( {line1} ) ----- Expected output : ( {line2} ) ---------- failed', "red")
                    print('score:', count*10)
                    print(test_lst)
                    grade = count*10                    
                    flash(f' Grade: {grade:.2f}',"grade")
                    
            return redirect(url_for('student_view'))
        
        else:
            flash('Invalid file. Please upload a .py file.')
    return render_template('student.html')



@app.route('/instructor', methods=['GET', 'POST'])
def instructor_view():
    if request.method == 'POST':
        code_file = request.files['code-file']
        test_file = request.files['test-file']
        print(f"DEBUG: {code_file.filename} and {test_file.filename}")
        if code_file and allowed_file(code_file.filename) and test_file and allowed_file(test_file.filename):
            code_filename = secure_filename(code_file.filename)
            test_filename = secure_filename(test_file.filename)
            code_path = os.path.join(app.config['INSTRUCTOR_UPLOAD_FOLDER'], code_filename)
            test_path = os.path.join(app.config['INSTRUCTOR_UPLOAD_FOLDER'], test_filename)
            code_file.save(code_path)
            flash(f'Code File *{code_file.filename}* uploaded successfully.', "first_msg")
            # flash(f'', "second_msg")
            test_file.save(test_path)
            flash(f'Test case *{test_file.filename}* file uploaded successfully.', "first_msg")
            # flash(f'{test_file.filename}', "second_msg")
            return redirect(url_for('instructor_view'))
        else:
            flash('Code and Test files are expected. '
                  'Looks like you uploaded only one file or trying to upload invalid files',"second_msg"
            )
    return render_template('instructor.html')


if __name__ == '__main__':
    app.run(debug=True)
