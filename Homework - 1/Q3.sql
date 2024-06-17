select p.compID, p.depName, p.pID, p.budget , w.eID, w.hours
from project p, WorkOnProject w
where p.compID = w.compID and p.depName = w.depName and p.pID = w.pID


select p.compID, p.depName, p.pID, p.budget, w.wDate, w.eID, (w.hours * e.hourlyWage) as Monthly_wage
from ((project p inner join WorkOnProject w
ON p.compID = w.compID and p.depName = w.depName and p.pID = w.pID)
inner join Employee e ON w.eID = e.eID );



select wages.compID, wages.depName, wages.pID, wages.budget, sum(Monthly_wage) as wage
from (select p.compID, p.depName, p.pID, p.budget, w.wDate, w.eID, (w.hours * e.hourlyWage) as Monthly_wage
      from ((project p inner join WorkOnProject w
      ON p.compID = w.compID and p.depName = w.depName and p.pID = w.pID)
      inner join Employee e ON w.eID = e.eID)) wages
GROUP BY wages.compID, wages.depName, wages.pID, wages.budget



select companies.compID, AVG(companies.budget) as Avg_Budget
from (  select wages.compID, wages.depName, wages.pID, wages.budget, sum(Monthly_wage) as wage
        from (  select p.compID, p.depName, p.pID, p.budget, w.wDate, w.eID, (w.hours * e.hourlyWage) as Monthly_wage
                from ((project p inner join WorkOnProject w
                ON p.compID = w.compID and p.depName = w.depName and p.pID = w.pID)
                inner join Employee e ON w.eID = e.eID)) wages
        GROUP BY wages.compID, wages.depName, wages.pID, wages.budget) as companies
where budget < wage
group by companies.compID
order by Avg_Budget


select DISTINCT p.compID, avg(p.budget) as Avg_Budget
from Project p
group by p.compID




select comp.compID, comp.Avg_Budget
from (  select DISTINCT p.compID, avg(p.budget) as Avg_Budget
        from Project p
        group by p.compID) as comp
where comp.compID not in(   select companies.compID
                            from (  select wages.compID, wages.depName, wages.pID, wages.budget, sum(Monthly_wage) as wage
                                    from (  select p.compID, p.depName, p.pID, p.budget, w.wDate, w.eID, (w.hours * e.hourlyWage) as Monthly_wage
                                            from ((project p inner join WorkOnProject w
                                            ON p.compID = w.compID and p.depName = w.depName and p.pID = w.pID)
                                            inner join Employee e ON w.eID = e.eID)) wages
                                    GROUP BY wages.compID, wages.depName, wages.pID, wages.budget) as companies
                            where budget < wage
                            group by companies.compID)
group by comp.compID, comp.Avg_Budget
order by Avg_Budget DESC