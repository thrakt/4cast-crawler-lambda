import json
import logging
import os
import requests
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event, context):
    """
    Lambda handler
    """

    session_id = os.environ["SESSIONID"]

    # get final predicts
    questions = requests.get(
        'https://www.4cast.to/api/questions/final?size=30',
        cookies={'SESSION':session_id}
        ).json()['content']
    
    logger.info('success getting questions.')

    # filter yet vote
    questions_f = [p for p in questions if p['participated'] == False and p['endAt'] - time.time() * 1000 < 1000 * 60 * 60 * 2]

    for q in questions_f:
        logger.info('vote a question.')
        logger.info(q)
        id = str(q['id'])

        # get to vote
        to_vote = requests.get(
            'https://www.4cast.to/api/predictions/'+id+'?page=1&size=10&questionId='+id,
            cookies={'SESSION':session_id}
            ).json()['content'][0]
        
        # vote most voted
        requests.post(
            'https://www.4cast.to/api/votes',
            data=json.dumps({'questionId':int(id),'predictionId':to_vote['id'],'predict':to_vote['prediction']}),
            cookies={'SESSION':session_id},
            headers={'Content-Type': 'application/json'}
            )

    return questions_f
