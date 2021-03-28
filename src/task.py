import cronex
import time
import datetime

from base_task import BaseTask


class Task(BaseTask):
    """
    Verifies the Title of a Pull Request matches a provided regex.
    """

    # current_time is only passed in for testing purposes
    def _execute(self, github_body, current_time = None) -> bool:
        self.pass_text = ""

        for block_time in self.settings.get('block_times', []):
            cron_expression = cronex.CronExpression(block_time)

            if current_time is None:
                current_time = time.gmtime(time.time())[:5]

            self.current_time = current_time
            if cron_expression.check_trigger(current_time) is True:
                return False

        return True

    def _requested_action(self, github_body) -> bool:
        if github_body.get("requested_action").get("identifier") == "override":
            self.pass_text = "@%s has overridden the original result" % github_body.get(
                "sender"
            ).get("login")
            return True
        return False

    def _get_task_name(self):
        return "Code Freeze"

    def _get_task_slug(self) -> str:
        return "code-freeze"

    def _get_fail_summary(self) -> str:
        return "Cannot deploy during Code Freeze."

    def _get_fail_text(self) -> str:
        return "The current time is: %s\n\nCode Freeze Settings are: %s" % (datetime.datetime(*self.current_time).strftime('%H:%M on %b %d %Y'), self.settings.get('block_times'))

    def _get_pass_summary(self) -> str:
        return ":+1:"

    def _get_pass_text(self) -> str:
        return self.pass_text

    def _get_actions(self):
        return [
            {
                "label": "Override",
                "identifier": "override",
                "description": "Allow exception for PR Too Big",
            }
        ]
