"""Простой HTTP-сервер для домашней работы 21.2."""

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


class HomeworkHandler(BaseHTTPRequestHandler):
    """Обработчик запросов для ДЗ по основам верстки."""

    HTML_DIR = os.path.join(os.path.dirname(__file__), "..", "html")

    def _read_html(self, filename: str) -> bytes:
        """Читает HTML-файл через контекстный менеджер."""
        filepath = os.path.join(self.HTML_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().encode("utf-8")

    def _send_response(
        self,
        status_code: int,
        content: bytes,
        content_type: str = "text/html; charset=utf-8",
    ) -> None:
        """Отправляет HTTP-ответ с заданным статусом и контентом."""
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:
        """Обрабатывает GET-запросы."""
        try:
            if self.path == "/contacts":
                html_content = self._read_html("contacts.html")
                self._send_response(200, html_content)
            else:
                html_content = self._read_html("404.html")
                self._send_response(404, html_content)
        except FileNotFoundError:
            error_content = self._read_html("500.html")
            self._send_response(500, error_content)
        except Exception:
            error_content = self._read_html("500.html")
            self._send_response(500, error_content)

    def do_POST(self) -> None:
        """Обрабатывает POST-запросы и выводит данные в консоль."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            parsed_data = parse_qs(post_data)

            print("=" * 50)
            print("📥 Получены POST-данные:")
            for key, values in parsed_data.items():
                print(f"  {key}: {', '.join(values)}")
            print("=" * 50)

            # Перенаправляем на страницу контактов после обработки
            html_content = self._read_html("contacts.html")
            self._send_response(200, html_content)
        except Exception:
            error_content = self._read_html("500.html")
            self._send_response(500, error_content)


def run_server(host: str = "localhost", port: int = 8000) -> None:
    """Запускает HTTP-сервер."""
    server = HTTPServer((host, port), HomeworkHandler)
    print(f"🚀 Сервер запущен: http://{host}:{port}")
    print(f"📄 Страница контактов: http://{host}:{port}/contacts")
    print("⏹️  Для остановки нажмите Ctrl+C")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен.")
        server.server_close()


if __name__ == "__main__":
    run_server()
