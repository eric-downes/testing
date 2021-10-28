import os
import time
import random
from typing import *

import arrow
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists, NotFound

PROJECT_ID = 'mpc-testing'
SUBR = (Subr := pubsub_v1.SubscriberClient)()
PUBR = (Pubr := pubsub_v1.PublisherClient)()

def create_topic_if_dne(topic:str,
                        project:str = PROJECT_ID,
                        pubr:Pubr = PUBR,
                        timeout:int = 10, # 3 seems too short a time...
                        ) -> str:
    topic_path = pubr.topic_path(project, topic)
    try: pubr.create_topic(name = topic_path)
    except AlreadyExists: pass
    return topic_path

def create_sub_if_dne(sub:str,
                      topic:str,
                      project:str = PROJECT_ID,
                      subr:Subr = SUBR,
                      pubr:Pubr = PUBR,
                      timeout:int = 10) -> None:
    sub_path = pubr.subscription_path(project, sub)
    topic_path = pubr.topic_path(project, topic)
    t0 = arrow.now()
    while (arrow.now() - t0).total_seconds() <= timeout:
        try: subr.create_subscription(name = sub_path, topic = topic_path)
        except AlreadyExists: return sub_path
    raise TimeoutError(f'could not create subscription {sub} :(')

def randhex(n:int = 8) -> str:
    return f'%0{n}x' % random.randrange(16 ** n)

def test_env():
        create_topic_if_dne(topic := 'topic_' + randhex())
        create_sub_if_dne(sub := 'sub_' + randhex(), topic)
        time.sleep(2)
        subs = SUBR.list_subscriptions(request = {"project": f'projects/{PROJECT_ID}'})
        assert sub in {s.name.split('/')[-1] for s in subs}

if __name__ == '__main__':
        test_env()
