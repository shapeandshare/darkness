
# Darkness Game Engine

## Overview
Darkness is a tile-based game engine that provides procedural world generation, entity lifecycle management, and realtime state processing. The system consists of a server-side component (Darkness) with MongoDB persistence and background state processing (Chrono), paired with a client visualization tool (Light). Together, these components form a complete engine for generating and managing dynamic tile-based worlds with automated lifecycle updates and real-time visualization of world state.
## Key Features

### World Generation
- Procedural world and terrain generation
- Chunked world management
- Tile-based environment system
- Entity lifecycle management

### Environment Types
- Ocean tiles with varying depths
- Land masses with varied terrain
- Shore and transition zones
- Forest and vegetation areas

### Entity System
- Flora: Trees, Grass
- Fauna: Fish
- Funga: Fungi
- Entity lifecycle states
- Automatic entity propagation

### State Management
- Real-time state updates
- Chunk quantum processing
- Entity lifecycle progression
- State persistence

## Architecture

```mermaid
graph TD
    %% External Client Components
    LightClient[Light Client]
    DarknessSDK[Darkness SDK]
    AbstractCommand[Abstract Command]
    StateClient[State Client]
    CommandOptions[Command Options]

    %% Command Types
    WorldCommands[World Commands]
    ChunkCommands[Chunk Commands]
    TileCommands[Tile Commands]
    EntityCommands[Entity Commands]
    MetricCommands[Metric Commands]

    %% Main Services
    StateService[State Service]
    ChronoService[Chrono Service]
    ChronoWorker[Chrono Worker]
    
    %% API Layer
    StateAPI[State API]
    ChronoAPI[Chrono API]
    MetricsAPI[Metrics API]
    HealthAPI[Health Check]

    %% Factory System
    WorldFactory[World Factory]
    ChunkFactory[Chunk Factory]
    EntityFactory[Entity Factory]
    FlatChunkFactory[Flat Chunk Factory]

    %% Data Models
    World[World Model]
    Chunk[Chunk Model]
    Tile[Tile Model]
    Entity[Entity Model]
    
    %% Database
    MongoDB[(MongoDB)]
    DAOClient[DAO Client]

    %% Entity Types
    Fauna[Fauna]
    Flora[Flora]
    Funga[Funga]
    
    %% Entity Subtypes
    Fish[Fish] --> Fauna
    Tree[Tree] --> Flora
    Grass[Grass] --> Flora
    Fungi[Fungi] --> Funga

    %% Chrono Worker System
    ChronoContext[Chrono Context Manager]
    ChronoStateClient[Chrono State Client]
    ChronoRouter[Chrono Router]
    ChronoLoop[Chrono Event Loop]

    %% External Client Connections
    LightClient --> DarknessSDK
    DarknessSDK --> StateClient
    StateClient --> |inherits| AbstractCommand
    StateClient --> CommandOptions
    
    %% Command Hierarchies
    AbstractCommand --> WorldCommands
    AbstractCommand --> ChunkCommands
    AbstractCommand --> TileCommands
    AbstractCommand --> EntityCommands
    AbstractCommand --> MetricCommands

    WorldCommands -.->|HTTP| StateAPI
    ChunkCommands -.->|HTTP| StateAPI
    TileCommands -.->|HTTP| StateAPI
    EntityCommands -.->|HTTP| StateAPI
    MetricCommands -.->|HTTP| MetricsAPI

    %% ChronoWorker Dependencies
    ChronoWorker --> ChronoContext
    ChronoContext --> ChronoStateClient
    ChronoWorker --> ChronoRouter
    ChronoRouter --> ChronoLoop
    ChronoStateClient -.->|HTTP| StateAPI
    ChronoLoop --> |Periodic World Updates| ChronoStateClient

    %% Service Layer Dependencies
    StateService --> WorldFactory
    StateService --> ChunkFactory
    StateService --> EntityFactory
    StateService --> DAOClient
    
    ChronoService --> StateService

    %% API Layer Dependencies
    StateAPI --> StateService
    ChronoAPI --> ChronoService
    
    %% Factory Dependencies
    WorldFactory --> DAOClient
    ChunkFactory --> DAOClient
    EntityFactory --> DAOClient
    FlatChunkFactory --> EntityFactory
    
    %% Data Access
    DAOClient --> MongoDB
    
    %% Model Relationships
    World --> |contains| Chunk
    Chunk --> |contains| Tile
    Tile --> |contains| Entity
    Entity --> |is type of| Fauna
    Entity --> |is type of| Flora
    Entity --> |is type of| Funga

    %% Component Groups
    subgraph "External Client Layer"
        LightClient
        DarknessSDK
        StateClient
        AbstractCommand
        CommandOptions
        WorldCommands
        ChunkCommands
        TileCommands
        EntityCommands
        MetricCommands
    end

    subgraph "API Layer"
        StateAPI
        ChronoAPI
        MetricsAPI
        HealthAPI
    end

    subgraph "Service Layer"
        StateService
        ChronoService
    end

    subgraph "Factory Layer"
        WorldFactory
        ChunkFactory
        EntityFactory
        FlatChunkFactory
    end

    subgraph "Chrono Worker System"
        ChronoWorker
        ChronoContext
        ChronoStateClient
        ChronoRouter
        ChronoLoop
    end

    subgraph "Data Model"
        World
        Chunk
        Tile
        Entity
        Fauna
        Flora
        Funga
        Fish
        Tree
        Grass
        Fungi
    end

    subgraph "Data Access Layer"
        DAOClient
        MongoDB
    end

    %% Styling
    classDef api fill:#f9f,stroke:#333,stroke-width:2px
    classDef service fill:#bbf,stroke:#333,stroke-width:2px
    classDef factory fill:#ffd,stroke:#333,stroke-width:2px
    classDef model fill:#dfd,stroke:#333,stroke-width:2px
    classDef database fill:#fdd,stroke:#333,stroke-width:2px
    classDef chrono fill:#dff,stroke:#333,stroke-width:2px
    classDef client fill:#fdf,stroke:#333,stroke-width:2px
    
    class StateAPI,ChronoAPI,MetricsAPI,HealthAPI api
    class StateService,ChronoService service
    class WorldFactory,ChunkFactory,EntityFactory,FlatChunkFactory factory
    class World,Chunk,Tile,Entity,Fauna,Flora,Funga,Fish,Tree,Grass,Fungi model
    class MongoDB,DAOClient database
    class ChronoWorker,ChronoContext,ChronoStateClient,ChronoRouter,ChronoLoop chrono
    class LightClient,DarknessSDK,StateClient,AbstractCommand,CommandOptions,WorldCommands,ChunkCommands,TileCommands,EntityCommands,MetricCommands client
```


