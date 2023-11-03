class Constants:
    """
    Constants are written here and used in whole application
    """

    RESET_PASSWORD_TOKEN = "PASSWORD_RESET"
    VERIFICATION_TOKEN = "VERIFICATION"
    INVITATION_TOKEN = "INVITATION"

    ADMIN = "ADMIN"
    EXAMINER = "EXAMINER"
    CANDIDATE = "CANDIDATE"
    SUBADMIN = "SUB-ADMIN"

    WEB = "WEB"
    ANDROID = "MOBILE"
    IOS = "IOS"

    EMAIL_LINK_EXPIRY = 48  # Hours

    EXAM_DURATION = 3600  # Seconds

    ACTIVE = "Active"
    INACTIVE = "Inactive"

    # JOB
    JOB_ADD = "ADDED"
    JOB_REMOVE = "REMOVED"
    JOB_UPDATE = "UPDATED"
    ALL = "ALL"

    # EXAM
    EXAM_CREATED = "CREATED"
    EXAM_DELETED = "DELETED"
    EXAM_EDITED = "EDITED"

    UNATTEMPTED = "UNATTEMPTED"

    # QUESTION_TYPE
    QUESTION_SUB = "subjective"
    QUESTION_OBJ = "objective"

    # CANDIDATE
    CANDIDATE_PASSED = "PASSED"
    CANDIDATE_FAILED = "FAILED"
    CANDIDATE_EXAM_SUBMIT = "EXAM_SUBMITTED"
    CANDIDATE_EXAM_ATTEMPTED = "EXAM_ATTEMPTED"
    CANDIDATE_EXAM_DISQUALIFIED = "DISQUALIFY"
    CANDIDATE_EXAM_LINK_EXPIRE = "LINK_EXPIRED"
    EXAM_LINK_SENT = "LINK_SENT"
    EXAM_LINK_NOT_SENT = "LINK_NOT_SENT"

    CUSTOM_NOTIFICATION = "CUSTOM_NOTIFICATION"

    # Notification constants
    JOB = "JOB"
    EXAM = "EXAM"
    NOTIFY = "NOTIFICATION"


