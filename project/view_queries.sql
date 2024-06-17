--Query 1

CREATE VIEW returned_shows AS
SELECT DISTINCT title
from RecordReturns RR inner join Households H on H.hID = RR.hID
where ChildrenNum = 0
;


CREATE VIEW longest_duration AS
select genre, duration
from Programs
Where genre LIKE 'A%'
except
select P1.genre, P1.duration
from Programs P1, Programs P2
where P2.genre = P1.genre and P1.duration < P2.duration
;



--Query 2

create view valid_ratings as
select PR.title, RR.hID
from ProgramRanks PR inner join RecordReturns RR on PR.hID = RR.hID and PR.title = RR.title
UNION ALL
select PR.title, RO.hID
from ProgramRanks PR inner join RecordOrders RO on PR.hID = RO.hID and PR.title = RO.title
;

CREATE VIEW valid_3 as
select title, COUNT(title) as num_ratings
from valid_ratings
group by title
;

--Query 3

create view title_returns as
select title, COUNT(title) as num_returns
from RecordReturns
group by title
;

create view wealthy_returns as
select RR.title, COUNT(RR.title) as num_returns
from RecordReturns RR inner join Households H on H.hID = RR.hID
where netWorth >= 8
group by RR.title
;

create view shows as
select TR.title
from title_returns TR inner join wealthy_returns wr on TR.title = wr.title
where TR.num_returns >= 10 and TR.num_returns < wr.num_returns * 2
;

create view low_shows as
select distinct title
from ProgramRanks
where rank < 2
;
