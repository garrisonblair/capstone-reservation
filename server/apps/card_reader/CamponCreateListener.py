from apps.util.ModelObserver import ModelObserver
from apps.util import utils
from datetime import datetime, time


from apps.system_administration.models.system_settings import SystemSettings


class CamponCreateListener(ModelObserver):

    def subject_created(self, campon):

        settings = SystemSettings.get_settings()

        if settings.campons_refutable:
            # Set booking expiration and notify booker
            booker = campon.camped_on_booking.booker

            campon.camped_on_booking.expiration_base = datetime.now().time()
            campon.camped_on_booking.save()
            utils.log_model_change(campon, utils.CHANGE)

            expiration_time = campon.camped_on_booking.get_expiration()  # type: time

            email_subject = "Your booking has been camped on"
            email_message = "Someone is camping on to your booking.\n"\
                            "If you do not reconfirm your booking before " + str(expiration_time.strftime("%H:%M:%S"))\
                            + ",\n"\
                            "it will be cancelled."

            booker.send_email(email_subject, email_message)

    def subject_deleted(self, subject):
        pass

    def subject_updated(self, subject):
        pass
