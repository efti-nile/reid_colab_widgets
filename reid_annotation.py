from google.colab.patches import cv2_imshow
import ipywidgets as widgets
import random
import cv2


class ReidAnnotation(widgets.VBox):
    """Widget for manual annotation of a little amount of data"""

    class RandomImageBox(widgets.VBox):
        """Displays a track as a randomly chosen image with a selection button.
        Text on button is a length of track
        """
        def __init__(self, imgs, resize_to=(50, 100)):
            """
            Args:
                imgs: a list of images in a track
                resize_to: a tuple (WIDTH, HEIGHT)
            """
            self.imgs = imgs
            self.thumb = cv2.resize(random.choice(self.imgs), resize_to)
            self.btn = widgets.Button(description=str(len(self.imgs)),
                                      button_style='success',
                                      layout=widgets.Layout(width=f'{resize_to[0]}px'))
            self.btn.on_click(self.button_callback)
            self.is_chosen = False  # if this image box selected by user
            self.image_out = widgets.Output()
            with self.image_out:
                cv2_imshow(self.thumb)
            super().__init__([self.image_out, self.btn])

        def button_callback(self, b):
            self.is_chosen ^= True
            b.button_style = 'danger' if self.is_chosen else 'success'

    def __init__(self, imgs_by_cam):
        """
        Args:
            imgs_by_cam: list[list[list[images]]] (imgs_by_cam[cam_idx][track_idx][img_idx])
        """
        self.imgs_by_cam = imgs_by_cam
        self.btn = widgets.Button(description='NEXT', layout=widgets.Layout(width='100%', height='50px'))
        cam_box_layout = widgets.Layout(overflow='scroll hidden',
                                        border='3px solid black',
                                        width='500px',
                                        height='',
                                        flex_flow='row',
                                        display='flex')
        self.cam_boxes = [
            widgets.Box(children=image_boxes, layout=cam_box_layout) for image_boxes in
            [[ReidAnnotation.RandomImageBox(imgs) for imgs in cam_imgs] for cam_imgs in imgs_by_cam]
            ]
        super().__init__([self.btn] + self.cam_boxes)
