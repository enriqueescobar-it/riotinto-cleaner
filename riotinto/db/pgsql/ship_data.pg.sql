CREATE TABLE ship_data (
    MovementDateTime TIMESTAMP,
    Destination VARCHAR(255),
    DestinationTidied VARCHAR(255),
    Speed FLOAT,
    AdditionalInfo VARCHAR(255),
    CallSign VARCHAR(50),
    Heading FLOAT,
    MMSI BIGINT,
    MovementID BIGINT,
    ShipName VARCHAR(255),
    ShipType VARCHAR(50),
    Beam FLOAT,
    Draught FLOAT,
    Length FLOAT,
    ETA TIMESTAMP,
    MoveStatus VARCHAR(50),
    LadenStatus VARCHAR(50),
    LRIMOShipNo BIGINT,
    Latitude FLOAT,
    Longitude FLOAT,
    BeamRatio FLOAT
);