class ApplicationMessages:
    """
    Response, error etc application messages
    """

    SUCCESS = "Success"
    NOT_AUTHORIZE = "{} is not authorized to perform this action"
    EMAIL_PASSWORD_INCORRECT = "Email or password is incorrect or both"
    CANDIDATE_ID_INCORRECT = "Candidate Id incorrect"
    CURRENT_NEW_PASSWORD_NOT_SAME = "New password should not be same as Current password"
    NEW_PASSWORD_RETYPE_PASSWORD_NOT_SAME = "Confirm password should be same as New password"
    INVALID_PASSWORD = "Invalid Password"
    INVALID_EMAIL = "You are not logged in with the same email id"
    CANDIDATE_INVALID_LOGIN = "Access Denied, Invalid Login"
    PASSWORD_CHANGE = "Password changed"
    PASSWORD_SET = "Password has been set"
    LOGOUT_SUCCESSFULLY = "Logout is successful"
    LOGOUT_FAILED = "Logout Failed. Contact admin."
    DOES_NOT_EXISTS = "{} not exists"
    EMAIL_SENT = "Email has been sent"
    INVITE_NOT_SENT = "Invite could not be sent. Check details again"
    ALREADY_EXISTS = "Already exists"
    DEPARTMENT_NOT_EXIST = "No such department exists"
    JOB_CREATED = "A new Job is created"
    JOB_UPDATED = "Job is updated successfully"
    JOB_NOT_EXISTS = "This Job does not exist"
    JOB_DELETED = "Job is deleted"
    JOB_ALREADY_DELETED = "The Job you are looking for has been deleted."
    JOB_UNPUBLISHED = "Job's status changed to UNPUBLISH"
    BAD_REQUEST = "Bad request"
    USER_DELETED = "User details removed"
    SUBADMIN_NOT_ADDED = "Subadmin details cannot be added. Check validity of details again"

    QUESTION_NOT_EXIST = 'Question not exists'
    QUESTION_CATEGORY_NOT_EXIST = "The Question Category you are looking for does not exists."
    QUESTION_UNPUBLISHED = 'Question un_published successfully '
    QUESTION_STATUS = 'status '
    QUESTION_STATUS_NOT_EXIST = ' Sorry! you can not do that,You can update question_status only please Try again'
    QUESTION_DURATION = "Time Duration for the Question should not be blank"
    QUESTION_TOTAL_MARKS = "Total Marks for the Question should not be 0 or negative"
    QUESTION_OBTAINED_MARKS = "Obtained Marks for the Question should not be more than Total marks or negative"

    QUESTION_CREATED = 'question created successfully '
    QUESTION_UPDATED = 'Question has updated successfully '
    QUESTION_STATUS_UPDATED = 'Question status updated successfully'
    QUESTION_DELETED = 'Question deleted successfully'
    QUESTION_CATEGORY_DELETED = 'Question Category deleted successfully'
    QUESTION_N_ADDED = 'Question cannot be added to te exam now. Try again Later '

    ANSWER_NOT_EXIST = 'ANSWER not exists'
    ANSWER_CREATED = 'ANSWER created successfully'
    ANSWER_DELETED = 'ANSWER deleted successfully'

    EXAM_CREATED = 'Exam created successfully '
    EXAM_UPDATED = 'Exam has updated successfully '
    EXAM_N_UPDATED = 'Exam cannot be updated. Try again Later '
    EXAM_STATUS_UPDATED = 'Exam status updated successfully'
    EXAM_DELETED = 'Exam deleted successfully'
    EXAM_QUESTIONS_NOT_EXIST = 'Exam Questions deleted successfully'
    EXAM_NOT_EXIST = "Exam does not exist"
    EXAM_ALREADY_EXIST = 'This Exam is already Exist '
    EXAM_STATUS_NOT_EXIST = ' Sorry! you can not do that,You can update exam status only please Try again'

    CANDIDATE_CREATED = 'Candidate created successfully '
    CANDIDATE_UPDATED = 'Candidate has updated successfully '
    CANDIDATE_DELETED = 'Candidate deleted successfully'
    CANDIDATE_NOT_EXIST = "Candidate does not exist"
    CANDIDATE_EXAM_ID_INCORRECT = 'Candidate exam id in correct'

    CANDIDATE_EXAM_SUBMIT = "Candidate has submitted the exam"
    CANDIDATE_EXAM_ATTEMPTED = "Candidate has attempted the exam"
    CANDIDATE_EXAM_DISQUALIFIED = "Candidate is disqualified"
    CANDIDATE_EXAM_LINK_EXPIRE = "Candidate has not attempted the exam and the link has expired"
    CANDIDATE_EXAM_LINK = "Candidate with this exam link already exists. Generate new link"

    USER_NOT_ACTIVE = "User is not active"
    SOMETHING_WENT_WRONG = "Something went wrong"
    USER_NOT_EXISTS = "User Does Not Exist"

    CURRENT_PASSWORD_INCORRECT = "Current password is incorrect"
    RESET_EMAIL_SUBJECT = "Reset Password"
    INVITE_EMAIL_SUBJECT = "Invitation for joining Hiring Portal"
    INVITE_CANDIDATE_SUBJECT = "NICKELFOX HIRING - EXAM LOGIN LINK"

    DELETE_NOT_DONE = "This record is already deleted. You cannot delete it again"
    NOT_ALLOWED = "This action is not allowed"

    QTAG_DELETED = "This Tag is deleted from the question"
    EXAMINER_NOT_YET_DELETED = "This examiner is not deleted yet"

    EXAM_QUESTION_DEPEND = "This exam cannot be deleted because it has {} questions associated." \
                           "Remove the dependency first"
    JOB_EXAM_DEPEND = "This Job cannot be deleted because it has exams associated. Remove the dependency first"
    EXAMINER_CANDIDATE_DEPEND = "This examiner cannot be deleted because it has {} candidates associated." \
                                "Remove the dependency first"
    EMAIL_ALREADY_EXIST = 'This email already exist'

    DEPARTMENT_DEPEND = "This department cannot be deleted because it has {} users, {} jobs, {} exams and {} " \
                        "question associated. Remove the dependency first"
    DEPARTMENT_DELETED = "This department is deleted"

    DEPARTMENT_NOT_YET_DELETED = "This department is not deleted yet"

    SUBADMIN_NOT_YET_DELETED = "This SUBADMIN is not deleted yet"

    EXAM_QUESTION_REMOVE = "{} questions removed from the Exam"
    PHONE_NO_LENGTH = "Phone number must be 10 digits long"
