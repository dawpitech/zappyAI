# Zappy AI - Python Implementation

A sophisticated AI client for the Zappy game using Goal-Oriented Action Planning (GOAP) and the F.U.C.K. protocol for inter-AI communication.

## Overview

This AI implementation controls a Trantorian drone in the Zappy world, aiming to reach the maximum elevation level (8) through strategic resource gathering, team coordination, and efficient incantation rituals.

## Features

- **GOAP-based Decision Making**: Uses Goal-Oriented Action Planning for intelligent behavior
- **Inter-AI Communication**: Implements the F.U.C.K. protocol for coordinated team strategies
- **Resource Management**: Efficient food and stone collection algorithms
- **Elevation Strategy**: Optimized incantation planning and execution
- **Team Coordination**: Collaborative elevation rituals with other team members

## Architecture

### Core Components

1. **GOAP Engine** (`goap/`)
   - Goal-based action planning system
   - Dynamic priority adjustment
   - State management and action execution

2. **Protocol Handler** (`protocol/`)
   - F.U.C.K. protocol implementation
   - Message encoding/decoding with Caesar cipher
   - Coordinate-based message interpretation

3. **Game Logic** (`game/`)
   - Zappy game state management
   - Resource tracking and inventory management
   - Vision and sound processing

4. **AI Controller** (`ai/`)
   - Main AI decision loop
   - Action execution and response handling
   - Team coordination strategies

## F.U.C.K. Protocol Implementation

### Message Structure

The AI uses the Federated Unified Chat Knowledge (F.U.C.K.) protocol for secure inter-AI communication:

```json
{
  "s": "IA3",           // Sender ID
  "p": "encoded_msg",   // Caesar-encoded payload
  "mid": "14826"        // Message ID
}
```

### Message Types

Based on coordinate modulo 6:

| Type | Meaning | Additional Data |
|------|---------|----------------|
| 0 | "I'm born" | None |
| 1 | "Provide latest message IDs and AI ID" | `[id1, id2, ...],IAid` |
| 2 | "I have evolved to N" | Evolution level: `N` |
| 3 | "I need specific resources" | `[resource: amount, ...]` |
| 4 | "I am going to evolve" | Target level: `N` |
| 5 | "I'm alive" | None |

### Caesar Cipher Key

The protocol uses a sophisticated mathematical formula to generate the Caesar cipher key:

```
key = F(U+C)K+TH + I+S
```

Where each variable represents a complex mathematical expression involving:
- Trigonometric functions and constants
- Definite integrals
- Infinite series
- Special functions (Dilogarithm, Binomial coefficients)

## GOAP Implementation

### Goals

- **Survive**: Maintain food levels above critical threshold
- **Collect Resources**: Gather stones needed for elevation
- **Evolve**: Reach higher elevation levels
- **Coordinate**: Assist team members in elevation rituals

### Actions

- **Movement**: Navigate efficiently across the map
- **Resource Collection**: Pick up food and stones
- **Broadcasting**: Communicate with team members
- **Incantation**: Initiate elevation rituals
- **Ejection**: Remove competitors from strategic locations

### Planning Algorithm

The GOAP planner evaluates:
1. Current world state
2. Available actions and their preconditions
3. Goal priorities and costs
4. Optimal action sequence to achieve goals

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd zappy/ai

# Install dependencies
pip install -r requirements.txt

# Install the AI package
pip install -e .
```

## Usage

### Basic Usage

```bash
./zappy_ai -p <port> -n <team_name> -h <hostname>
```

### Parameters

- `-p port`: Server port number
- `-n name`: Team name for authentication
- `-h machine`: Server hostname (default: localhost)

### Example

```bash
# Connect to local server on port 4242 with team "Epitech"
./zappy_ai -p 4242 -n Epitech -h localhost
```

## Configuration

### AI Parameters

Edit `config/ai_config.py`:

```python
# GOAP Configuration
GOAP_PLANNING_DEPTH = 10
GOAP_REPLANNING_INTERVAL = 5.0

# Survival Parameters
CRITICAL_FOOD_THRESHOLD = 50
OPTIMAL_FOOD_LEVEL = 200

# Communication Settings
BROADCAST_INTERVAL = 30.0
PROTOCOL_ENCRYPTION = True
```

### Protocol Settings

Edit `config/protocol_config.py`:

```python
# F.U.C.K. Protocol Configuration
CAESAR_KEY_FORMULA = True  # Use mathematical formula for key
FALLBACK_CAESAR_KEY = 13   # Fallback if formula fails
MESSAGE_TIMEOUT = 10.0
MAX_RETRIES = 3
```

## Development

### Project Structure

```
zappy_ai/
├── app
│   └── zappyAI.py
├── README.md
├── Share
│   └── OpenSans Regular.ttf
└── src
    ├── actions
    │   ├── action.py
    │   ├── look_action.py
    │   ├── move_forward_action.py
    │   ├── take_object_action.py
    │   ├── turn_left_action.py
    │   └── turn_right_action.py
    ├── goals
    │   ├── explore_goal.py
    │   ├── find_food_goal.py
    │   ├── goal.py
    │   └── survive_goal.py
    ├── local_map.py
    ├── planner.py
    ├── state.py
    ├── test.py
    └── Trantorien.py
```

### Adding New Actions

1. Define the action in `src/actions/`:

```python
class NewAction(Action):
    def __init__(self):
        super().__init__("new_action")
        self.preconditions = {"condition": True}
        self.effects = {"result": True}
        self.cost = 1.0

    def execute(self, agent, world_state):
        # Implementation
        pass
```

2. Register the action in the planner
3. Add tests for the new action

## Advanced Features

### Team Coordination

The AI implements sophisticated team coordination:

- **Resource Sharing**: Alerts team members about resource locations
- **Elevation Coordination**: Organizes multi-player incantation rituals
- **Strategic Positioning**: Coordinates territorial control

### Adaptive Behavior

- **Dynamic Goal Prioritization**: Adjusts goals based on world state
- **Learning from Failures**: Improves strategies based on outcomes
- **Environmental Adaptation**: Responds to changing world conditions

### Security Features

- **Encrypted Communications**: Uses F.U.C.K. protocol encryption
- **Message Authentication**: Verifies message integrity
- **Anti-Griefing**: Detects and responds to hostile behavior

## Performance Optimization

### Efficient Pathfinding

- **A* Algorithm**: Optimal path planning
- **Cached Routes**: Reuses computed paths
- **Dynamic Obstacles**: Adapts to world changes

### Resource Optimization

- **Memory Management**: Efficient state representation
- **Network Optimization**: Minimizes bandwidth usage
- **CPU Optimization**: Optimized GOAP planning

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Check server availability
   - Verify port and hostname
   - Ensure team name is correct

2. **Protocol Errors**
   - Verify F.U.C.K. protocol implementation
   - Check Caesar cipher key calculation
   - Validate message format

3. **GOAP Planning Issues**
   - Increase planning depth
   - Check action preconditions
   - Verify world state accuracy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests
5. Submit a pull request

## License

This project is part of the Epitech Zappy project and follows the school's academic guidelines.

## Authors

- **Team**: Louka ORTEGA CAND | Antton DUCOS | Antoine BELANGER | Maxime GOYHENECHE | Remy THAI
- **Protocol**: F.U.C.K. Protocol Implementation
- **AI Engine**: GOAP-based Decision Making

## References

- [GOAP Algorithm Documentation](https://en.wikipedia.org/wiki/Goal-oriented_action_planning)
