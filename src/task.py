import datetime
import time

import cronex
from task_interfaces import MetaTaskInterface


class Task(MetaTaskInterface):
    """
    Verifies the Title of a Pull Request matches a provided regex.
    """

    name = "Code Freeze"
    slug = "code-freeze"
    pass_summary = ""
    fail_summary = "Cannot deploy during Code Freeze."
    _pass_text = ""
    actions = [
        {
            "label": "Hotfix",
            "identifier": "hotfix",
            "description": "Allow deployment of hotfix during code freeze.",
        }
    ]

    # current_time is only passed in for testing purposes
    def execute(self, github_body, settings, current_time=None) -> bool:
        self.settings = settings

        # A manual override has been requested
        if (
            github_body.get("githaxs", {}).get("full_event")
            == "check_run.requested_action"
            and github_body.get("requested_action", {}).get("identifier", "")
            == "hotfix"
        ):
            self.actions = None
            self.pass_text = "%s has overridden the original result" % github_body.get(
                "sender"
            ).get("login")
            return True

        for block_time in settings.get("block_times", []):
            cron_expression = cronex.CronExpression(block_time)

            if current_time is None:
                current_time = time.gmtime(time.time())[:5]

            self.current_time = current_time
            if cron_expression.check_trigger(current_time) is True:
                return False

        return True

    @property
    def fail_text(self) -> str:
        return "The current time is: {}\n\nCode Freeze Settings are: {}".format(
            datetime.datetime(*self.current_time).strftime("%H:%M on %b %d %Y"),
            self.settings.get("block_times"),
        )

    @property
    def pass_text(self) -> str:
        return self._pass_text
