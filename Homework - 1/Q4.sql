select DISTINCT w.pID, w.compID, w.depName, w.eID, e.hourlyWage
from WorkOnProject w inner join Employee e
On w.eID = e.eID



select DISTINCT w.compID, w.depName, w.eID, e.hourlyWage, count(w.pID) as num_projects
from WorkOnProject w inner join Employee e
On w.eID = e.eID
group by w.compID, w.depName, w.eID, e.hourlyWage

select compID, depName, count(pID) as num_projects
from Project
group by compID, depName


select compID, depName, MAX(hourlyWage) as max_depart_wage
from Employee
group by compID, depName

select distinct proj_dep.compID
from            (select compID, depName, count(pID) as num_projects
                from Project
                group by compID, depName) proj_dep
    inner join (select DISTINCT w.compID, w.depName, w.eID, e.hourlyWage, count(w.pID) as num_projects
                from WorkOnProject w inner join Employee e
                On w.eID = e.eID
                group by w.compID, w.depName, w.eID, e.hourlyWage) proj_emp
    ON proj_dep.num_projects = proj_emp.num_projects
    inner join (select compID, depName, MAX(hourlyWage) as max_depart_wage
                from Employee
                group by compID, depName) as dep_max_wages
    ON dep_max_wages.max_depart_wage = hourlyWage
group by proj_dep.compID
