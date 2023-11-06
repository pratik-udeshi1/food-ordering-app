class ApiResponse:

    @staticmethod
    def create_api_response(serializer):
        user_data = serializer.data
        response_data = {
            'message': 'User registered successfully',
            'user_id': user_data['id'],
            'email': user_data['email'],
            'full_name': user_data['full_name'],
            'phone_number': user_data['phone_number'],
            'role': user_data['role_name'],
        }
        return response_data
