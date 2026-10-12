
import unittest
from unittest.mock import MagicMock, patch

import traffic_generator


class TestTrafficGenerator(unittest.TestCase):

    @patch("traffic_generator.log_event")
    @patch("traffic_generator.socket.socket")
    def test_successful_connection(self, mock_socket, mock_log):
        client = MagicMock()
        mock_socket.return_value.__enter__.return_value = client

        client.getsockname.return_value = ("127.0.0.1", 12345)
        client.recv.return_value = b"Message received successfully!"

        result = traffic_generator.attempt_connection(
            "127.0.0.1", 5000, send_message=True
        )

        self.assertEqual(result, "success")
        mock_log.assert_called_once()

        event = mock_log.call_args.kwargs
        self.assertEqual(event["source_ip"], "127.0.0.1")
        self.assertEqual(event["destination_ip"], "127.0.0.1")
        self.assertEqual(event["destination_port"], 5000)
        self.assertEqual(event["event_type"], "connection_attempt")
        self.assertEqual(event["status"], "success")

    @patch("traffic_generator.log_event")
    @patch("traffic_generator.socket.socket")
    def test_refused_connection(self, mock_socket, mock_log):
        client = MagicMock()
        mock_socket.return_value.__enter__.return_value = client

        client.getsockname.return_value = ("127.0.0.1", 12345)
        client.connect.side_effect = ConnectionRefusedError

        result = traffic_generator.attempt_connection(
            "127.0.0.1", 5001
        )

        self.assertEqual(result, "connection_refused")
        mock_log.assert_called_once()

        event = mock_log.call_args.kwargs
        self.assertEqual(event["destination_port"], 5001)
        self.assertEqual(event["status"], "connection_refused")


if __name__ == "__main__":
    unittest.main()
