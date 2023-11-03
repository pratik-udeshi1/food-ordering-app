class Constants:
    """
    Constants are written here and used in whole application
    """

    RESET_PASSWORD_TOKEN = "PASSWORD_RESET"
    VERIFICATION_TOKEN = "VERIFICATION"
    INVITATION_TOKEN = "INVITATION"

    ADMIN = "ADMIN"

    WEB = "WEB"
    ANDROID = "MOBILE"
    IOS = "IOS"

    ACTIVE = "Active"
    INACTIVE = "Inactive"


class ApplicationMessages:
    """
    Response, error etc application messages
    """

    SUCCESS = "Success"
    NOT_AUTHORIZE = "{} is not authorized to perform this action"
    EMAIL_PASSWORD_INCORRECT = "Email or password is incorrect or both"
    CURRENT_NEW_PASSWORD_NOT_SAME = "New password should not be same as Current password"
    NEW_PASSWORD_RETYPE_PASSWORD_NOT_SAME = "Confirm password should be same as New password"
    INVALID_PASSWORD = "Invalid Password"
    INVALID_EMAIL = "You are not logged in with the same email id"
    PASSWORD_CHANGE = "Password changed"
    PASSWORD_SET = "Password has been set"
    LOGOUT_SUCCESSFULLY = "Logout is successful"
    LOGOUT_FAILED = "Logout Failed. Contact admin."
    DOES_NOT_EXISTS = "{} not exists"
    EMAIL_SENT = "Email has been sent"
    INVITE_NOT_SENT = "Invite could not be sent. Check details again"
    ALREADY_EXISTS = "Already exists"
    BAD_REQUEST = "Bad request"
    USER_DELETED = "User details removed"

    USER_NOT_ACTIVE = "User is not active"
    SOMETHING_WENT_WRONG = "Something went wrong"
    USER_NOT_EXISTS = "User Does Not Exist"

    CURRENT_PASSWORD_INCORRECT = "Current password is incorrect"
    RESET_EMAIL_SUBJECT = "Reset Password"

    NOT_ALLOWED = "This action is not allowed"

    PHONE_NO_LENGTH = "Phone number must be 10 digits long"
