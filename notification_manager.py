from twilio.rest import Client


class NotificationManager:

    def __init__(self, account_sid, auth_token, send_phone, receive_phone):
        self.twilio_account_sid = account_sid
        self.twilio_auth_token = auth_token
        self.twilio_phone = send_phone
        self.my_phone = receive_phone
        self.client = Client(self.twilio_account_sid, self.twilio_auth_token)

    def send_flight_deals(self, message):
        message = self.client.messages \
            .create(
                body=message,
                from_=self.twilio_phone,
                to=self.my_phone,
                    )
