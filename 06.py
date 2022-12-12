from collections import deque

PACKET_START_MARKER_LEN, MESSAGE_START_MARKER_LEN = 4, 14

DatastreamBuffer = str
MarkerPosition = int


def parse_input() -> DatastreamBuffer:
    with open('inputs/06.in', 'r') as f:
        return f.read()


def search_for_marker(datastream_buffer: DatastreamBuffer, marker_len: int) -> MarkerPosition:
    read_buffer = deque(datastream_buffer[:marker_len])
    for i in range(marker_len, len(datastream_buffer)):
        if len(set(read_buffer)) == marker_len:
            return i

        read_buffer.popleft()
        read_buffer.append(datastream_buffer[i])


def detect_packet(datastream_buffer: DatastreamBuffer) -> MarkerPosition:
    return search_for_marker(datastream_buffer, PACKET_START_MARKER_LEN)


def detect_message(datastream_buffer: DatastreamBuffer) -> MarkerPosition:
    return search_for_marker(datastream_buffer, MESSAGE_START_MARKER_LEN)


input = parse_input()
print(detect_packet(input))
print(detect_message(input))
