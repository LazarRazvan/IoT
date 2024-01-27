from flask_mail import Mail, Message

class Notification(object):
    def __init__(self, flask_app, sender, recipients):
        """
        Create notifications object for current scenario.

        Parameters:
            flask_app   : Flask application object
            sender      : Sender email address
            recipients  : Recipients email address list
        """
        self.sender = sender
        self.flask_app = flask_app
        self.recipients = recipients
        self.mail = Mail(self.flask_app)


    def application_start(self, trigger_value):
        subject = "Application Start"
        text = f"Application started with trigger value of {trigger_value} kW!"

        with self.flask_app.app_context():
            try:
            # create
                msg = Message(subject=subject, body=text, sender=self.sender,
                                recipients=self.recipients)
                # send
                self.mail.send(msg)
            except Exception as e:
                print(f"Failed to send application start notification: {e}!")


    def application_stop(self):
        subject = "Application Stop"
        text = f"Application stopped by user!"

        with self.flask_app.app_context():
            try:
            # create
                msg = Message(subject=subject, body=text, sender=self.sender,
                                recipients=self.recipients)
                # send
                self.mail.send(msg)
            except Exception as e:
                print(f"Failed to send application stop notification: {e}!")


    def switch_on(self, trigger_power, active_power):
        subject = "Switch turned on"
        text = f"Switched turned on! Trigger power: {trigger_power} kW; Active power: {active_power} kW!"

        with self.flask_app.app_context():
            try:
            # create
                msg = Message(subject=subject, body=text, sender=self.sender,
                                recipients=self.recipients)
                # send
                self.mail.send(msg)
            except Exception as e:
                print(f"Failed to send switch on notification: {e}!")


    def switch_off(self, trigger_power, active_power):
        subject = "Switch turned off"
        text = f"Switched turned off! Trigger power: {trigger_power} kW; Active power: {active_power} kW!"

        with self.flask_app.app_context():
            try:
            # create
                msg = Message(subject=subject, body=text, sender=self.sender,
                                recipients=self.recipients)
                # send
                self.mail.send(msg)
            except Exception as e:
                print(f"Failed to send switch on notification: {e}!")


    def switch(self, err_msg):
        subject = "Switch Error"
        text = f"Error \"{err_msg}\" encountered trying to send switch command!"

        with self.flask_app.app_context():
            try:
            # create
                msg = Message(subject=subject, body=text, sender=self.sender,
                                recipients=self.recipients)
                # send
                self.mail.send(msg)
            except Exception as e:
                print(f"Failed to send switch notification: {e}!")


    def inverter(self, err_msg):
        subject = "Inverter Error"
        text = f"Error \"{err_msg}\" reported by inverter!"

        with self.flask_app.app_context():
            try:
            # create
                msg = Message(subject=subject, body=text, sender=self.sender,
                                recipients=self.recipients)
                # send
                self.mail.send(msg)
            except Exception as e:
                print(f"Failed to send inverter notification: {e}!")
