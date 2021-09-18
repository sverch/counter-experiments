import os
from collections import Counter
from slack_sdk.webhook import WebhookClient


class SummaryCounter(Counter):
    """Counter with a name that can print a nice summary"""
    def __init__(self, name, *args, **kwargs):
        self.name = name
        url = os.getenv("DATA_EVENTS_WEBHOOK")
        self.webhook = WebhookClient(url)
        super().__init__(*args, **kwargs)

    def markdown(self):
        msg = ("\n")
        msg += ("# %s\n" % self.name)
        msg += ("\n")
        for key, value in self.items():
            msg += ("- %s: %s\n" % (key, value))
        return msg

    def slack_markdown(self):
        """https://api.slack.com/reference/surfaces/formatting#basics"""
        msg = ("\n")
        msg += ("*%s*\n" % self.name)
        msg += ("\n")
        for key, value in self.items():
            msg += ("- %s: %s\n" % (key, value))
        return msg

    def pretty_print(self):
        print(self.markdown())

    def post_to_slack(self):
        self.webhook.send(
            text="fallback",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": self.slack_markdown(),
                    }
                }
            ]
        )


c = SummaryCounter("New Cases")


def count_events():
    c["bar"] += 1
    c["bar"] += 1
    c["bar"] += 1
    c["baz"] += 1
    c["baz"] += 1
    c.pretty_print()
    c.post_to_slack()


count_events()
