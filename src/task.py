import datetime
import time

import cronex
from task_interfaces import MetaTaskInterface, SubscriptionLevels


class Task(MetaTaskInterface):
    """
    Verifies the Title of a Pull Request matches a provided regex.
    """

    name = "Code Freeze"
    slug = "code-freeze"
    pass_text = ""
    fail_summary = "Cannot deploy during Code Freeze."
    _pass_summary = ""
    subscription_level = SubscriptionLevels.FREE
    _actions = [
        {
            "label": "Hotfix",
            "identifier": "hotfix",
            "description": "Allow deployment of hotfix.",
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
            self._actions = None
            self._pass_summary = (
                "@%s has overridden the original result"
                % github_body.get("sender").get("login")
            )
            return True

        for block_time in settings.get("block_times", []):
            cron_expression = cronex.CronExpression(block_time)

            if current_time is None:
                current_time = time.gmtime(time.time())[:5]

            self.current_time = current_time
            if cron_expression.check_trigger(current_time) is True:
                return False

        self._actions = None
        return True

    @property
    def fail_text(self) -> str:
        return "The current time is: {}\n\nCode Freeze Settings are: {}".format(
            datetime.datetime(*self.current_time).strftime("%H:%M on %b %d %Y"),
            self.settings.get("block_times"),
        )

    @property
    def pass_summary(self) -> str:
        return self._pass_summary

    @pass_summary.setter
    def pass_summary(self, pass_summary):
        self._pass_summary = pass_summary

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, actions):
        self._actions = actions
