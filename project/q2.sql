--Notes--
--1) in ddl we cannot express overlap, nor can we express cover of relations.
--   manger and tech expert cannot express overlap
--   premium and regular families cannot express cover

--2) in ddl we cannot enforce relations to express having a at least one row of a certain value
--   at least one time, in other words, we cannot enforce values and number of rows in relations,
--   we can only enforce the model and range of values of the relations.
--   in our case, we cant enforce that each family has a least one DTA, nor can we enforce that each
--   DTA has at least one channel.

--   We would like to point out that we are aware that we can add a default row to overcome
--   this issue, but we didnt do it because it doesnt correlate with the story.
--   For example, adding a row of a DTA per family with assumption to default values, but as we
--   mentioned, it just doesnt make sense based on the story.



-- We assume that each department has only one manager running it.
create table Department (
    dName VARCHAR(100) primary key,
    dDescription VARCHAR(100),
    eID NUMERIC(9,0) NOT NULL,
);

create table Employee (
    eID NUMERIC(9,0) PRIMARY KEY,
    eName VARCHAR(100),
    dName VARCHAR(100) NOT NULL,
    FOREIGN KEY (dName) references Department ON DELETE CASCADE
);

-- We assume that each manager runs only one department.
-- its also not possible any other way as the only primary key of Manager relations is
-- their ID. so we cannot express one manager running multiple departments.
-- (well at least as its based in this story).
create table Manager (
    eID NUMERIC(9,0) PRIMARY KEY,
    mSalary NUMERIC(38,0),
    FOREIGN KEY (eID) references Employee ON DELETE CASCADE
);

create table Tech_Exp (
    eID NUMERIC(9,0) PRIMARY KEY,
    tExpertise VARCHAR(100),
    FOREIGN KEY (eID) references Employee ON DELETE CASCADE
);

ALTER TABLE Department
    ADD FOREIGN KEY (eID) REFERENCES Manager;


-- From the story, families that get a 7 or above score in the fLevel field become premium
-- families, otherwise they become regular ones.
-- in ddl we cannot move around rows from one relation to another relation based on their values,
-- So, We Assume that when adding families to the data base, we know beforehand whether they
-- are premium or regular and add them to both to the main relation "Family" and the relative
-- relation "premium family" or "regular family" based on the on the fLevel.

-- From the story we dont know what the family identifier consists of, so we wrote accordingly
-- to the value limits in the question.
CREATE TABLE Family (
    fID VARCHAR(100) primary key,
    fName VARCHAR(100),
    fLevel NUMERIC(1,0) check (fLevel > 0),
);


CREATE TABLE Family_Member(
    fID VARCHAR(100),
    fmName VARCHAR(100),
    fmPhone VARCHAR(100),
    fmBirth_date VARCHAR(100),
    primary key (fID, fmName),
    foreign key (fID) references Family ON DELETE CASCADE
);

CREATE TABLE Premium_Family (
    fID VARCHAR(100) primary key,
    eID NUMERIC(9,0),
    FOREIGN KEY (eID) references Tech_Exp ON DELETE CASCADE,
    FOREIGN KEY (fID) references Family ON DELETE CASCADE
);

CREATE TABLE Regular_Family (
    fID VARCHAR(100) primary key,
    FOREIGN KEY (fID) references Family ON DELETE CASCADE
);

-- In the story, its not requested to save information about the Manager the request was forwarded
-- to, so we didnt do it and we assumed that the same identifiers are set for forwarded requests.

-- We assume that when either a manager or a family is deleted from the database, so will the request
-- be deleted (same for the forwarded requests).

-- As we assumed in the ERD, we also assume here that because each family can only send one request
-- per date format (we dont know which)
CREATE TABLE Request (
    fID VARCHAR(100),
    eID NUMERIC(9,0),
    rDate VARCHAR(100),
    rDecision VARCHAR(100),
    PRIMARY KEY (fID, eID, rDate),
    foreign key (fID) references Regular_Family ON DELETE CASCADE,
    foreign key (eiD) references Manager ON DELETE CASCADE
);

CREATE TABLE Forwarded_Request (
    fID VARCHAR(100),
    eID NUMERIC(9,0),
    rDate VARCHAR(100),
    frReason VARCHAR(100),
    PRIMARY KEY (fID, eID, rDate),
    foreign key (fID, eID, rDate) references Request ON DELETE CASCADE
);

-- In ddl we cannot confirm that the order of installation of DTAs are in
-- ascending order like requested in the story
CREATE TABLE DTA (
    fID VARCHAR(100),
    dtaNumber NUMERIC(38,0),
    FOREIGN KEY (fID) references Family ON DELETE CASCADE,
    PRIMARY KEY (fID, dtaNumber)
);


-- We assume that because we cant swap the DTA, when its deleted, it means the
-- family left the service (deleted).

--  the family table could be approached in a few ways, we chose to split into 2 sub tables,
--  even if we chose to only implement one table and to check the family wealth
--  level and according to that to add a reference to a tech expert (or null if below 7),
--  we still couldn't make sure that when a DTA is broken that it will be sent back to the family
--  tech expect in case they are premium, because in the case of the eID referencing to a regular familys
--  row, the tech expect would be set to null and then the relation would cause problems.

--  A possible solution is to make "premium repairs" and "regular repairs" tables, reference them
--  accordingly, and assume that upon repair, we will add repair relations according to which family
--  sent the repair but it just doesnt line up with the story, so we didnt implement that.
CREATE TABLE Repair (
    fID VARCHAR(100),
    dtaNumber NUMERIC(38,0),
    eID NUMERIC(9,0),
    rCost NUMERIC(38,0),
    PRIMARY KEY (fID, dtaNumber),
    foreign key (fID, dtaNumber) references DTA ON DELETE CASCADE,
    foreign key (eID) references Tech_Exp ON DELETE set null
);

CREATE TABLE Channel(
    cNum NUMERIC(38,0) primary key,
    cName VARCHAR(100),
);


CREATE TABLE Channel_In_DTA(
    cNum NUMERIC(38,0),
    fID VARCHAR(100),
    dtaNumber NUMERIC(38,0),
    PRIMARY KEY (cNum, dtaNumber),
    FOREIGN KEY (cNum) references Channel ON DELETE CASCADE,
    FOREIGN KEY (fID, dtaNumber) references DTA ON DELETE CASCADE
);

-- To make sure that we can switch between the same channels multiple times,
-- on the same DTA, the specified time will also act as a primary key.
CREATE TABLE Switch_Channel (
    cNum NUMERIC(38,0),
    fID VARCHAR(100),
    dtaNumber NUMERIC(38,0),
    specTime VARCHAR(100),
    PRIMARY KEY (cNum, dtaNumber, specTime),
    FOREIGN KEY (cNum) references Channel ON DELETE CASCADE,
    FOREIGN KEY (fID, dtaNumber) references DTA ON DELETE CASCADE
);

CREATE Table Show (
    sName VARCHAR(100) PRIMARY KEY,
    sGenre VARCHAR(100),
    sLength NUMERIC(38,0)
);

-- To be abe to air the same show at the same channel multiple times
-- The specified time will also act as a primary key.
Create Table Air_On (
    cNum NUMERIC(38,0),
    sName VARCHAR(100),
    airTime VARCHAR(100),
    PRIMARY KEY (cNum, sName, airTime),
    FOREIGN KEY (cNum) references Channel ON DELETE CASCADE,
    FOREIGN KEY (sName) references Show ON DELETE CASCADE
);
