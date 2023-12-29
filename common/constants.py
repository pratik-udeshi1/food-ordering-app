class Constants:
    """
    Constants are written here and used in whole application
    """

    RESET_PASSWORD_TOKEN = "PASSWORD_RESET"
    VERIFICATION_TOKEN = "VERIFICATION"
    INVITATION_TOKEN = "INVITATION"

    ADMIN = "ADMIN"
    STAFF = "STAFF"

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
    NOT_FOUND = "Record Not Found"
    NOT_AUTHORIZE = "{} is not authorized to perform this action"
    EMAIL_PASSWORD_INCORRECT = "Email or password is incorrect"
    CURRENT_NEW_PASSWORD_NOT_SAME = "New password should not be same as Current password"
    NEW_PASSWORD_RETYPE_PASSWORD_NOT_SAME = "Confirm password should be same as New password"
    INVALID_PASSWORD = "Invalid Password"
    INVALID_EMAIL = "You are not logged in with the same email id"
    PASSWORD_CHANGE = "Password changed"
    PASSWORD_SET = "Password has been set"
    LOGOUT_SUCCESSFULLY = "Logout is successful"
    LOGOUT_FAILED = "Logout Failed. Contact admin."
    DOES_NOT_EXISTS = "{} not found"
    EMAIL_SENT = "Email has been sent"
    INVITE_NOT_SENT = "Invite could not be sent. Check details again"
    ALREADY_EXISTS = "Already exists"
    BAD_REQUEST = "Bad request"
    USER_DELETED = "User details removed"
    RECORD_DELETED = "Record removed successfully"
    RECORD_NOT_DELETED = "Error occurred while removing the Record"

    USER_NOT_ACTIVE = "User is not active"
    SOMETHING_WENT_WRONG = "Something went wrong"
    USER_NOT_EXISTS = "User Does Not Exist"

    CURRENT_PASSWORD_INCORRECT = "Current password is incorrect"
    RESET_EMAIL_SUBJECT = "Reset Password"

    NOT_ALLOWED = "This action is not allowed"

    PHONE_NO_LENGTH = "Phone number must be 10 digits long"
    STRIPE_CUST_EXIST = "Customer already has a payment method"
    STRIPE_CUST_PM_SUCCESS = "Customer and payment method created successfully"
    STRIPE_PAYMENT_SUCCESS = "Payment processed successfully on Stripe"
    STRIPE_PAYMENT_FAIL = "Payment Failed on Stripe"
    STRIPE_PROFILE_NOT_EXIST = "Stripe profile doesn't exist. " \
                               "Please create signup for stripe profile, to access further"
