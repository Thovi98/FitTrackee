import pytest
from flask import Flask

from fittrackee.emails.email import EmailTemplate

from .template_results.email_update_to_current_email import (
    expected_en_html_body as expected_en_current_email_html_body,
    expected_en_text_body as expected_en_current_email_text_body,
    expected_fr_html_body as expected_fr_current_email_html_body,
    expected_fr_text_body as expected_fr_current_email_text_body,
)
from .template_results.email_update_to_new_email import (
    expected_en_html_body as expected_en_new_email_html_body,
    expected_en_text_body as expected_en_new_email_text_body,
    expected_fr_html_body as expected_fr_new_email_html_body,
    expected_fr_text_body as expected_fr_new_email_text_body,
)


class TestEmailTemplateForEmailUpdateToCurrentEmail:
    EMAIL_DATA = {
        'username': 'test',
        'new_email_address': 'new.email@example.com',
        'operating_system': 'Linux',
        'browser_name': 'Firefox',
        'fittrackee_url': 'http://localhost',
    }

    @pytest.mark.parametrize(
        'lang, expected_subject',
        [
            ('en', 'FitTrackee - Email changed'),
            ('fr', 'FitTrackee - Adresse email modifiée'),
        ],
    )
    def test_it_gets_subject(
        self, app: Flask, lang: str, expected_subject: str
    ) -> None:
        email_template = EmailTemplate(app.config['TEMPLATES_FOLDER'])

        subject = email_template.get_content(
            'email_update_to_current_email', lang, 'subject.txt', {}
        )

        assert subject == expected_subject

    @pytest.mark.parametrize(
        'lang, expected_text_body',
        [
            ('en', expected_en_current_email_text_body),
            ('fr', expected_fr_current_email_text_body),
        ],
    )
    def test_it_gets_text_body(
        self, app: Flask, lang: str, expected_text_body: str
    ) -> None:
        email_template = EmailTemplate(app.config['TEMPLATES_FOLDER'])

        text_body = email_template.get_content(
            'email_update_to_current_email', lang, 'body.txt', self.EMAIL_DATA
        )

        assert text_body == expected_text_body

    def test_it_gets_en_html_body(self, app: Flask) -> None:
        email_template = EmailTemplate(app.config['TEMPLATES_FOLDER'])

        text_body = email_template.get_content(
            'email_update_to_current_email', 'en', 'body.html', self.EMAIL_DATA
        )

        assert expected_en_current_email_html_body in text_body

    def test_it_gets_fr_html_body(self, app: Flask) -> None:
        email_template = EmailTemplate(app.config['TEMPLATES_FOLDER'])

        text_body = email_template.get_content(
            'email_update_to_current_email', 'fr', 'body.html', self.EMAIL_DATA
        )

        assert expected_fr_current_email_html_body in text_body


class TestEmailTemplateForEmailUpdateToNewEmail:
    EMAIL_DATA = {
        'username': 'test',
        'email_confirmation_url': 'http://localhost/email-update?token=xxx',
        'operating_system': 'Linux',
        'browser_name': 'Firefox',
        'fittrackee_url': 'http://localhost',
    }

    @pytest.mark.parametrize(
        'lang, expected_subject',
        [
            ('en', 'FitTrackee - Confirm email change'),
            ('fr', "FitTrackee - Confirmer le changement d'adresse email"),
        ],
    )
    def test_it_gets_subject(
        self, app: Flask, lang: str, expected_subject: str
    ) -> None:
        email_template = EmailTemplate(app.config['TEMPLATES_FOLDER'])

        subject = email_template.get_content(
            'email_update_to_new_email', lang, 'subject.txt', {}
        )

        assert subject == expected_subject

    @pytest.mark.parametrize(
        'lang, expected_text_body',
        [
            ('en', expected_en_new_email_text_body),
            ('fr', expected_fr_new_email_text_body),
        ],
    )
    def test_it_gets_text_body(
        self, app: Flask, lang: str, expected_text_body: str
    ) -> None:
        email_template = EmailTemplate(app.config['TEMPLATES_FOLDER'])

        text_body = email_template.get_content(
            'email_update_to_new_email', lang, 'body.txt', self.EMAIL_DATA
        )

        assert text_body == expected_text_body

    def test_it_gets_en_html_body(self, app: Flask) -> None:
        email_template = EmailTemplate(app.config['TEMPLATES_FOLDER'])

        text_body = email_template.get_content(
            'email_update_to_new_email', 'en', 'body.html', self.EMAIL_DATA
        )

        assert expected_en_new_email_html_body in text_body

    def test_it_gets_fr_html_body(self, app: Flask) -> None:
        email_template = EmailTemplate(app.config['TEMPLATES_FOLDER'])

        text_body = email_template.get_content(
            'email_update_to_new_email', 'fr', 'body.html', self.EMAIL_DATA
        )

        assert expected_fr_new_email_html_body in text_body
