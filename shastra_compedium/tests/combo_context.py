from shastra_compedium.tests.factories import (
    CombinationDetailFactory,
    ExampleImageFactory,
    PositionDetailFactory,
    PositionFactory,
    SourceFactory,
    SubjectFactory,
)
from shastra_compedium.tests.functions import set_image


class CombinationContext:
    def __init__(self, contents=None, subject=None):
        self.subject = subject or SubjectFactory()
        self.source = SourceFactory()
        self.first_position = PositionFactory()
        if contents is not None:
            self.combo = CombinationDetailFactory(
                contents=contents,
                subject=self.subject,
                positions=[self.first_position])
        else:
            self.combo = CombinationDetailFactory(
                subject=self.subject,
                positions=[self.first_position])
        self.combo.sources.add(self.source)

    def set_images(self):
        # this one links the combo
        self.img1 = set_image(folder_name="PositionImageUploads")
        self.example_image = ExampleImageFactory(
            image=self.img1,
            subject=self.combo.subject,
            general=False)
        self.example_image.combinations.add(self.combo)

        # this one is a main image
        self.img2 = set_image(folder_name="PositionImageUploads")
        self.example_image2 = ExampleImageFactory(
            image=self.img2,
            subject=self.combo.subject,
            general=True)

    def set_dependancies(self, setup_image=True):
        # this one links the combo
        self.pos_detail = PositionDetailFactory(position=self.first_position)
        self.pos_detail.sources.add(self.source)

        if setup_image:
            self.pos_img = set_image(folder_name="PositionImageUploads")
            self.example_pos_image = ExampleImageFactory(
                image=self.pos_img,
                position=self.first_position,
                general=False)
            self.example_pos_image.details.add(self.pos_detail)
        return self.pos_detail
