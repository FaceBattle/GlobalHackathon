import urllib

class FBPost(object):
    """docstring for FBPost"""
    def __init__(self, json):
        super(FBPost, self).__init__()
        self.message = json.get('message', '')

        self.url = ''
        self.description = ''
        self.title = ''

        if 'attachments' in json:
            attachment_list = json['attachments']['data']
            attachment = attachment_list[0]

            if attachment['type'] == 'link' or attachment['type'] == 'share' :
                self.description = attachment.get('description', '')
                self.title = attachment.get('title', '')
                url = attachment.get('url', '')
                if len (url) > 0 :
                    if url.startswith('https://www.facebook.com/l.php?u='):
                        url = url[len('https://www.facebook.com/l.php?u='):]
                    elif url.startswith('http://www.facebook.com/l.php?u='):
                        url = url[len('http://www.facebook.com/l.php?u='):]
                    url = urllib.unquote(url)
                self.url = url

        self.like_count = json['likes']['summary']['total_count']
        self.comment_count = json['comments']['summary']['total_count']
        self.created_time = json['created_time']
        self.id = json['id']


class FBPostV2(object):
    """docstring for FBPost"""
    def __init__(self, json):
        super(FBPostV2, self).__init__()
        self.message = json.get('message', '')

        self.url = ''
        self.description = ''
        self.title = ''
        self.image_url = ''

        if 'attachments' in json:
            attachment_list = json['attachments']['data']
            attachment = attachment_list[0]

            self.description = attachment.get('description', '')
            self.title = attachment.get('title', '')
            url = attachment.get('url', '')
            if len (url) > 0 :
                if url.startswith('https://www.facebook.com/l.php?u='):
                    url = url[len('https://www.facebook.com/l.php?u='):]
                elif url.startswith('http://www.facebook.com/l.php?u='):
                    url = url[len('http://www.facebook.com/l.php?u='):]
                url = urllib.unquote(url)
            self.url = url

            if 'media' in attachment:
                media = attachment['media']
                if 'image' in media:
                    image = media['image']
                    self.image_url = image['src']
                    self.image_height = image['height']
                    self.image_width = image['width']

        self.like_count = json['likes']['summary']['total_count']
        self.comment_count = json['comments']['summary']['total_count']
        self.created_time = json['created_time']
        self.id = json['id']
