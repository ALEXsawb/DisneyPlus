def logging_in(response, expire_time_in_min, user_id):
    response.set_cookie('logged_in', 'True', expire_time_in_min * 60, expire_time_in_min * 60,
                        '/', None, False, False, 'lax')
    response.set_cookie('end_user_id', user_id, expire_time_in_min * 60, expire_time_in_min * 60,
                        '/', None, False, False, 'lax')