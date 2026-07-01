import unittest

from aura.application.services.robot_state_store import RobotStateStore


class RobotStateStoreTests(unittest.TestCase):
    def test_records_commands_and_errors(self):
        state_store = RobotStateStore()

        state_store.record_command("Test command")
        state_store.record_error("Test error")

        state = state_store.snapshot()
        self.assertEqual(state.command_count, 1)
        self.assertEqual(state.error_count, 1)
        self.assertEqual(state.last_command, "Test command")
        self.assertEqual(state.last_error, "Test error")
        self.assertEqual(len(state.events), 2)

    def test_event_log_is_bounded(self):
        state_store = RobotStateStore()

        for index in range(25):
            state_store.record_command(f"Command {index}")

        state = state_store.snapshot()
        self.assertEqual(len(state.events), 20)
        self.assertEqual(state.events[-1].message, "Command 24")


if __name__ == "__main__":
    unittest.main()
