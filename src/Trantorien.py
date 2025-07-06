import socket

class Trantorien:
  """
  @class Trantorien
  @brief Represents an AI player (Trantorien) in the Zappy game.

  Handles TCP socket communication with the server and encapsulates basic player actions.
  """

  def __init__(self, host: str, port: int, team: str):
    """
    @brief Constructor for the Trantorien class.

    @param host IP address or hostname of the server
    @param port Port number to connect to
    @param team Team name to authenticate with
    """
    self.host = host
    self.port = port
    self.team = team
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def connect(self):
    """
    @brief Connects to the Zappy server and performs initial handshake.

    This includes receiving the welcome message, sending the team name,
    and reading the number of available slots and map dimensions.
    """
    self.sock.connect((self.host, self.port))
    print(self._recv_line())
    self._send_line(self.team)
    print("Slot info:", self._recv_line().strip())
    print("Map size:", self._recv_line().strip())

  def _recv_line(self) -> str:
    """
    @brief Receives a line from the server.

    @return A complete message line (ending with newline) from the server.
    """
    data = b""
    while not data.endswith(b'\n'):
      chunk = self.sock.recv(1)
      if not chunk:
        break
      data += chunk
    return data.decode()

  def _send_line(self, msg: str):
    """
    @brief Sends a line to the server.

    @param msg The message to send (newline will be appended automatically).
    """
    self.sock.sendall((msg + '\n').encode())

  def forward(self) -> str:
    """
    @brief Moves the player forward by one tile.

    @return Server response (usually "ok" or "ko").
    """
    self._send_line("Forward")
    return self._recv_line().strip()

  def right(self) -> str:
    """
    @brief Rotates the player 90° to the right.

    @return Server response.
    """
    self._send_line("Right")
    return self._recv_line().strip()

  def left(self) -> str:
    """
    @brief Rotates the player 90° to the left.

    @return Server response.
    """
    self._send_line("Left")
    return self._recv_line().strip()

  def look(self) -> str:
    """
    @brief Makes the player look around.

    @return Server response with tile contents.
    """
    self._send_line("Look")
    return self._recv_line().strip()

  def inventory(self) -> str:
    """
    @brief Checks the player's inventory.

    @return Server response with inventory details.
    """
    self._send_line("Inventory")
    return self._recv_line().strip()

  def broadcast(self, message: str) -> str:
    """
    @brief Broadcasts a message to all other players.

    @param message The text message to send.
    @return Server response.
    """
    self._send_line(f"Broadcast {message}")
    return self._recv_line().strip()

  def connect_nbr(self) -> str:
    """
    @brief Request connection slots informations.
    @return Server response.
    """
    self._send_line("Connect_nbr")
    return self._recv_line().strip()

  def close(self):
    """
    @brief Closes the connection to the server.
    """
    self.sock.close()
