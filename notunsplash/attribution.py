"""Attribution module for Unsplash photos"""

class Attribution:
    """Class to handle photo attribution in various formats"""
    def __init__(self, photo):
        self.photo = photo

    @property
    def html(self):
        """Return HTML format attribution"""
        return (
            f'Photo by <a href="{self.photo.user.html_link}">{self.photo.user.name}</a> '
            f'on <a href="https://unsplash.com">Unsplash</a>'
        )

    @property
    def markdown(self):
        """Return Markdown format attribution"""
        return (
            f'Photo by [{self.photo.user.name}]({self.photo.user.html_link}) '
            f'on [Unsplash](https://unsplash.com)'
        )

    @property
    def rst(self):
        """Return reStructuredText format attribution"""
        return (
            f'Photo by `{self.photo.user.name} <{self.photo.user.html_link}>`_ '
            f'on `Unsplash <https://unsplash.com>`_'
        )

    @property
    def text(self):
        """Return plain text format attribution"""
        return (
            f'Photo by {self.photo.user.name} ({self.photo.user.html_link}) '
            f'on Unsplash (https://unsplash.com)'
        )

    @property
    def dict(self):
        """Return dictionary format attribution"""
        return {
            "name": self.photo.user.name,
            "url": self.photo.user.html_link
        }
