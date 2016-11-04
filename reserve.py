 '''
    conditon['student_id']=request.form.get('student_id')
    conditon['student_name']=request.form.get('student_name')
    conditon['gpa_min']=request.form.get('student_gpa_min')
    conditon['gpa_max']=request.form.get('student_gpa_max')
    conditon['up_or_down']=request.form.get('up_or_down')
    conditon['order']=request.form.get('order')
    conditon['is_dishonour']=request.form.get('is_dishonour')
    conditon['student_course']=request.form.get('student_course')
    conditon['student_grade']=request.form.get('student_grade')
    conditon['student_college']=request.form.get('student_college')
    conditon['student_reward']=request.form.get('student_course')
    conditon['student_seminar']=request.form.get('student_course')

    condition['course_id']=request.form.get('course_id')
    condition['course_name']=request.form.get('course_name')
    condition['course_time']=request.form.get('course_time')
    condition['course_location']=request.form.get('course_location')

'''



    '''

@app.route('/email',methods=['GET'])
def email_form():
    return render_template('email-form.html') 

@app.route('/find-form',methods=['GET'])
def find_form():
    return render_template('find-form.html')


@app.route('/signin',methods=['GET'])
def signin_form():
    return render_template('form.html') 
    '''