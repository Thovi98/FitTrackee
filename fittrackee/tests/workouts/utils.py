import json
from datetime import datetime
from io import BytesIO
from typing import Optional, Tuple

from flask import Flask

from fittrackee import db
from fittrackee.privacy_levels import PrivacyLevel
from fittrackee.users.models import User
from fittrackee.workouts.models import Workout, WorkoutComment

from ..mixins import RandomMixin


def post_a_workout(
    app: Flask,
    gpx_file: str,
    notes: Optional[str] = None,
    workout_visibility: Optional[PrivacyLevel] = None,
) -> Tuple[str, str]:
    client = app.test_client()
    resp_login = client.post(
        '/api/auth/login',
        data=json.dumps(dict(email='test@test.com', password='12345678')),
        content_type='application/json',
    )
    token = json.loads(resp_login.data.decode())['auth_token']
    workout_data = '{"sport_id": 1'
    if notes is not None:
        workout_data += f', "notes": "{notes}"'
    if workout_visibility is not None:
        workout_data += f', "workout_visibility": "{workout_visibility.value}"'
    workout_data += '}'
    response = client.post(
        '/api/workouts',
        data=dict(
            file=(BytesIO(str.encode(gpx_file)), 'example.gpx'),
            data=workout_data,
        ),
        headers=dict(
            content_type='multipart/form-data', Authorization=f'Bearer {token}'
        ),
    )
    data = json.loads(response.data.decode())
    return token, data['data']['workouts'][0]['id']


class WorkoutCommentMixin(RandomMixin):
    def create_comment(
        self,
        user: User,
        workout: Workout,
        text: Optional[str] = None,
        text_visibility: PrivacyLevel = PrivacyLevel.PRIVATE,
        created_at: Optional[datetime] = None,
    ) -> WorkoutComment:
        text = self.random_string() if text is None else text
        comment = WorkoutComment(
            user_id=user.id,
            workout_id=workout.id,
            workout_visibility=workout.workout_visibility,
            text=text,
            text_visibility=text_visibility,
            created_at=created_at,
        )
        db.session.add(comment)
        db.session.commit()
        return comment
