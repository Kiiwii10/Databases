Select COUNT(wDate), compID, depName, pID, eID
From WorkOnProject
GROUP BY compID, depName, pID, eID


select c.compID, c.depName, c.eID, c.pID
from (  Select COUNT(wDate) as months_count, compID, depName, pID, eID
        From WorkOnProject
        GROUP BY compID, depName, pID, eID) c
where months_count >= 6

select r.compID, r.depName, count(DISTINCT eID) as Employees_Count
from (  select c.compID, c.depName, c.eID, c.pID
        from (  Select COUNT(wDate) as months_count, compID, depName, pID, eID
                From WorkOnProject
                GROUP BY compID, depName, pID, eID) c
        where months_count >= 6) r
group by r.compID, r.depName