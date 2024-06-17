--The database is under the assumptions that:
-- 1) The numeric types are whole numbers.
-- 2) The length of numeric types is shorter than 38. (numeric limit)
-- 3) Company establishment date (cBirth) is a string

CREATE TABLE Company(
    cID NUMERIC(38,0) PRIMARY KEY,
    cName VARCHAR(50),
    cBirth VARCHAR(50),
    cSite VARCHAR(50) check ( RIGHT(cSite, 4) =  '.com' ) UNIQUE,
    cField VARCHAR(50)
);


CREATE TABLE Department(
    dName VARCHAR(50),
    cID NUMERIC(38,0),
    dDescription VARCHAR(50),
    UNIQUE (cID ,dDescription),
    PRIMARY KEY (dName, cID),
    FOREIGN KEY (cID) references Company
);


CREATE TABLE Salary(
    pName VARCHAR(50),
    sLevel VARCHAR(50)
        CHECK (sLevel = 'Entry Level' OR sLevel = 'Associate' OR sLevel = 'Director' OR sLevel = 'Executive'),
    sSalary NUMERIC(38, 0) Check (sSalary > 0) NOT NULL,
    PRIMARY KEY (pName, sLevel)
);


CREATE TABLE Recruiter(
    rID NUMERIC(9, 0) PRIMARY KEY CHECK(rID > 99999999 AND rID < 1000000000),
    rName VARCHAR(50)
);


-- from the story, it is said that no field in the position table can be null,
-- afterwards, it is asked that we keep track of what positions recruiters passed
-- workers to, and that no 2 recruiters passed workers to the same position.
-- its not possible to track given position by recruiters in the recruiter table
-- because we dont know how many people each recruiter will pass.
-- on the other hand we cant leave an empty field in the position table, and we dont
-- know which recruiter will recruit to a given position when created. also, we cant leave it
-- empty or filled with a default value because rID is a foreign key to recruiter.
-- which means its not possible to keep track of recruiters passed workers in the position table as well.
--
-- the implemented solution is to create by default a defective recruiter with an unused
-- id, for example '111111111' or a managers id, when we know that he wont be recruiting
-- any workers.
Insert into Recruiter Values (111111111, 'Defective_recruiter')

CREATE TABLE Position(
    pID NUMERIC(38,0) PRIMARY KEY,
    cID NUMERIC(38,0) NOT NULL,
    dName VARCHAR(50) NOT NULL,
    pName VARCHAR(50) NOT NULL,
    sLevel VARCHAR(50) NOT NULL,
    pHours INT DEFAULT (182) check (pHours >= 0 and pHours <= 31*24) NOT NULL,
    rID  NUMERIC(9, 0) DEFAULT (111111111) NOT NULL,
    FOREIGN KEY (rID) REFERENCES Recruiter,
    FOREIGN KEY (dName, cID) REFERENCES Department,
    FOREIGN KEY (pName, sLevel) REFERENCES Salary,
);