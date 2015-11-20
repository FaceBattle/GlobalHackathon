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
            self.description = attachment.get('description', '')
            self.title = attachment.get('title', '')

            if attachment['type'] == 'link' or attachment['type'] == 'share' :
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