### Major Components

#### Darkness Server
- FastAPI-based REST API
- MongoDB persistence layer
- Factory system for object creation
- Service layer for business logic
- Background processing system

#### Light Client
- Pygame-based visualization
- Real-time state updates
- Tile rendering system
- Entity visualization
- User interaction handling

#### Chrono Worker
- Background state processing
- Entity lifecycle management
- World state updates
- Quantum processing system

## Requirements

### Server Requirements
- Python 3.12 or higher
- MongoDB 7.0 or higher
- FastAPI
- uvicorn
- pymongo
- pydantic

### Client Requirements
- Python 3.12 or higher
- Pygame
- pydantic
- requests

### Platform Support
- Linux
- macOS
- Windows

## Installation

### Server Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install shapeandshare.darkness
```

### Client Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install shapeandshare.light
```

## Setup

### MongoDB Setup
```bash
# For macOS with MongoDB Version 7.0.14
curl https://fastdl.mongodb.org/osx/mongodb-macos-arm64-7.0.14.tgz -o mongodb.tgz
tar xfvz mongodb.tgz
mkdir -p data
```

### Environment Variables
```bash
# Server
export DARKNESS_MONGODB_HOST="localhost"
export DARKNESS_MONGODB_PORT="27017"
export DARKNESS_MONGODB_DATABASE="darkness"

# Client
export DARKNESS_TLD="localhost:8000"
export DARKNESS_SERVICE_SLEEP_TIME="1.0"
export DARKNESS_SERVICE_TIMEOUT="5.0"
export DARKNESS_SERVICE_RETRY_COUNT="5"

# Chrono Worker
export DARKNESS_WORKER_CHRONO_SLEEP_TIME="10"
```

## Running the System

### Using Local Infrastructure Scripts
The system provides scripts in `infra/local` for managing all components:

```bash
# Initial setup and startup of all components
infra/local/startup.sh

# Individual component management:
# MongoDB setup and start
infra/local/01_mongodb_setup.sh
infra/local/03_mongodb_run.sh

# State service setup and start
infra/local/02_state_setup.sh
infra/local/04_state_run.sh

# Chrono worker start
infra/local/05_chrono_run.sh

# System shutdown
infra/local/shutdown.sh
```

### Component Status
Check running components:
```bash
screen -ls
```

Expected output:
```
There are screens on:
        12345.darkness-mongodb     (Detached)
        12346.darkness-state       (Detached)
        12347.darkness-chrono      (Detached)
```

### Screen Session Management
Attach to a component screen:
```bash
screen -r darkness-state    # Attach to state service
screen -r darkness-mongodb  # Attach to MongoDB
screen -r darkness-chrono   # Attach to chrono worker
```

Detach from a screen session: Press `Ctrl+A` followed by `D`

### Starting Light Client
With the Darkness infrastructure running:
```bash
light
```
