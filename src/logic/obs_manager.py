from obswebsocket import obsws, requests
from obswebsocket.exceptions import ConnectionFailure
from logic.config import cfg

class OBSManager:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.ws = None
        self.input_kind_map = {}

    def connect(self):
        try:
            self.ws = obsws(self.host, self.port, self.password)
            self.ws.connect()
            print("Connected to OBS WebSocket")
            self.refresh_data()

        except ConnectionFailure as e:
            print(f"Failed to connect to OBS WebSocket: {e}")
            self.ws = None

    def disconnect(self):
        if self.ws:
            self.ws.disconnect()
            print("Disconnected from OBS WebSocket")
            self.ws = None

    def getInputKind(self, input_name):
        return self.input_kind_map.get(input_name, "unknown")

    def getKindEmoji(self, kind):
        mapping = {
            "text": "📝",
            "image": "📷",
            "browser": "🌐",
            "ffmpeg": "🎥",
            "capture": "📡",
            "unknown": "❓",
        }
        for key in mapping:
            if key in kind:
                return mapping[key]
        return mapping["unknown"]

    def refresh_data(self):
        if not self.ws:
            print("Not connected to OBS WebSocket")
            return [], []

        scenes_list = []
        inputs_list = []

        try:
            response_scenes = self.ws.call(requests.GetSceneList())
            raw_scenes = response_scenes.getScenes()
            scenes_list = [s["sceneName"] for s in raw_scenes]
            response_inputs = self.ws.call(requests.GetInputList())
            raw_inputs = response_inputs.getInputs()

            for item in raw_inputs:
                input_name = item["inputName"]
                input_kind = item["inputKind"]
                inputs_list.append(input_name)
                self.input_kind_map[input_name] = input_kind

        except Exception as e:
            print(f"Error refreshing data from OBS: {e}")

        return sorted(scenes_list), sorted(inputs_list)

    def set_source_value(self, source_name, new_value):
        if not self.ws:
            print("Not connected to OBS WebSocket")
            return
        kind = self.input_kind_map[source_name]
        settings = {}

        if "text" in kind:
            settings = {"text": str(new_value)}

        elif "image" in kind:
            settings = {"file": str(new_value)}
        elif "browser" in kind:
            settings = {"url": str(new_value)}
        elif "ffmpeg" in kind:
            settings = {"local_file": str(new_value)}
        else:
            print(f"Unsupported source type: '{kind}' for {source_name}")
            return

        try:
            self.ws.call(
                requests.SetInputSettings(
                    inputName=source_name, inputSettings=settings, overlay=True
                )
            )
            print(f"Updated '{source_name}' with new value: {new_value}")
        except Exception as e:
            print(f"Error setting source value in OBS: {e}")

    def get_source_by_name(self, source_name):
        if not self.ws:
            print("Not connected to OBS WebSocket")
            return None
        try:
            response_inputs = self.ws.call(requests.GetInputList())
            raw_inputs = response_inputs.getInputs()
            for item in raw_inputs:
                if item["inputName"] == source_name:
                    return item
            print(f"Source '{source_name}' not found in OBS.")
            return None
        except Exception as e:
            print(f"Error retrieving source from OBS: {e}")
            return None
    
    def test_connection(self, host, port, password):
        try:
            test_ws = obsws(host, port, password)
            test_ws.connect()
            test_ws.disconnect()
            return True
        except ConnectionFailure:
            return False


obs_manager = OBSManager(
    cfg.data.get("obs_host"),
    cfg.data.get("obs_port"),
    cfg.data.get("obs_password")
)
