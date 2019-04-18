from django.core.management.base import BaseCommand
from argparse                    import FileType
from datetime                    import datetime

from webapp.models               import FoodReviews

def _to_date(d):
    return datetime.fromtimestamp(d) if d else None

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='path to txt file')
        parser.add_argument('--limit', type=int, help='to limit no of data upload')

    def handle(self, *args, **kwargs):
        rawfile = kwargs['file_path']
        limit   = kwargs['limit']
        with open(rawfile, encoding='latin-1') as f:
            _data  = {}
            total = 0
            for line in f.readlines():
                if not line.strip() == '':
                    try:
                        key, value = line.strip().split(':', 1)
                        _data[key] = value
                    except: pass
                else:
                    # trimming and striping values.
                    _data = dict([(k, v.strip()) for k, v in _data.items()])

                    # Inserting data to db from txt file.
                    FoodReviews.objects.create(
                        product_id  = _data.get('product/productId'),
                        user_id     = _data.get('review/userId'),
                        name        = _data.get('review/profileName'),
                        helpfulness = _data.get('review/helpfulness'),
                        score       = _data.get('review/score'),
                        timestamp   = _to_date(int(_data.get('review/time'))),
                        summary     = _data.get('review/summary'),
                        text        = _data.get('review/text'))

                    total += 1
                    print('\r{} recods inserted..'.format(total), end='')
                    _data = {}

                    if limit and total >= limit:
                        break