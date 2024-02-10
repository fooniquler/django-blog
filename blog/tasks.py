import json
import time
import random as rnd

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from .models import Post


@shared_task
def moderate_post(post_id):
    processing_time = rnd.randint(3, 5)
    time.sleep(processing_time)

    post = Post.objects.get(id=post_id)
    post.status = 'published'
    post.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'user_{post.author.id}',
        {
            'type': 'post_published',
            'message': 'Your post has been published!!!'
        }
    )
