from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.core.validators import RegexValidator
from django.conf import settings
from PIL import Image, ImageDraw

# Programs
CAS = 'CAS'
CCS = 'CCS'
CEA = 'CEA'

# SCHOLARSHIP TYPES
MERIT = 'Merit'
JLSS_MERIT = 'JLSS Merit'
RA_7687 = 'RA 7687'
JLSS_RA_7687 = 'JLSS RA 7687'
RA_10612 = 'RA 10612'


class Members(models.Model):
    studentNumber = models.PositiveIntegerField()
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    program_and_year = models.CharField(max_length=20)
    college = models.CharField(max_length=3, choices=[(CAS, 'CAS'), (CCS, 'CCS'), (CEA, 'CEA')])
    scholarshipType = models.CharField(max_length=20, choices=[(MERIT, 'Merit'), (JLSS_MERIT, 'JLSS Merit'), (RA_7687, 'RA 7687'), (JLSS_RA_7687, 'JLSS RA 7687'), (RA_10612, 'RA 10612')])
    cpNum = models.CharField(max_length=12, validators=[RegexValidator(r'^\d{1,12}$')], blank=True)
    personalEmail = models.EmailField()
    cspcEmail = models.EmailField()
    address = models.CharField(max_length=100)
    position = models.CharField(max_length=50, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def __str__(self):
        return f'Member: {self.firstName} {self.middleName} {self.lastName}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Use a fixed URL path that will redirect dynamically
        qr_code_url = f"/qr-redirect/{self.studentNumber}/"
        qr_image = qrcode.make(qr_code_url)
        canvas = Image.new('RGB', (qr_image.size), 'white')
        canvas.paste(qr_image)
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(f'qr_code_{self.studentNumber}.png', File(buffer), save=False)